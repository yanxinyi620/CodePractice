import enum
import logging
import uuid
import json
import requests

from requests_toolbelt import MultipartEncoder
from tenacity import retry, stop_after_delay, wait_random


logger = logging.getLogger()
logger.setLevel(logging.INFO)

COMPUTATION_PATH_PREFIX = '/testModule'


class ComputationUri(enum.Enum):
    API = f'{COMPUTATION_PATH_PREFIX}/post_test1'


def make_uuid(prefix):
    return prefix + str(uuid.uuid4()).replace("-", "")


@retry(stop=(stop_after_delay(5)), wait=wait_random(min=0, max=5), reraise=True)
def upload_post_input(computation_gate_way_url, name, age):
    upload_dataset_data = {
        "name": name,
        "age": age,
    }

    multipart_encoder = MultipartEncoder(upload_dataset_data)
    headers = {'Content-Type': multipart_encoder.content_type}

    url = f'http://{computation_gate_way_url}{ComputationUri.API.value}'
    response = requests.post(url=url, headers=headers, data=multipart_encoder)
    response = json.loads(response.text)
    if 'return_code' not in response or response['return_code'] != '200':
        logger.error(f"computation {computation_gate_way_url} error, , {response}")
        raise Exception('error!')
    
    return response


response = upload_post_input('127.0.0.1:5001', 'xinyi', '18')
