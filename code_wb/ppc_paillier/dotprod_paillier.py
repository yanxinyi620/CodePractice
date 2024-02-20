#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  lr_paillier.py
@Time    :  2023/04/19 20:00:14
@Author  :  yanxinyi
@Version :  v1.0
@Contact :  yanxinyi620@163.com
@Desc    :  paillier test
'''

import time
import numpy as np

from phe import paillier
from phe import EncodedNumber


def paillier_pk(ring=None, legth=3072):
    public_key, private_key = paillier.generate_paillier_keypair(ring, legth)
    return public_key, private_key


def paillier_encrypt(arr, public_key):
    res = []
    for i in arr:
        encrypted_i = public_key.encrypt(i)
        res.append(encrypted_i)
    return np.array(res)


def paillier_arrdot(w, X, public_key):
    res = []
    for sample in X:
        encrypted_sample = paillier_encrypt(sample, public_key)
        arrdot = sum(w * encrypted_sample)
        res.append(arrdot)
    return np.array(res)


def paillier_encrypt_X(X, public_key):
    encrypted_X = []
    for sample in X:
        encrypted_sample = paillier_encrypt(sample, public_key)
        encrypted_X.append(encrypted_sample)
    return np.array(encrypted_X)


def paillier_Xdot(w, encrypted_X):
    res = []
    for encrypted_sample in encrypted_X:
        arrdot = sum(w * encrypted_sample)
        res.append(arrdot)
    return np.array(res)


def paillier_decrypt(encrypted_arr, private_key):
    res = []
    for encrypted_value in encrypted_arr:
        value = private_key.decrypt(encrypted_value)
        res.append(value)
    return np.array(res)


if __name__ == '__main__':

    '''
    密钥bits长度: 2048
    feature_num * N, 100维*100数据, 加密69s, 预测2.6s, 解密0.2s
    耗时公式：
        加密: 6.9ms * feature_num * N (万次加密 69s)
        计算: 0.26ms * feature_num * N (万次数乘+加法 2.6s)
        解密: 2.0ms * N (百次解密 0.2s)
    '''

    feature_num = 100
    N = 100
    print(f'feature_num: {feature_num}, N: {N}.')

    np.random.seed(100)
    w = (np.random.rand(feature_num) - 0.4) * 3
    X = np.random.rand(N, feature_num) * 3

    public_key, private_key = paillier_pk(None, 2048)

    # start_time = time.time()
    # encrypted_G = paillier_arrdot(w, X, public_key)
    # end_time = time.time()
    # time_costs = end_time - start_time

    # G = paillier_decrypt(encrypted_G, private_key)
    # print(f'time_costs: {"%.4f" % time_costs}, G: {G[:5]}.')

    start_time = time.time()
    encrypted_X = paillier_encrypt_X(X, public_key)
    end_time = time.time()
    encrypt_costs = end_time - start_time

    start_time = time.time()
    encrypted_G = paillier_Xdot(w, encrypted_X)
    end_time = time.time()
    Xdot_costs = end_time - start_time

    start_time = time.time()
    G = paillier_decrypt(encrypted_G, private_key)
    end_time = time.time()
    decrypt_costs = end_time - start_time

    G_true = np.dot(w, X.T)
    print(f'encrypt_costs: {"%.4f" % encrypt_costs}, '
          f'Xdot_costs: {"%.4f" % Xdot_costs}, '
          f'decrypt_costs: {"%.4f" % decrypt_costs}.'
          f'\nG_pail: {G[:5]}.\nG_true: {G_true[:5]}.')


    # test -------------------------------------------
    print(f'\ntest ciphertext and raw_decrypt')
    value = 2.6546
    encrypted = public_key.encrypt(value)
    ciphertext = encrypted.ciphertext(be_secure=False)
    exponent = encrypted.exponent
    print(exponent, ciphertext)

    encoded = private_key.raw_decrypt(ciphertext)
    decrypted = EncodedNumber(public_key, encoded, exponent).decode()
    # decrypted = private_key.decrypt(encrypted)
    print(value, decrypted)

