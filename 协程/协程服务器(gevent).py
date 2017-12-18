from gevent import socket, monkey, spawn, getcurrent
monkey.patch_all()

conns = {}
addrs = {}


def handle_request(conn):
    print(getcurrent())
    while True:
        data = conn.recv(1024)
        if data:
            print("%s发来数据：%s" % (str(addrs[conn.fileno]), data))
            conn.send(data)
        else:
            print("%s断开连接" % str(addrs[conn.fileno]))
            del conns[conn.fileno]
            del addrs[conn.fileno]
            conn.close()
            break


def server(port):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', port))
    s.listen(5)
    while True:
        print('等待新连接')
        cli, addr = s.accept()
        conns[cli.fileno] = cli
        addrs[cli.fileno] = addr
        spawn(handle_request, cli)


if __name__ == '__main__':

    server(7788)
