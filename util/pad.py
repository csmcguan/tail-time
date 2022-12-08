import os
import sys
import time
import multiprocessing as mp
import numpy as np 
from os import makedirs

def load_trace(f):
    return np.loadtxt(f, delimiter="\t")

def dump_trace(trace, fname):
    global dump_dir
    with open(os.path.join(dump_dir, fname), "w") as fp:
        for pkt in trace:
            fp.write("{:.4f}\t{}\n".format(pkt[0], pkt[1]))

def next_burst(trace, idx):
    direction = trace[idx][1]
    end = idx
    while end < len(trace) and trace[end][1] == direction:
        end += 1
    return trace[idx:end], len(trace[idx:end])

def get_dummys(wnd, num, direction):
    timestamps = np.random.uniform(wnd[0], wnd[1], num)
    timestamps = np.reshape(timestamps, (len(timestamps),1))
    return np.concatenate((timestamps, direction * np.ones((len(timestamps),1))), axis=1)

def burst_pad(trace):
    global ref_sequence
    t_idx = 0
    r_idx = 0
    dummys = np.array([])
    # make sure bursts are lined up by direction
    while trace[t_idx][1] != ref_sequence[r_idx][1]:
        t_idx += 1
    while t_idx < len(trace) and r_idx < len(ref_sequence):
        t_burst, t_len = next_burst(trace, t_idx)
        r_burst, r_len = next_burst(ref_sequence, r_idx)
        # get dummy cells
        if r_len > t_len:
            pad = get_dummys([t_burst[0][0], t_burst[-1][0]], r_len-t_len, trace[t_idx][1])
            if len(dummys) == 0:
                dummys = pad
            else:
                dummys = np.concatenate((dummys, pad), axis=0)
        t_idx += t_len
        r_idx += r_len
    # pad out trace to end of ref sequence
    ts = trace[-1][0] + 0.0001
    while r_idx < len(ref_sequence):
        r_burst, r_len = next_burst(ref_sequence, r_idx)
        diff = r_burst[-1][0] - r_burst[0][0]
        pad = get_dummys([ts, ts+diff], r_len, r_burst[0][1])
        pad = pad[pad[:,0].argsort(kind="mergesort")]
        if len(dummys) == 0:
            dummys = pad
        else:
            dummys = np.concatenate((dummys, pad), axis=0)
        ts = dummys[-1][0] + 0.0001
        r_idx += r_len
    if len(dummys) == 0:
        return trace
    noisy_trace = np.concatenate((trace, dummys), axis=0)
    noisy_trace = noisy_trace[noisy_trace[:,0].argsort(kind="mergesort")]
    return noisy_trace

def simulate_defense(f):
    trace = load_trace(f)
    trace = burst_pad(trace)
    f = f.split('/')[-1]
    dump_trace(trace, f)

def get_ref_sequence(f):
    trace = load_trace(f)
    return [f, len(trace)]

def parallel(flist, func, n_jobs=25):
    pool = mp.Pool(n_jobs)

    if func == "get_ref_sequence":
        traces = pool.map(get_ref_sequence, flist)
        traces.sort(key = lambda traces: traces[1])
        return traces[-1][0]

    pool.map(simulate_defense, flist)

if __name__ == '__main__':
    global log
    global defended
    global ref_sequence
    global addon

    log = "log"
    defended = "defended"
    addon = sys.argv[1]
    flist  = []
    for file in os.listdir(os.path.join(log, addon)):
        flist.append(os.path.join(log, addon, file))

    if not os.path.exists(defended):
        makedirs(defended)
    dump_dir = os.path.join(defended, addon)
    if not os.path.exists(dump_dir):
        makedirs(dump_dir)

    print("traces are dumped to {}".format(dump_dir))

    start = time.time()
    print("getting reference sequence")
    ref_sequence = parallel(flist, "get_ref_sequence")
    print("reference sequence: {}".format(ref_sequence))
    ref_sequence = load_trace(ref_sequence)
    print("time: {}".format(time.time() - start))

    start = time.time()
    print("padding traces")
    parallel(flist, "simulate_defense")
    print("time: {}".format(time.time() - start))
