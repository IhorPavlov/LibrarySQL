from Library.library import Library
from socket import socket
from msgutils import recv_msg, send_msg, default_encoding
from Library.utils import logprint
from threading import Thread
from Library.utils.inputs import input_numeric
import time


welcome_msg = 'What do you want?\n'\
                        '1 - show all books in the library\n'\
                        '2 - show available books in the library\n'\
                        '3 - show all readers in the library\n'\
                        '4 - give book\n'\
                        '5 - return book\n'\
                        '6 - add book to library\n'\
                        '7 - remove book from library\n'\
                        '8 - register reader\n'\
                        '9 - remove reader from library\n'\
                        '0 - exit\n'\
                        'make your choice: '

class ClientHandler(Thread):
    def __init__(self, conn: socket, lib: Library):
        super(ClientHandler, self).__init__()
        self.__connection = conn
        self.__lib = lib

    def run(self) -> None:
        send_msg(welcome_msg.encode(default_encoding), self.__connection)
        start = time.time()
        while True:
            answer = recv_msg(self.__connection)
            if not answer:
                logprint.print_fail(f'No answer!, time {time.time() - start}')
                break

            answer = answer.decode(default_encoding)

            if not answer.isnumeric() or int(answer) < 0 or int(answer) > 9:
                logprint.print_fail(f'Invalid input!, time {time.time() - start}')
                break

            answer = int(answer)

            # 1 - show all books in the library
            if answer == 1:
                # sleep(5)
                start = time.time()
                ret = self.__lib.get_all_books()
                retStr = '\n'.join(map(str, ret))
                send_msg((retStr + '\n\n' + welcome_msg).encode(default_encoding), self.__connection)
                logprint.print_warning(f'time "show all books" {time.time() - start}')

            # 2 - show all available books in the library
            if answer == 2:
                start = time.time()
                ret = self.__lib.get_available_books()
                retStr = '\n'.join(map(str, ret))
                send_msg((retStr + '\n\n' + welcome_msg).encode(default_encoding), self.__connection)
                logprint.print_warning(f'time "show available books" {time.time() - start}')

            # 3 - show all readers in the library
            if answer == 3:
                start = time.time()
                ret = self.__lib.get_all_readers()
                retStr = '\n'.join(map(str, ret))
                send_msg((retStr + '\n\n' + welcome_msg).encode(default_encoding), self.__connection)
                logprint.print_warning(f'time "show all readers" {time.time() - start}')

             # 4 - give book
            if answer == 4:
                start = time.time()
                id_book = self.custom_input('Enter id book: ', is_numeric=True)
                if not id_book:
                    logprint.print_fail('No answer')
                    break

                id_reader = self.custom_input('Enter id reader: ', is_numeric=True)
                if not id_reader:
                    logprint.print_fail('No answer')
                    break

                _, retStr = self.__lib.book_for_reader(id_book, id_reader)  #retStr записывает в себя результат ф-ии: сообщение, что такая-то книга выдана либо её нету, "_" забирает тру фолс из результата функции?
                send_msg((retStr + '\n\n' + welcome_msg).encode(default_encoding), self.__connection)
                logprint.print_warning(f'time "give book" {time.time() - start}')

            # 5 - return book
            if answer == 5:
                start = time.time()
                id_book = self.custom_input('Enter id book: ', is_numeric=True)
                if not id_book:
                    logprint.print_fail('No answer')
                    break

                id_reader = self.custom_input('Enter id reader: ', is_numeric=True)
                if not id_reader:
                    logprint.print_fail('No answer')
                    break

                _, retStr = self.__lib.return_to_library(id_book, id_reader)
                send_msg((retStr + '\n\n' + welcome_msg).encode(default_encoding), self.__connection)
                logprint.print_warning(f'time "return book" {time.time() - start}')

            # 6 - add book to library
            if answer == 6:
                start = time.time()
                name = self.custom_input('Enter book\'s name: ')
                if not name:
                    logprint.print_fail('No answer')
                    break

                author = self.custom_input('Enter book\'s author: ')
                if not author:
                    logprint.print_fail('No answer')
                    break

                year = self.custom_input('Enter book\'s year: ', is_numeric=True)
                if not year:
                    logprint.print_fail('No answer')
                    break

                _, retStr = self.__lib.add_book(name, author, year)
                send_msg((retStr + '\n\n' + welcome_msg).encode(default_encoding), self.__connection)
                logprint.print_warning(f'time "add book" {time.time() - start}')

            # 7 - remove book from library
            if answer == 7:
                start = time.time()
                book_id = self.custom_input('Enter book id: ', is_numeric=True)
                if not book_id:
                    logprint.print_fail('No answer')
                    break

                _, retStr = self.__lib.remove_book(book_id)
                send_msg((retStr + '\n\n' + welcome_msg).encode(default_encoding), self.__connection)
                logprint.print_warning(f'time "remove book" {time.time() - start}')

            # 8 - register reader
            if answer == 8:
                start = time.time()
                name = self.custom_input('Enter reader\'s name: ')
                if not name:
                    logprint.print_fail('No answer')
                    break

                surname = self.custom_input('Enter reader\'s surname: ')
                if not surname:
                    logprint.print_fail('No answer')
                    break

                year = self.custom_input(f'Enter {name}\'s year of birth: ', is_numeric=True)
                if not year:
                    logprint.print_fail('No answer')
                    break

                _, retStr = self.__lib.add_reader(name, surname, year)
                send_msg((retStr + '\n\n' + welcome_msg).encode(default_encoding), self.__connection)
                logprint.print_warning(f'time "register reader" {time.time() - start}')

            # 9 - remove reader from library
            if answer == 9:
                start = time.time()
                reader_id = self.custom_input('Enter reader id: ', is_numeric=True)
                if not reader_id:
                    logprint.print_fail('No answer')
                    break

                _, retStr = self.__lib.remove_reader(reader_id)
                send_msg((retStr + '\n\n' + welcome_msg).encode(default_encoding), self.__connection)
                logprint.print_warning(f'time "remove reader" {time.time() - start}')

            # 0 - exit
            if answer == 0:
                start = time.time()
                logprint.print_done(f'The client {self.__connection} disconnected')
                logprint.print_warning(f'time {time.time() - start}')
                exit(0)

        self.__connection.close()

    def custom_input(self, msg: str, is_numeric: bool = False):
        '''пользовательский ввод с защитой от некорректного ввода'''
        send_msg(msg.encode(default_encoding), self.__connection)

        while True:
            ans = recv_msg(self.__connection)
            if ans is False:
                return False
            ans = ans.decode(default_encoding)
            if is_numeric and ans.isnumeric():
                return int(ans)
            elif not is_numeric and ans:
                return ans
            else:
                err_msg = 'Invalid input\n' + msg
                send_msg(err_msg.encode(default_encoding), self.__connection)