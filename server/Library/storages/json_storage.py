from .istorage import IStorage
from Library.library_units.book import Book
from Library.library_units.people import People
import os
import json
from Library.utils import logprint


class JSONStorage(IStorage):
    def __init__(self, db_books_filename, db_people_filename):
        self.__db_books_filename = db_books_filename
        self.__db_people_filename = db_people_filename

    def load_books(self) -> list:
        if not os.path.exists(self.__db_books_filename):
            logprint.print_warning('JSON books database doesn\'t exist yet')
            return []
        with open(self.__db_books_filename) as f:
            dict_books = json.load(f)
        return [Book.from_dict(book)for book in dict_books]

    def load_readers(self) -> list:
        if not os.path.exists(self.__db_people_filename):
            logprint.print_warning('JSON people database doesn\'t exist yet')
            return []
        with open(self.__db_people_filename) as f:
            dict_people = json.load(f)
        return [People.from_dict(reader) for reader in dict_people]

    def save_books(self, list_Books: list):
        with open(self.__db_books_filename, 'w') as f:
            json.dump([book.to_dict() for book in list_Books], f)

    def save_readers(self, list_People: list):
        with open(self.__db_people_filename, 'w') as f:
            json.dump([reader.to_dict() for reader in list_People], f)

