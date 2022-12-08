import os
import sys
import time
import numpy as np 
import multiprocessing as mp

def load_trace(file):
    trace = np.loadtxt(file, delimiter="\t")
    return trace[:,1]

def bwoh(f):
    global undefended
    global defended

    orig = len(load_trace(os.path.join(undefended, f)))
    padd = len(load_trace(os.path.join(defended, f)))
    return (padd - orig) / orig

def parallel(flist, n_jobs = 25):
    pool = mp.Pool(n_jobs)
    ovhd  = pool.map(bwoh, flist)    
    return ovhd

if __name__ == '__main__':
    global undefended
    global defended

    if len(sys.argv) != 2:
        print("usage: python3 bwoh.py <config>")
        sys.exit(1)

    undefended = "./log/undefended/"
    defended = "./defended/{}".format(sys.argv[1])

    flist = []
    for f in os.listdir(defended):
        flist.append(f)
    ovhd = parallel(flist)
    ovhd.sort()
    print("{} avg: {}".format(sys.argv[1], sum(ovhd) / len(ovhd)))
    print("{} med: {}".format(sys.argv[1], ovhd[len(ovhd) // 2]))
