import pandas as pd

from config import get_logger
from utils import CSV_SEP


log = get_logger()


def origin_dataset_to_prepare_csv(dataset_file, psi_prepare):
    log.info("run get_psi_prefix_csv")
    data = pd.read_csv(dataset_file)
    output = pd.DataFrame(data.get('id'))
    output.to_csv(psi_prepare, sep=CSV_SEP, header=False, index=None)
    log.info("finish get_psi_prefix_csv")


def origin_dataset_to_prepare_csv2(dataset_file, psi_prepare):
    log.info("run get_psi_prefix_csv")
    
    f1 = open(psi_prepare, 'w')
    with open(dataset_file) as f:
        columns = next(f)
        columns_list = columns.strip().split(',')
        id_idx = columns_list.index('id')
        for line in f:
            id = line.strip().split(',', id_idx+1)[id_idx]
            print(id, file=f1)
    f1.close()

    log.info("finish get_psi_prefix_csv")


if __name__=="__main__":

    # 提供2组数据测试
    # 1000w * 3 (id: 10M, data: 20M)
    file_path1 = 'D:/Github/CodePractice/code_wb/datasets/xinyi_table_0.csv'
    # 50w * 301 (id: 0.5M, data: 150M)
    file_path2 = 'D:/Github/CodePractice/code_wb/datasets/epsilon_hetero_P1.csv'

    file_path = file_path2
    file_save = 'D:/Github/CodePractice/code_wb/datasets/save_temp.csv'

    # 原方案, origin_dataset_to_prepare_csv
    # file_path1：11.2s (CPU: 100%, 内存: 1495M)
    # file_path2：16.3s (CPU: 100%, 内存: 3474M)
    origin_dataset_to_prepare_csv(file_path, file_save)

    # 原方案, origin_dataset_to_prepare_csv
    # file_path1：4.14s (CPU: 104%, 内存: 47.8M)
    # file_path2：2.50s (CPU: 118%, 内存: 47.9M)
    origin_dataset_to_prepare_csv2(file_path, file_save)
