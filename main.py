import struct
import socket

local_host = '127.0.0.1'
local_port = 53

remote_host = '192.168.0.1'
remote_port = 53


def parser_request(data: bytes):
    header = data[:12]
    payload = data[12:]

    (
        id_request,  # ID запроса
        flags, # Флаги
        num_queries, # Количество запросов
        num_answers, # Количество ответов
        num_authority, # Количество серверов которые ответили
        num_additional # Количество дополнительных байт
    ) = struct.unpack(">6H", header)

    queries = []
    for i in range(num_queries):
        res = payload.index(0) + 5
        queries.append(payload[:res])
        payload = payload[res:]

    return id_request, queries

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        server.bind((local_host, local_port))
    except:
        print("[!!] Failed to listen on %s:%d" % (local_host, local_port))
        print("[!!] Check for other listening sockets or correct permissions.")
    print("[*] Listening on %s:%d" % (local_host, local_port))
    while True:
        data, addres = server.recvfrom(512)
        id_request, queries = parser_request(data)
        print(id_request)
        print(queries)
        remote_socket.sendto(data, (remote_host, remote_port))
        data_rev, addres_rev = remote_socket.recvfrom(512)
        server.sendto(data_rev, addres)
        print(data_rev)
if __name__ == '__main__':
    main()
