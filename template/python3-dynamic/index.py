import sys
import logging
import json
import threading
import os
from function import globalFlag
from function import handler

logger = logging.getLogger("funcLogger")
logger.setLevel(logging.INFO)
sh = logging.FileHandler('/home/app/log/function.log', 'w', encoding='utf-8')
sh.setFormatter(
    logging.Formatter(fmt='%(asctime)s %(levelname)s %(threadName)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S'))
logger.addHandler(sh)


def get_stdin():
    buf = ""
    while True:
        line = sys.stdin.readline()
        buf += line
        if line == "":
            break
    return buf


class ThreadWithConfig(threading.Thread):
    def __init__(self, name, config_, args_):
        super(ThreadWithConfig, self).__init__()
        self.name = name
        self.config = config_
        self.args_ = args_
        self._return = None

    def run(self):
        self._return = runWithConfig(self.config, self.args_)

    def get_return(self):
        threading.Thread.join(self)
        return self._return


def runWithConfig(config: dict, args: dict):
    # 根据配置文件执行函数
    now_func_name = config['start_func_name']
    while True:
        now_func_info = config[now_func_name]

        if now_func_name.startswith('join'):  # 执行线程等待
            for wait_thread in now_func_info['wait_threads']:
                eval('{}.join()'.format(wait_thread))
                args1 = eval('{}.get_return()'.format(wait_thread))
                args.update(args1)
            now_func_name = now_func_info['next_func_true']
        else:  # 执行当前函数
            logger.info('{} started'.format(now_func_name))
            sys.stdout.flush()
            args = eval('handler.{}'.format(now_func_name))(args)
            logger.info('{} over'.format(now_func_name))
            sys.stdout.flush()

        # 根据控制类型决定下一步执行
        step_type = now_func_info['type']
        if step_type == 'order':
            now_func_name = now_func_info['next_func_true']
        elif step_type == 'branch' or step_type == 'loop':
            condition = globalFlag.get_value(now_func_info['condition'])
            if condition:
                now_func_name = now_func_info['next_func_true']
            else:
                now_func_name = now_func_info['next_func_false']

        if now_func_name == "":  # 判断退出条件
            break
    return args


if __name__ == "__main__":
    # 运行开始
    logger.info('all started')
    sys.stdout.flush()

    # 初始化全局变量
    globalFlag.init()

    # 读取配置文件
    with open('./function/process-cfg.json', 'r') as f:
        config_json = json.load(f)

    # 函数名称标志
    label_path = '/home/app/log/' + config_json['name']
    if not os.path.exists(label_path):
        os.makedirs(label_path)

    # 设置全局标志变量
    for flag_tuple in config_json['global']:
        globalFlag.set_value(flag_tuple[0], True if flag_tuple[1] == 'True' else False)

    # 获取标准输入
    st = get_stdin()
    args = {"std_in": st}

    # 将配置以字典形式存入内存
    config = dict()
    # 读入各个线程的配置文件
    for thread_name, thread_process in config_json['thread_process'].items():
        func_info = {'start_func_name': ""}
        for i, func in enumerate(thread_process):
            func_name = func['func_name']
            if func_name == 'join':
                func_name = 'join' + str(i)
            if i == 0:
                func_info['start_func_name'] = func_name
            func_info[func_name] = func
        config[thread_name] = func_info

    extra_threads = config_json['extra_threads']
    if len(extra_threads) == 0:
        # 单线程运行
        args = runWithConfig(config['main'], args)
    else:
        # 多线程运行
        for thread_name in extra_threads:
            exec("{} = ThreadWithConfig('{}', config['{}'], args)".format(thread_name, thread_name, thread_name))
            eval("{}.start()".format(thread_name))
        # 主线程运行
        args = runWithConfig(config['main'], args)

    if 'res' in args.keys():
        print(args['res'])

    logger.info("all end")
    logger.info("over")
