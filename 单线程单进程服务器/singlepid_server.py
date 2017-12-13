# 单进程单线程，完成并发服务器
from socket import *


def main():

    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(("", 7788))
    serverSocket.listen(5)

    serverSocket.setblocking(False)

    clientServerList = []

    while True:
        try:
            clientServer, clientAddr = serverSocket.accept()
        except Exception as e:
            pass
        else:
            clientServer.setblocking(False)
            print("客户端：%s已连接" % str(clientAddr))
            clientServerList.append((clientServer, clientAddr))

        for clientServer, clientAddr in clientServerList:
            try:
                recvData = clientServer.recv(1024)
            except Exception as e:
                pass
            else:
                if recvData:
                    print("%s:%s" % (str(clientAddr), recvData))
                else:
                    clientServer.close()
                    print("%s断开连接" % str(clientAddr))
                    clientServerList.remove((clientServer, clientAddr))


if __name__ == '__main__':
    main()