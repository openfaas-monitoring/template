from function import globalFlag
import time


def function1(args):
    args['num1'] = args['std_in']
    return args


def function2(args):
    time.sleep(2)
    args['num1'] = args['num1'] + args['num1']
    if len(args['num1']) < 10:
        globalFlag.set_value('flag1', True)
    else:
        globalFlag.set_value('flag1', False)

    return args


def function3(args):
    args['res'] = args['num1']
    return args
