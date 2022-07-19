import math
import time
import itertools
import numpy as np
import pandas as pd
from threading import Thread
from multiprocessing import Process, Pool
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


'''
多进程建议在 linux 中运行
多进程 (ProcessPoolExecutor) 在 windows 环境下会出现特别慢或者报错等异常情况
多进程 (Process/Pool) 在 windows 或者 notebook 中变慢或报错，在 linux 正常
'''

path_prefix = '../datasets/'
test_name = 'hist'


if test_name == 'IO':

    data0_path = path_prefix + 'epsilon_hetero_P1.csv'
    data1_path = path_prefix + 'epsilon_hetero_P1.csv'
    data_path = [data0_path, data1_path]

    def load_dataset(file_name, idx):
        data = pd.read_csv(file_name, header=0)
        return None

    # 单线程/进程  # 30.448s
    t = time.time()
    data0 = pd.read_csv(data0_path, header=0)
    data1 = pd.read_csv(data1_path, header=0)
    print(time.time() - t)


    # 多线程  # 16.700s
    t = time.time()
    ths = []
    for i in range(len(data_path)):
        th = Thread(target=load_dataset, args=(data_path[i], i,))
        th.start()
        ths.append(th)
    for th in ths:
        th.join()
    print(time.time() - t)


    # 多进程  # 58.678s
    t = time.time()
    ths = []
    for i in range(len(data_path)):
        th = Process(target=load_dataset, args=(data_path[i], i,))
        th.start()
        ths.append(th)
    for th in ths:
        th.join()
    print(time.time() - t)


    # concurrent.futures 多线程/多进程
    # 多线程  # 16.804s
    t = time.time()
    pool = ThreadPoolExecutor(max_workers=2)
    results = list(pool.map(load_dataset, data_path, [0, 1]))
    print(time.time() - t)

    # 多进程  # 36.519s (在 Notebook 中出现 ERROE)
    t = time.time()
    pool = ProcessPoolExecutor(max_workers=2)
    results = list(pool.map(load_dataset, data_path, [0, 1]))
    print(time.time() - t)


if test_name == 'CPU':
    
    PRIMES = [112272535095293,112582705942171,
              112272535095293,115280095190773,
              115797848077099,1099726899285419]

    def is_prime(n):
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False

        sqrt_n = int(math.floor(math.sqrt(n)))
        for i in range(3, sqrt_n + 1, 2):
            if n % i == 0:
                return False
        return True

    # 单线程/进程  0.864s
    start = time.time()
    results = list(map(is_prime, PRIMES))
    end = time.time()
    print ('Took %.3f seconds.' % (end - start))

    # 多线程  0.876s
    start = time.time()
    pool = ThreadPoolExecutor(max_workers=6)
    results = list(pool.map(is_prime, PRIMES))
    end = time.time()
    print ('Took %.3f seconds.' % (end - start))

    # 多进程  0.256s
    start = time.time()
    pool = ProcessPoolExecutor(max_workers=6)
    results = list(pool.map(is_prime, PRIMES))
    end = time.time()
    print ('Took %.3f seconds.' % (end - start)) 

    # 多进程 0.239s
    start = time.time()
    ths = []
    for i in range(len(PRIMES)):
        th = Process(target=is_prime, args=(PRIMES[i],))
        th.start()
        ths.append(th)
    for th in ths:
        th.join()
    end = time.time()
    print ('Took %.3f seconds.' % (end - start)) 

    # 多进程 0.259s
    start = time.time()
    pool = Pool(6)
    results = list(pool.map(is_prime, PRIMES))
    end = time.time()
    print ('Took %.3f seconds.' % (end - start))


if test_name == 'hist':
    # testing
    df = pd.read_csv(path_prefix + 'epsilon_hetero_P1.csv', header=0)

    if 'id' in df.columns:
        df.drop('id', axis=1, inplace=True)
    X = df.values

    n = X.shape[0]
    d = X.shape[1]

    max_bin = 32
    X_split = np.zeros((d, max_bin+1))
    X_bin = np.zeros((d, n), dtype='int16')

    for k in range(d):
        Xk_bin, Xk_split = pd.qcut(X[:, k], max_bin, labels=False, retbins=True)

        X_split[k] = Xk_split
        X_bin[k] = Xk_bin

    # hist
    d = X_bin.shape[0]

    g_hist = np.zeros((d, max_bin))
    h_hist = np.zeros((d, max_bin))

    glist_instance = X_bin[2] + 1
    hlist_instance = X_bin[6] + 6

    # # hist0
    # start = time.time()
    # for k in range(d):

    #     Xk_bin = X_bin[k]
        
    #     gk_hist = pd.DataFrame(glist_instance).groupby(Xk_bin).sum()
    #     hk_hist = pd.DataFrame(hlist_instance).groupby(Xk_bin).sum()

    #     for v in gk_hist.index:
    #         g_hist[k][v] = gk_hist.loc[v, 0]
    #         h_hist[k][v] = hk_hist.loc[v, 0]
    # end = time.time()
    # print ('Took %.3f seconds.' % (end - start))
    # print(g_hist[10, -10], h_hist[10, -10])

    # # hist1
    # start = time.time()
    # for k in range(d):

    #     Xk_bin = X_bin[k]

    #     for v in range(max_bin):
    #         g_hist[k][v] = glist_instance[Xk_bin==v].sum()
    #         h_hist[k][v] = hlist_instance[Xk_bin==v].sum()
    # end = time.time()
    # print ('Took %.3f seconds.' % (end - start))
    # print(g_hist[10, -10], h_hist[10, -10])


    # mult thread
    def hist_group(k, Xk_bin, max_bin, glist_instance, hlist_instance):

        # Xk_bin = X_bin[k]

        gk_list = np.zeros((max_bin))
        hk_list = np.zeros((max_bin))
        
        gk_hist = pd.DataFrame(glist_instance).groupby(Xk_bin).sum()
        hk_hist = pd.DataFrame(hlist_instance).groupby(Xk_bin).sum()

        for v in gk_hist.index:
            # g_hist[k][v] = gk_hist.loc[v, 0]
            # h_hist[k][v] = hk_hist.loc[v, 0]
            gk_list[v] = gk_hist.loc[v, 0]
            hk_list[v] = hk_hist.loc[v, 0]

        return gk_list, hk_list

    # start = time.time()
    # pool = ProcessPoolExecutor(max_workers=4)
    # results = list(pool.map(hist_group, range(d)))

    # g_hist = np.array([gh[0] for gh in results])
    # h_hist = np.array([gh[1] for gh in results])

    # end = time.time()
    # print ('Took %.3f seconds.' % (end - start))
    # print(g_hist[10, -10], h_hist[10, -10])

    def main():

        start = time.time()
        pool = ProcessPoolExecutor(max_workers=4)
        results = list(pool.map(hist_group, range(d), X_bin[:][:], 
                                itertools.repeat(max_bin), itertools.repeat(glist_instance), 
                                itertools.repeat(hlist_instance), chunksize=4))
        # results = list(pool.map(hist_group, range(d), [X_bin[k] for k in range(d)], chunksize=4))

        g_hist = np.array([gh[0] for gh in results])
        h_hist = np.array([gh[1] for gh in results])

        end = time.time()
        print ('Took %.3f seconds.' % (end - start))
        print(g_hist[10, -10], h_hist[10, -10])

    main()
