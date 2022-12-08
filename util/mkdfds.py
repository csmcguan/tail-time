import os
import sys
import time
import numpy as np 
import pickle
from os import makedirs

def load_trace(file):
    trace = np.loadtxt(file, delimiter="\t")
    trace = trace[:,1]
    if len(trace) < 5000:
        append = [0 for i in range(5000 - len(trace))]
        trace = np.append(trace, append)
    elif len(trace) > 5000:
        trace = trace[:5000]
    return trace

def dump_pkl(ds):
    for d in ds:
        with open(os.path.join(dst, "{}.pkl".format(d)), "wb") as fp:
            print("{}: {}".format(d, ds[d].shape))
            pickle.dump(ds[d], fp, protocol=2)

def mkdfds(conf):
    global src

    ds = {}
    X_train = "X_train_{}".format(conf)
    X_test  = "X_test_{}".format(conf)
    X_valid = "X_valid_{}".format(conf)
    y_train = "y_train_{}".format(conf)
    y_test  = "y_test_{}".format(conf)
    y_valid = "y_valid_{}".format(conf)
    ds[X_train] = np.array([])
    ds[X_test]  = np.array([])
    ds[X_valid] = np.array([])
    ds[y_train] = np.array([])
    ds[y_test]  = np.array([])
    ds[y_valid] = np.array([])

    for site in range(100):
        # test
        for i in range(5):
            for inst in range(0, 2):
                f = os.path.join(src, "{}-{}.cell".format(site, i*20+inst))
                trace = load_trace(f)
                if len(ds[X_test]) == 0 and len(ds[y_test]) == 0:
                    ds[X_test] = np.append(ds[X_test], trace)
                    ds[y_test] = np.append(ds[y_test], site)
                else:
                    ds[X_test] = np.vstack((ds[X_test], trace))
                    ds[y_test] = np.append(ds[y_test], site)
            # train
            for inst in range(2, 18):
                f = os.path.join(src, "{}-{}.cell".format(site, i*20+inst))
                trace = load_trace(f)
                if len(ds[X_train]) == 0 and len(ds[y_train]) == 0:
                    ds[X_train] = np.append(ds[X_train], trace)
                    ds[y_train] = np.append(ds[y_train], site)
                else:
                    ds[X_train] = np.vstack((ds[X_train], trace))
                    ds[y_train] = np.append(ds[y_train], site)
            # valid
            for inst in range(18, 20):
                f = os.path.join(src, "{}-{}.cell".format(site, i*20+inst))
                trace = load_trace(f)
                if len(ds[X_valid]) == 0 and len(ds[y_valid]) == 0:
                    ds[X_valid] = np.append(ds[X_valid], trace)
                    ds[y_valid] = np.append(ds[y_valid], site)
                else:
                    ds[X_valid] = np.vstack((ds[X_valid], trace))
                    ds[y_valid] = np.append(ds[y_valid], site)
    dump_pkl(ds)

if __name__ == '__main__':
    global src

    if len(sys.argv) != 2:
        print("usage: python3 mkdfds.py <conf>")
        sys.exit(1)

    src = sys.argv[1]
    conf = src.split('/')[-1]

    dst = "./dfds/{}".format(conf)
    if not os.path.exists(dst):
        os.makedirs(dst)
    mkdfds(conf)
