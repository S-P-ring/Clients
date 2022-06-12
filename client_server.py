import socket
import json
import functools


def result(data):
    method = data["method"]
    params = data["params"]
    if len(params) == 1:
        param = params[0]
    else:
        param1, param2 = params[0], params[1]
    if method == "fib":
        result = fibonacci(param)
    elif method == "fac":
        result = factorial(param)
    elif method == "sum":
        result = summ(param1, param2)
    else:
        result = subtraction(param1, param2)
    return result


def decode_json(data):
    decode_data = json.loads(data)
    return decode_data


def encode_json(data):
    encode_data = json.dumps(data)
    return encode_data


def answer(decode_data, my_result):
    del decode_data["method"]
    del decode_data["params"]
    decode_data["result"] = my_result
    return decode_data


@functools.lru_cache(maxsize=None)
def fibonacci(param):
    if param < 3:
        return param
    else:
        return fibonacci(param - 1) + fibonacci(param - 2)


def factorial(param):
    if param == 0:
        return 1
    return factorial(param - 1) * param


def summ(param1, param2):
    return param1 + param2


def subtraction(param1, param2):
    return param1 - param2


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('185.65.244.210', 12345))

while True:
    data = client_socket.recv(2048)
    decode_data = decode_json(data)
    my_result = result(decode_data)
    my_answer = answer(decode_data, my_result)
    encode_data = encode_json(my_answer)
    client_socket.sendall(bytes(encode_data, encoding='utf-8')
