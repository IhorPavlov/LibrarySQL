from Library.storages.orm_storage import ORMStorage
from client_handler import ClientHandler
from Library.library import Library
from socket import socket



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

    ip = '127.0.0.1'
    port = 12347

    storage = ORMStorage()

    lib = Library(storage)

    if not lib.load_books():
        lib.load_books_from_txt_file('./Library/init_data/books.txt', sep='$!$')

    if not lib.load_readers():
        lib.load_readers_from_txt_file('./Library/init_data/readers.txt')

    start_server(ip, port, lib)