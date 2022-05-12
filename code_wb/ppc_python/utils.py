import pandas as pd
from enum import Enum


DEFAULT_DATASET_RECORD_COUNT = 5
CSV_SEP = ','
NORMALIZED_NAMES = 'field{}'


class AlgorithmType(Enum):
    PPC_SQL = 1
    PPC_MPC = 2
    PSI_TWO = 3
    PSI_MULTI = 4
    PPC_TRAIN = 5
    PPC_PREDICT = 6


def read_content_from_file_by_binary(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
    return content


def make_dataframe(dataset):
    csv_line = dataset.strip().split("\n")
    data = list(map(lambda x: x.split(CSV_SEP), csv_line[1:]))
    frame = pd.DataFrame(data, columns=csv_line[0].split(CSV_SEP))
    return frame


if __name__=="__main__":

    # 提供2组数据测试
    # 1000w * 3 (id: 10M, data: 20M)
    file_path1 = 'D:/Github/CodePractice/code_wb/datasets/xinyi_table_0.csv'
    # 50w * 301 (id: 0.5M, data: 150M)
    file_path2 = 'D:/Github/CodePractice/code_wb/datasets/epsilon_hetero_P1.csv'

    file_path = file_path2

    # with open(file_path) as f:
        
    #     columns = next(f)
    #     columns_list = columns.strip().split(',')

    #     for line in f:
    #         line_list = line.strip().split(',')
    #         break

    raw_data = read_content_from_file_by_binary(file_path)
    df = make_dataframe(str(raw_data, 'utf-8'))  # 使用 file_path2，内存 10G+, 任务杀掉了
