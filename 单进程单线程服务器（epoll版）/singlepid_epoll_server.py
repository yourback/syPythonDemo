# 鉴于poll和select方法类似，只是解决了并发上限问题
# 所以直接上epoll方法

from select import *
from socket import *


def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)

    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    serverSocket.bind(("", 7788))

    serverSocket.listen(5)

    # 创建epoll对象
    epoll = select.epoll()

    # 存放conn与addr对应
    addrs = {}
    conns = {}

    # 服务器socket注册进入epoll中
    epoll.register(serverSocket.fileno, select.EPOLLIN | select.EPOLLET)

    while True:
        # 获得有数据来的事件列表
        epoll_list = epoll.poll()

        # 遍历事件列表
        for fd, events in epoll_list:
            if fd == serverSocket.fileno:
                conn, addr = serverSocket.accept()
                print('%s已经连接' % addr)

                # 存放连接与地址
                conns[conn.fileno] = conn
                addrs[conn.fileno] = addr

                # 把连接注册到epoll中
                epoll.register(conn.fileno, select.EPOLLIN | select.EPOLLET)

            elif events == select.EPOLLIN:
                recvDataConn = conns[fd]
                recvData = recvDataConn.recv(1024)
                recvDataAddr = addrs[fd]
                if recvData:
                    print("%s发来消息：%s" % (str(recvDataAddr), recvData))
                    recvDataConn.send(recvData)
                else:
                    print("%s断开连接" % str(recvDataAddr))
                    del conns[fd]
                    del addrs[fd]
                    epoll.unregister(fd)
                    recvDataConn.close()


if __name__ == '__main__':
    main()
