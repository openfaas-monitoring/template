import globalFlag


def function1(res, args):
    print("function1")
    return res, args


def function2(res, args):
    print("function2")
    globalFlag.set_value('flag1', False)
    args['num'] = 0
    return res, args


def function3(res, args):
    print("function3")
    return res, args


def function4(res, args):
    print("function4")
    args['num'] += 1
    print(args['num'])
    if args['num'] > 10:
        globalFlag.set_value('flag2', False)
    return res, args


def function5(res, args):
    print("function5")
    return res, args
