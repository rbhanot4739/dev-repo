from multiprocessing import Process, Pipe, current_process


def tester(child_conn):
    data = child_conn.recv()
    msg = child_conn.recv()
    print(data, ' ', msg)
    data = [val * 2 for val in data]
    child_conn.send(data)


if __name__ == '__main__':
    arr = [1, 2, 3]
    parent_conn, child_conn = Pipe()
    p1 = Process(target=tester, args=(child_conn,))
    p1.start()
    parent_conn.send(arr)
    parent_conn.send('msg ')
    print(parent_conn.recv())
