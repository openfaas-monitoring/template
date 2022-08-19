from function import globalFlag
import time


def function1(args):
    args['num1'] = int(args['std_in'])
    return args


def function2(args):
    time.sleep(1)
    args['num2'] = args['num1'] + 1

    return args


def function3(args):
    time.sleep(1)
    args['num3'] = args['num1'] + 2
    return args


def function4(args):
    time.sleep(1)
    args['num4'] = args['num1'] + 3
    return args


def function5(args):
    args['res'] = str(args['num1']) + str(args['num2']) + str(args['num3']) + str(args['num4'])
    return args
