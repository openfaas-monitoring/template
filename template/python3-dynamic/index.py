import sys
import logging
import globalFlag
import json
from function import handler

logger = logging.getLogger("funcLogger")
logger.setLevel(logging.INFO)
sh = logging.StreamHandler(stream=sys.stderr)
sh.setFormatter(logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S'))
logger.addHandler(sh)


def get_stdin():
    buf = ""
    while True:
        line = sys.stdin.readline()
        buf += line
        if line == "":
            break
    return buf


if __name__ == "__main__":
    # 初始化全局变量
    globalFlag.init()

    # 读取配置文件
    with open('./function/process-cfg.json', 'r') as f:
        process = json.load(f)

    # 设置全局标志变量
    for flag_tuple in process['global']:
        globalFlag.set_value(flag_tuple[0], True if flag_tuple[1] == 'True' else False)

    # 获取标准输入
    # st = get_stdin()
    # if ret != None:
    #     print(ret)
    res, args = " ", dict()

    # 将配置以字典形式存入内存
    func_info = dict()
    now_func_name = ""
    for i, func in enumerate(process['process']):
        func_info[func['func_name']] = func
        if i == 0:
            now_func_name = func['func_name']

    # 根据配置文件执行函数
    while True:
        now_func_info = func_info[now_func_name]

        # 执行当前函数
        logger.info('{} started'.format(now_func_name))
        res, args = eval('handler.{}'.format(now_func_name))(res, args)
        logger.info('{} over'.format(now_func_name))

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

        # 判断退出条件
        if now_func_name == "":
            break

    print('over')
