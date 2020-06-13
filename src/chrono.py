from time import time

from src import utils as ut

def initRecord():
    return time()

def addRecord(records, tLast, header):

    t = time()
    delta = ut.round_to_n(t - tLast, 3)
    records.append(delta)

    print(header + ": " + str(delta) + "s")

    return t