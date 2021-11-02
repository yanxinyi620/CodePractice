import os
import gzip
import numpy as np
import pandas as pd
import urllib
import tarfile
import requests

import torchvision.datasets.mnist
from torch.utils.model_zoo import tqdm
from torchvision.datasets.utils import download_and_extract_archive


USER_AGENT = "gcastle-hub/dataset"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"}

root = '.'
url = 'https://raw.githubusercontent.com/gcastle-hub/dataset/master/alarm/18V_55N_Wireless.tar.gz'
filename = '18V_55N_Wireless.tar.gz'
md5 = '36ee135b86c8dbe09668d9284c23575b'

# download_and_extract_archive
download_and_extract_archive(url, download_root=root, filename=filename, md5=md5)

X = pd.read_csv(root+'/'+filename[:-7]+'/Alarm.csv')
true_dag = np.load(root+'/'+filename[:-7]+'/DAG.npy')


'''
# raw csv and npy
if 'urllib.request.urlopen':
    # urllib.request.urlopen(urllib.request.Request())
    response = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": USER_AGENT}))
    with open(filename, "wb") as fh:
        fh.write(response.read())

    # Read from downloaded file
    tar = tarfile.open(filename, mode="r:gz")
    X = pd.read_csv(tar.extractfile(tar.getnames()[1]), header=0, sep=",")

# raw gz
if 'raw gz':

    url = 'https://raw.githubusercontent.com/yanxinyi620/Python_practice/master/datasets/18V_55N_Wireless/'
    data_file = 'Alarm.csv.gz'
    dag_file = 'DAG.npy.gz'

    url_data = url + data_file
    url_dag = url + dag_file

    # urllib.request.urlopen(urllib.request.Request())
    response = urllib.request.urlopen(urllib.request.Request(url_data, headers={"User-Agent": USER_AGENT}))
    with open(data_file, "wb") as fh:
            fh.write(response.read())

    response = urllib.request.urlopen(urllib.request.Request(url_dag, headers={"User-Agent": USER_AGENT}))
    with open(dag_file, "wb") as fh:
            fh.write(response.read())

    X = pd.read_csv(data_file, compression='gzip')
    f = gzip.GzipFile(dag_file, "r")
    true_dag = np.load(f)

# raw csv and npy
if 'raw csv and npy':

    url_data = 'https://raw.githubusercontent.com/yanxinyi620/Python_practice/master/datasets/18V_55N_Wireless/Alarm.csv'
    url_dag = 'https://raw.githubusercontent.com/yanxinyi620/Python_practice/master/datasets/18V_55N_Wireless/DAG.npy'
    # url_data = 'C:/Users/yanxinyi/Documents/GitHub/Python_practice/datasets/18V_55N_Wireless/Alarm.csv'
    # url_dag = 'C:/Users/yanxinyi/Documents/GitHub/Python_practice/datasets/18V_55N_Wireless/DAG.npy'

    X = pd.read_csv(url_data)
    # true_dag = np.load(url_dag)
'''