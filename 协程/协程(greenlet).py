from greenlet import *
import time


def task1():
    while True:
        print('------task1------')
        grt2.switch()
        time.sleep(0.5)


def task2():
    while True:
        print('------task2------')
        grt1.switch()
        time.sleep(0.5)


if __name__ == '__main__':
    grt1 = greenlet(task1)
    grt2 = greenlet(task2)
    grt1.switch()
