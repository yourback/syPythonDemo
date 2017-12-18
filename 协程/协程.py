import time

# 生成器
def A():
    while True:
        print('----A----')
        yield
        time.sleep(0.5)


def B(c):
    while True:
        print('----B----')
        # python 2.7 是 c.next()
        # python 3.x 是 next(c)
        next(c)
        time.sleep(0.5)


if __name__ == '__main__':
    a = A()
    B(a)
