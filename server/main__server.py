from Library.storages.json_storage import JSONStorage
# from threading import Thread
# from LibraryITEA.utils.inputs import input_numeric
from client_handler import ClientHandler
from Library.library import Library
from socket import socket
from Library.utils import logprint
import concurrent.futures as cf
# import asyncio
import sqlalchemy
from Library.storages.sql_storage import SQLStorage



def start_server(ip: str, port: int, lib: Library):
    with socket() as sock:
        sock.bind((ip, port))
        sock.listen(5)

        while True:
            conn, _ = sock.accept()
            print(f'connected: {_}')
            client = ClientHandler(conn, lib)
            client.start()

if __name__ == '__main__':
    with cf.ProcessPoolExecutor(max_workers=None) as ex:
        ip = '127.0.0.1'
        port = 12347

        storage = SQLStorage('db_books.db', 'db_readers.db')
        # storage = JSONStorage('db_books.db', 'db_readers.db')

        lib = Library(storage)
        if not lib.load_books():
            lib.load_books_from_txt_file('./LibraryITEA/init_data/books.txt', sep='$!$')

        if not lib.load_readers():
            lib.load_readers_from_txt_file('./LibraryITEA/init_data/readers.txt')

        # print(lib.get_all_books())
        # print(lib.get_all_readers())


        start_server(ip, port, lib)