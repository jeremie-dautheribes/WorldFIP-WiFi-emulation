#!/usr/bin/env python3
from time import sleep
from math import gcd
from functools import reduce
from itertools import cycle
from frame import ID_Dat


class BusArbitror(object):
    '''
    Représente un arbitre de bus du protocol World-FIP
    '''
    def __init__(self, table={}):
        self._table = table
        self._microcycle, self._macrocycle = self.cycles_from_table(table)

    def do_loop(self):
        '''
        Loop over all messages

        This 1st version simply print the messages, tgit he next version should
        actually send the frame to the network.
        '''
        t2 = None
        for t, msg in cycle(self.list_macrocycle()):
            if t != t2:
                t2 = t
                sleep(bus._microcycle / 1000)
                print(f't = {t}ms')

            # Do the job
            print('\t', msg.__dict__)

    def list_macrocycle(self):
        '''
        Do a full macrocycle

        return a tuple `(time, Frame)`
        '''
        for t in range(0, self._macrocycle, self._microcycle):
            # Loop over the table to see what message should be send
            for id, period in self._table.items():
                if t % period == 0:
                    yield (t, ID_Dat(id))

    @staticmethod
    def cycles_from_table(table):
        '''Return the microcycle and macrocycle from a period table'''
        def lcm(numbers):
            '''Helper to compute the Least Commom Multiple'''
            return reduce(lambda a, b: a * b // gcd(a, b), numbers)
        return (min(table.values()), lcm(table.values()))


if __name__ == '__main__':
    bus = BusArbitror({
        101: 100,
        102: 200,
        103: 500,
        104: 100,
        105: 200,
    })
    bus.do_loop()
