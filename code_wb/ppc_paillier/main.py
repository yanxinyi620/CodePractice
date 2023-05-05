from datetime import datetime
from phe import paillier

if __name__ == '__main__':
    # Generate two random plaintexts
    enc_total = 0
    add_total = 0
    dec_total = 0
    # Generate a Paillier keypair
    public_key, private_key = paillier.generate_paillier_keypair(None, 2048)

    plaintext1 = 1234
    plaintext2 = 5678

    # 加密两个数
    start_time = datetime.now()
    encrypted1 = public_key.encrypt(plaintext1)
    encrypted2 = public_key.encrypt(plaintext2)
    end_time = datetime.now()
    enc_cost = (end_time - start_time).total_seconds() * 1000
    print("加密两个数耗时: ", enc_cost, "ms")

    # 同态加密加法
    start_time = datetime.now()
    encrypted_sum = encrypted1 + encrypted2
    end_time = datetime.now()
    add_cost = (end_time - start_time).total_seconds() * 1000
    print("同态加密加法耗时: ", add_cost , "ms")

    # 同态明文乘法
    start_time = datetime.now()
    encrypted_sum = 2 * encrypted_sum
    end_time = datetime.now()
    add_cost = (end_time - start_time).total_seconds() * 1000
    print("同态密文乘法耗时: ", add_cost, "ms")

    # 同态明文加法
    start_time = datetime.now()
    encrypted_sum = 5 + encrypted_sum
    end_time = datetime.now()
    add_cost = (end_time - start_time).total_seconds() * 1000
    print("同态明文加法耗时: ", add_cost, "ms")


    # 解密结果
    start_time = datetime.now()
    result = private_key.decrypt(encrypted_sum)
    print("解密结果2 * （{} + {}） + 5 = {} ".format(plaintext1, plaintext2, result))
    end_time = datetime.now()
    dec_cost = (end_time - start_time).total_seconds() * 1000
    print("解密结果耗时: ", dec_cost , "ms")

