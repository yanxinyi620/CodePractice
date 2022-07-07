import enum
import logging
import uuid
import json
import requests

from requests_toolbelt import MultipartEncoder
from tenacity import retry, stop_after_delay, wait_random


logger = logging.getLogger()
logger.setLevel(logging.INFO)

COMPUTATION_PATH_PREFIX = '/api/v3/ppc-computation/pcs'


class ComputationUri(enum.Enum):
    XGB_API = f'{COMPUTATION_PATH_PREFIX}/xgb-active-data'
    XGB_XBIN_API = f'{COMPUTATION_PATH_PREFIX}/xgb-x-bin-data'
    XGB_HIST_API = f'{COMPUTATION_PATH_PREFIX}/xgb-hist-data'
    XGB_INSTANCE_API = f'{COMPUTATION_PATH_PREFIX}/xgb-instance-data'


def make_uuid(prefix):
    return prefix + str(uuid.uuid4()).replace("-", "")


@retry(stop=(stop_after_delay(5)), wait=wait_random(min=0, max=5), reraise=True)
def upload_xgb_gh_input(computation_gate_way_url, job_id, loading_index,
                        round_ID, index_path, glist_path, hlist_path):
    file_name = make_uuid("tmp")
    upload_dataset_data = {
        "jobId": job_id,
        "loadingIndex": str(loading_index),
        "round": str(round_ID),
        'indexList': (file_name, open(index_path, 'rb'), 'text/plain'),
        'gData': (file_name, open(glist_path, 'rb'), 'text/plain'),
        'hData': (file_name, open(hlist_path, 'rb'), 'text/plain'),
    }

    multipart_encoder = MultipartEncoder(upload_dataset_data)
    headers = {'Content-Type': multipart_encoder.content_type}

    url = f'http://{computation_gate_way_url}{ComputationUri.XGB_API.value}'
    response = requests.post(url=url, headers=headers, data=multipart_encoder)
    # response = json.loads(response.text)
    
    return response


@retry(stop=(stop_after_delay(5)), wait=wait_random(min=0, max=5), reraise=True)
def upload_xgb_ins_input(computation_gate_way_url, job_id, loading_index, dataset_id, 
                         learning_id, round_ID, iterate_ID, max_k, max_v, instance_path):
    file_name = make_uuid("tmp")
    upload_dataset_data = {
        "jobId": job_id,
        "loadingIndex": str(loading_index),
        "dataset": str(dataset_id),
        "learning": str(learning_id),
        "round": str(round_ID),
        "iterate": str(iterate_ID),
        "maxk": str(max_k),
        "maxv": str(max_v),
        'instance': (file_name, open(instance_path, 'rb'), 'text/plain'),
    }

    multipart_encoder = MultipartEncoder(upload_dataset_data)
    headers = {'Content-Type': multipart_encoder.content_type}

    url = f'http://{computation_gate_way_url}{ComputationUri.XGB_INSTANCE_API.value}'
    response = requests.post(url=url, headers=headers, data=multipart_encoder)

    return response


if 'gh':
    path_prefix = 'c:/Users/yanxi/Documents/GitHub/Ppc-XGB/ppc_xgboost/datasets/tmp/'
    used_index_prefix = path_prefix + 'used_index'
    glist_file_prefix = path_prefix + 'g_list'
    hlist_file_prefix = path_prefix + 'h_list'

    tree_id = 0

    used_index_filename = used_index_prefix + '_' + str(tree_id) + '.npy'
    used_glist_filename = glist_file_prefix + '_' + str(tree_id) + '_p'
    used_hlist_filename = hlist_file_prefix + '_' + str(tree_id) + '_p'

    used_glist_filename_p0 = used_glist_filename + '0.data'
    used_glist_filename_p1 = used_glist_filename + '1.data'
    used_hlist_filename_p0 = used_hlist_filename + '0.data'
    used_hlist_filename_p1 = used_hlist_filename + '1.data'

    response = upload_xgb_gh_input('127.0.0.1:5850', '1', '2', tree_id, used_index_filename, 
                                   used_glist_filename_p0, used_hlist_filename_p0)


if 'ins':
    path_prefix = 'c:/Users/yanxi/Documents/GitHub/Ppc-XGB/ppc_xgboost/datasets/'
    instance_prefix = path_prefix + 'instance'

    tree_id = '0'
    leaf_num = '0'

    instance_filename = instance_prefix + '_0_0.csv'

    upload_xgb_ins_input('127.0.0.1:5850', '1', '2', '-1', '-1', tree_id, leaf_num, 
                         '0', '0', instance_filename)


