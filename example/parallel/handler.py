from function import globalFlag
import time
import os

func_name = 'paralleltest'
label_path = '/home/app/log/' + func_name
if not os.path.exists(label_path):
    os.makedirs(label_path)


def function1(args):
    args['num1'] = int(args['std_in'])
    if args['num1'] % 2 == 0:
        globalFlag.set_value('flag2', True)
    else:
        globalFlag.set_value('flag2', False)
    return args


def function2(args):
    time.sleep(2)
    if 'num2' not in args.keys():
        args['num2'] = 2
    else:
        args['num2'] += 1
    if args['num2'] < 5:
        globalFlag.set_value('flag1', True)
    else:
        globalFlag.set_value('flag1', False)

    return args


def function3(args):
    time.sleep(2)
    args['num3'] = 3
    return args


def function4(args):
    args['res'] = str(args['num1']) + str(args['num2']) + str(args['num3'])
    return args


def function5(args):
    time.sleep(3)
    args['num3'] = 5
    return args
