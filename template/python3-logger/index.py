import sys
import logging
from function import handler

logger = logging.getLogger("funcLogger")
logger.setLevel(logging.INFO)
sh = logging.StreamHandler(stream=sys.stderr)
sh.setFormatter(logging.Formatter(
    fmt='%(asctime)s %(levelname)s %(funcName)s %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S'))
logger.addHandler(sh)


def get_stdin():
    buf = ""
    while(True):
        line = sys.stdin.readline()
        buf += line
        if line == "":
            break
    return buf


if __name__ == "__main__":
    st = get_stdin()
    ret = handler.handle(st, logger)
    if ret != None:
        print(ret)
