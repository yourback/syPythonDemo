# 单进程单线程，利用select函数完成并发服务器
from select import *
from socket import *


def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # 服务器主动断开连接后，在2MSL时间内可以重启占用原来端口号，继续为客户端服务
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    serverSocket.bind(("", 7788))

    serverSocket.listen(5)

    inputs = [serverSocket]

    # 新建字典   key 连接  value 客户端地址 (ip：端口号)
    duiying = {}

    while True:
        readable, writable, exceptional = select(inputs, [], [])

        for sock in readable:
            if sock == serverSocket:
                conn, addr = serverSocket.accept()

                print('%s连接了' % str(addr))

                duiying[conn] = addr

                inputs.append(conn)

            else:
                recvData = sock.recv(1024)
                add = str(duiying[sock])
                if recvData:
                    print('收到%s的消息：%s' % (add, recvData))
                    sock.send(recvData)
                else:
                    del duiying[sock]
                    print('%s断开连接' % add)
                    inputs.remove(sock)
                    sock.close()


if __name__ == '__main__':
    main()
