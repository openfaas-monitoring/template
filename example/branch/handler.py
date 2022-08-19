from function import globalFlag
import time


def function1(args):
    args['res'] = args['std_in']
    if int(args['res']) % 2 == 0:
        globalFlag.set_value('flag1', False)
    else:
        globalFlag.set_value('flag1', True)
    return args


def function2(args):
    time.sleep(1)
    args['res'] = args['res'][::-1]
    return args


def function3(args):
    time.sleep(1)
    args['res'] = str(int(args['res']) * 2)
    return args
