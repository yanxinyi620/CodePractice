import os
import numpy as np
import pandas as pd

from config import get_logger
from utils import DEFAULT_DATASET_RECORD_COUNT


log = get_logger()


def check_csv_format(df):
    try:
        data = df.columns
        # empty file is ok
        if data[0] == 'Placeholder':
            return

        # value is None or ''
        for row in df.values:
            if row[0] is None or '' == str(row[0]).strip():
                log.error(f"row title format check error")
                raise BaseException()

            for i in range(1, len(row)):
                float(row[i])
                if row[i] is None or '' == str(row[i]).strip():
                    log.error(f"row {i} format check error")
                    raise BaseException()

        if 'id' in data:
            duplicated_list = df.duplicated('id', False).tolist()
            if True in duplicated_list:
                log.error(f"id duplicated, check csv file")
                raise BaseException()
        if 'id\r' in data:
            duplicated_list = df.duplicated('id\r', False).tolist()
            if True in duplicated_list:
                log.error(f"idr duplicated, check csv file")
                raise BaseException()

    except BaseException as be:
        log.error(f"check_csv_format error, {be}")
        # raise PpcException(PpcErrorCode.DATASET_CSV_ERROR.get_code(),
        #                    PpcErrorCode.DATASET_CSV_ERROR.get_msg())
    return


def handle_local_dataset(file_path):
    # if not utils.file_exists(file_path):
    #     raise PpcException(PpcErrorCode.DATASET_NOT_FOUND.get_code(), PpcErrorCode.DATASET_NOT_FOUND.get_msg())

    size = os.path.getsize(file_path)

    df = pd.read_csv(file_path, index_col=False)
    (row, col) = df.shape
    check_csv_format(df)
    data = df.head(DEFAULT_DATASET_RECORD_COUNT)
    data_field = str(data.columns.values).replace("'", "").replace("\\r", "")
    # version_hash = utils.make_hash_from_file_path(file_path, CryptoType[config.CONFIG_DATA['CRYPTO_TYPE']])

    # return row, col, size, data_field, version_hash
    return row, col, size, data_field


def check_csv_format2(file_name):

    try:
        with open(file_name) as f:
            
            columns = next(f)
            columns_list = columns.strip().split(',')

            if columns_list[0] == 'Placeholder':
                return 0, 0, '[]'

            col = len(columns_list)
            data_field = '[' + columns.strip().replace("'", "").replace("\\r", "").replace(",", " ") + ']'

            row = 0
            id_idx = columns_list.index('id')
            idx_list = []
            for line in f:

                line_list = line.strip().split(',')
                if line_list[0] is None or line_list[0].strip() == '':
                    log.error(f"row title format check error")
                    raise BaseException()

                assert len(line_list) == col

                # np.array(line_list[1:], dtype=float)
                list(map(float, line_list[1:]))
                # None 在 map 就会报错，可以不运行下面的代码
                # if None in line_list[1:]:
                #     log.error(f"row {row} format check error")
                #     raise BaseException()
                
                row += 1
                idx_list.append(line_list[id_idx])

            if 'id' in columns_list:
                if len(set(idx_list)) != len(idx_list):
                    log.error(f"id duplicated, check csv file")
                    raise BaseException()

        return row, col, data_field

    except BaseException as be:
        log.error(f"check_csv_format error, {be}")
        # raise PpcException(PpcErrorCode.DATASET_CSV_ERROR.get_code(),
        #                    PpcErrorCode.DATASET_CSV_ERROR.get_msg())
    
    return


def handle_local_dataset2(file_path):

    size = os.path.getsize(file_path)
    row, col, data_field = check_csv_format2(file_path)

    return row, col, size, data_field


def add_dataset_by_local2(file_path):
# def add_dataset_by_local(file_path, dataset_id, agency_id, agency_name, data_field, dataset_description, 
#                          dataset_size, row_count, column_count, dataset_title, user_name, version_hash):
    # dataset_metadata = make_dataset_metadata(data_field, dataset_description, dataset_size, row_count, column_count,
    #                                          version_hash, user_name)
    try:
        # iss_client.send_iss_data_post(dataset_id, dataset_title, agency_id, agency_name, dataset_metadata)
        # hdfs_client.upload_file(file_path, user_name + os.sep + dataset_id)
        # raw_data = utils.read_content_from_file_by_binary(file_path)
        # log.info(f"add_dataset_by_local raw_data:{raw_data}")
        # df = utils.make_dataframe(str(raw_data, 'utf8'))
        # log.info(f"add_dataset_by_local df:{df}")
        # data_detail = utils.df_to_dict(df.head(utils.DEFAULT_DATASET_RECORD_COUNT))
        data_detail = pd.read_csv(file_path, index_col=False, nrows=DEFAULT_DATASET_RECORD_COUNT)
        # job_database_service.save_dataset_preview(dataset_id, data_detail)
    except BaseException as e:
        log.warn(f"add_dataset_by_local warn: {e}")
        # raise PpcException(PpcErrorCode.DATASET_UPLOAD_ERROR.get_code(), PpcErrorCode.DATASET_UPLOAD_ERROR.get_msg())
    return data_detail


if __name__=="__main__":

    # 提供2组数据测试
    # 1000w * 3 (id: 10M, data: 20M)
    file_path1 = 'D:/Github/CodePractice/code_wb/datasets/xinyi_table_0.csv'
    # 50w * 301 (id: 0.5M, data: 150M)
    file_path2 = 'D:/Github/CodePractice/code_wb/datasets/epsilon_hetero_P1.csv'

    file_path = file_path2

    # 原方案，handle_local_dataset
    # file_path1：21.6s (read_csv：4.2s, check_csv_format：17.4s) (CPU: 100%, 内存: 2662M)
    # file_path2：74.9s (read_csv：10.3s, check_csv_format：64.6s) (CPU: 100%, 内存: 3582M)
    row, col, size, data_field = handle_local_dataset(file_path)

    # 新方案，handle_local_dataset2
    # file_path1：10.6s (CPU: 106%, 内存: 1472M)
    # file_path2：21.03s (CPU: 101%, 内存: 108M)
    row, col, size, data_field = handle_local_dataset2(file_path)

    print(row, col, size, data_field)

    # 原方案，add_dataset_by_local（file_path2，内存 10G+, 任务杀掉了）
    # 新方案，add_dataset_by_local2（file_path2，耗时 1.23s, 内存 50M, CPU 226%）
    data_detail = add_dataset_by_local2(file_path)

    print(data_detail)
