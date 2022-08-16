def init():  # 初始化
    global global_dict
    global_dict = {}


def set_value(key, value):
    # 定义一个全局变量
    global_dict[key] = value


def get_value(key):
    # 获得一个全局变量，不存在则提示读取对应变量失败
    try:
        return global_dict[key]
    except:
        print('读取' + key + '失败\r\n')
