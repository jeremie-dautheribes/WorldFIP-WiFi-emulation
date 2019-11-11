#!/usr/bin/env python3
from time import sleep
from argparse import ArgumentParser
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, SO_REUSEPORT
from frame import RP_Dat, ID_Dat


def usleep(sec):
    sleep(sec / 1000 / 1000)


RETURN_TIME = 10


class Consumer(object):
    def __init__(self, id: int):
        self._id = id
        self._data = None

    def run_server(self, port=5432):
        self._sock = socket(AF_INET, SOCK_DGRAM)
        self._sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self._sock.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        self._sock.bind(('', port))
        self._port = port

    def recv_id_dat(self):
        data, addr = self._sock.recvfrom(ID_Dat.size())
        try:
            return ID_Dat.from_repr(data)
        except:
            return None

    def recv_rp_dat(self):
        old_to = self._sock.gettimeout()
        self._sock.settimeout(RETURN_TIME)
        try:
            data, addr = self._sock.recvfrom(RP_Dat.size())
        finally:
            self._sock.settimeout(old_to)

        try:
            return RP_Dat.from_repr(data)
        except:
            return None

    def do_loop(self):
        while True:
            # 1. Get the ID_Dat, use the existing one if exists
            id_dat = self.recv_id_dat()

            # 2. Ignore messages for which we are not a consumer
            if not id_dat or id_dat.id != self._id:
                continue

            # 4. Get the object from the bus
            usleep(RETURN_TIME)
            rp_dat, to = None, False
            while not rp_dat:
                try:
                    rp_dat = self.recv_rp_dat()
                except:
                    print('timeout reached, ignoring')
                    to = True
                    break
            if to:
                continue

            # 4.5 I worked
            print(f'received: {rp_dat}')


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('id', type=int)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    prod = Consumer(args.id)
    prod.run_server()
    prod.do_loop()
