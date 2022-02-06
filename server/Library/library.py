from .library_units.book import Book
from .library_units.people import People
from .storages.istorage import IStorage
from .utils import logprint
from typing import Union
from threading import Lock


class Library:
    def __init__(self, storage: IStorage, list_Books: list = None, list_People: list = None):  #
        self.__storage = storage
        self.__list_Books = list_Books if list_Books else []
        self.__list_People = list_People if list_People else []
        self.__lock = Lock()

    def __str__(self):
        return f'{self}'

    def add_book(self, name: str, author: str, year: int = None, book_id: int = None) -> (bool, str):
        """добавляет книгу в библиотеку и перезаписывает JSON-файл полным списком книг"""
        with self.__lock:
            if book_id is not None:
                for book in self.__list_Books:
                    if int(book.get_id()) == book_id:
                        return logprint.print_fail(f'книга под под номером {book_id} уже существует')
            # self.__list_Books.append(Book(name, author, year, book_id))
            self.__storage.add_book(name, author, year, book_id)
            # self.save_all_books()
            return_msg = f'книга {name} успешно добавлена в библиотеку'
        logprint.print_done(return_msg)
        return True, return_msg

    def remove_book(self, book_id: int) -> (bool, str):
        """удаляет книгу из библиотеки"""
        with self.__lock:
            if book_id is not None:
                for book in self.__list_Books:
                    if int(book.get_id()) == book_id:
                        # self.__list_Books.remove(self.__get_book_by_id(book_id))
                        self.__storage.remove_book(book_id)
                        return_msg = f'Книга № {book.get_id()} ({book.get_name()}, {book.get_author()}) удалена из библиотеки'
                        logprint.print_done(return_msg)
                        # self.save_all_books()
                        return True, return_msg

            return_msg = f'Ошибка ввода или такой книги нет в библиотеке'
        logprint.print_fail(return_msg)
        return False, return_msg

    def __get_book_by_id(self, book_id: int) -> Union[Book, None]:
        """
        Функция получения книги по id из списка книг

        :param book_id: id книги, которую хотим получить
        :return: obj Book (если книга есть в библиотеке); None (если книги нет)
        """
        for book in self.__list_Books:
            if int(book.get_id()) == book_id:
                return book
        return None

    def get_all_books(self) -> list:
        # self.load_books()
        # for book in self.__list_Books:
        #     print('reader_id_', book.get_reader_id())
        if self.load_books() is True:
            return self.__list_Books

    def get_available_books(self) -> list:
        # return self.__list_Books

        # for book in self.__list_Books:
        #     if not book.get_reader_id():
        #         print(book)
        available_books = []
        if self.load_books() is True:
            for book in self.__list_Books:
                if book.get_reader_id() == 'None':
                    available_books.append(book)

        return available_books

    # def get_sorted_book_by_id(self):
    #     print('List Books:')
    #     self.print_sorted_book('id')

    def print_sorted_book(self, sort: str = 'id', reverse: bool = False):
        if sort not in ['id', 'name', 'author', 'year']:
            print(f'Error: no sorting by {sort} field')
            return

        def get_sort_field(book: Book):
            if sort == 'id':
                return book.get_id()
            elif sort == 'name':
                return book.get_name()
            elif sort == 'author':
                return book.get_author()
            elif sort == 'year':
                return book.get_year()

        for book in sorted(self.__list_Books, key=get_sort_field, reverse=reverse):
            print(book)

    def add_reader(self, name: str, surname: str, year: int = None, reader_id: int = None) -> (bool, str):
        '''добавляет нового читателя в список читателей. '''
        with self.__lock:
            # print(reader_id)
            if reader_id is not None:
                for reader in self.__list_People:
                    if int(reader.get_id()) == reader_id:
                        return_msg = f'читатель {name} c номером {reader_id} уже зарегистрирован в этой библиотеке'
                        logprint.print_done(return_msg)
                        return True, return_msg
            # self.__list_People.append(People(name, surname, year, reader_id))
            self.__storage.add_reader(name, surname, year, reader_id)
            # self.save_all_readers()
            return_msg = f'читатель {name} {surname} успешно зарегистрирован в библиотеке' #под номером {reader_id}
        logprint.print_done(return_msg)
        return True, return_msg

    def __get_reader_by_id(self, reader_id: int) -> Union[People, None]:
        """
        Функция получения читателя по id из списка читателей

        :param reader_id: id читателя, которого хотим получить
        :return: obj Book (зарегистрирован ли читатель в библиотеке); None (если не зарегистрирован)
        """
        for reader in self.__list_People:
            if int(reader.get_id()) == reader_id:
                return reader
        return None

    def remove_reader(self, reader_id: int) -> (bool, str):
        #добавить возможность удалять по имени и фамилии
        with self.__lock:
            if reader_id is not None:
                for reader in self.__list_People:
                    if int(reader.get_id()) == reader_id:
                        # self.__list_People.remove(self.__get_reader_by_id(reader_id))
                        self.__storage.remove_reader(reader_id)
                        return_msg = f'Карточка читателя {reader.get_name()} {reader.get_surname()} (№{reader.get_id()}) удалена из библиотеки'
                        logprint.print_done(return_msg)
                        return True, return_msg
            # self.save_all_readers()
            return_msg = f'Ошибка ввода или такой читатель не зарегистрирован в библиотеке'
            logprint.print_done(return_msg)
        return True, return_msg

    def get_all_readers(self):
        # self.load_readers()
        if self.load_readers() is True:
            return self.__list_People

    def book_for_reader(self, book_id: int, reader_id: int) -> (bool, str):
        return_msg = ''
        with self.__lock:
            # print(book_id)
            book = self.__get_book_by_id(book_id)
            # print(book, type(book))
            if not book:
                return_msg = f'Error: книга с номером {book_id} не в библиотеке'
                logprint.print_fail(return_msg)
                return False, return_msg
            reader = self.__get_reader_by_id(reader_id)
            if not reader:
                return_msg = f'Error: Читателя с номером {reader_id} нет в библиотеке'
                logprint.print_fail(return_msg)
                return False, return_msg
            if Book.get_reader_id(book) != 'None':
                return_msg = f'Error: Книги под номером {book_id} нету в библиотеке'
                logprint.print_fail(return_msg)
                return False, return_msg
            book.set_reader_id(reader_id)
            self.__storage.update_book(book_id, reader_id) #применить при переходе на SQL
            # self.save_all_books()

        return_msg = f'Книга {book.get_name()} (c/н {book_id}) выдана читателю {reader.get_name()} (номер {reader_id})'
        logprint.print_done(return_msg)

        return True, return_msg
        #применить при переходе на SQL
        #self.__storage.update_book(book)

    def return_to_library(self, book_id: int, reader_id: int) -> (bool, str):

        with self.__lock:
            book = self.__get_book_by_id(book_id)
            if not book:
                return_msg = f'Error: книги с номером {book_id} нет в библиотеке'
                logprint.print_fail(return_msg)
                return False, return_msg
            reader = self.__get_reader_by_id(reader_id)
            if not reader:
                return_msg = f'Error: читателя с номером {reader_id} нет в библиотеке'
                logprint.print_fail(return_msg)
                return False, return_msg
            if book.get_reader_id() != reader.get_id():
                reader_2 = self.__get_reader_by_id(book.get_reader_id())
                return_msg = f'Error: {reader.get_name()} не может вернуть книгу {book_id}, книга выдана {reader_2.get_name()} ({book.get_reader_id()})'
                logprint.print_fail(return_msg)
                return False, return_msg
            book.set_reader_id(None)
            self.__storage.return_book(book_id, None)

        return_msg = f'Читатель {reader.get_name()} вернул книгу "{book.get_name()}" в библиотеку'
        logprint.print_done(return_msg)

        return True, return_msg

    def load_books(self) -> bool:
        self.__list_Books = self.__storage.load_books()
        if len(self.__list_Books):
            return True
        return False

    def load_books_from_txt_file(self, filename: str,
                                 sep: str = '$!$',
                                 encoding: str = 'utf-8') -> bool:
        self.__list_Books = self.__storage.load_books_from_txt_file(filename, sep, encoding)
        if not len(self.__list_Books):
            logprint.print_fail(f'error load books from \'{filename}\'')
            return False

        self.save_all_books()
        return True

    def load_readers(self) -> bool:

        self.__list_People = self.__storage.load_readers()
        if len(self.__list_People):
            return True
        return False

    def load_readers_from_txt_file(self, filename: str,
                                   sep: str = ',',
                                   encoding: str = 'utf-8') -> bool:
        self.__list_People = self.__storage.load_readers_from_txt_file(filename, sep, encoding)
        if not len(self.__list_People):
            logprint.print_fail(f'error load readers from {filename}')
            return False

        self.save_all_readers()
        return True

    def save_all_books(self):
        self.__storage.save_books(self.__list_Books)

    def save_all_readers(self):
        self.__storage.save_readers(self.__list_People)









