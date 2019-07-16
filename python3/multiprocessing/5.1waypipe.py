from multiprocessing import Process, Pipe, current_process


def sender(s):
    s.send('Sent Hello to Receiver')


def receiver(r):
    print(r.recv())  # r.send('Hello to Sender')  -- Uncomment this and see the communication will fail


if __name__ == '__main__':
    recvr_conn, sender_conn = Pipe(duplex=False)
    send_proc = Process(target=sender, args=(sender_conn,))
    recv_proc = Process(target=receiver, args=(recvr_conn,))

    send_proc.start()
    recv_proc.start()

    send_proc.join()
    recv_proc.join()
