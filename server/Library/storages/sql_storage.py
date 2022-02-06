from Library.storages.istorage import IStorage
from Library.library_units.book import Book
from Library.library_units.people import People
from Library.utils import logprint
import sqlalchemy
from sqlalchemy import Column, Integer, Text, ForeignKey

class SQLStorage(IStorage):
    def __init__(self, db_books_filename, db_people_filename):
        self.__db_books_filename = db_books_filename
        self.__db_people_filename = db_people_filename
        self.__engine = sqlalchemy.create_engine('postgresql://postgres:123@localhost:5432/postgres')

        meta_data = sqlalchemy.MetaData()

        self.__db_books_filename = sqlalchemy.Table('books', meta_data,
                                                    Column('id', Integer, primary_key=True),
                                                    Column('name', Text, nullable=False),
                                                    Column('author', Text, nullable=False),
                                                    Column('year', Integer, nullable=False),
                                                    Column('reader_id', Integer, ForeignKey('readers.id'), nullable=True))

        self.__db_people_filename = sqlalchemy.Table('readers', meta_data,
                                                     Column('id', Integer, primary_key=True),
                                                     Column('name', Text, nullable=False),
                                                     Column('surname', Text, nullable=False),
                                                     Column('year', Integer, nullable=False))

        # engine = sqlalchemy.create_engine('postgresql://postgres:123@localhost:5432/postgres')
        meta_data.create_all(self.__engine)
        logprint.print_done('The table \"books\" is created')
        logprint.print_done('The table \"readers\" is created')

    def load_books(self) -> list:
        books_str = list()
        for book in self.__engine.execute(sqlalchemy.select(self.__db_books_filename.c.id,
                                                     self.__db_books_filename.c.name,
                                                     self.__db_books_filename.c.author,
                                                     self.__db_books_filename.c.year,
                                                     self.__db_books_filename.c.reader_id)):
            books_str.append(str(book))
        # print('books_str', books_str)
        ##создаем список со списками (где каждый список - отедльная книга с int и str элементами)
        list_all_books = [SQLStorage.load_books_from_str(book) for book in books_str]
        # print('list_all_books', list_all_books)
        ##конвертируем каждую книгу в словарь и погружаем их все в список
        list_dict_book = []
        for book in list_all_books:
            if book[4] == 'None':
                book[4] = None
            book_dict = dict(name=f'{book[1]}',
                             author= f'{book[2]}',
                             year= f'{book[3]}',
                             id=f'{book[0]}',
                             reader_id=f'{book[4]}')
            list_dict_book.append(book_dict)

        ##возвращаем список в котором каждая книга об'ект Book
        return [Book.from_dict(book) for book in list_dict_book]

    #############
        # for book in self.__engine.execute(self.__db_books_filename.select().where(self.__db_books_filename.c.id is not None)):
        #     book_dict = dict(name=f'{self.__engine.execute(sqlalchemy.select(self.__db_books_filename.c.name))}',
        #                  author= f'{self.__engine.execute(sqlalchemy.select(self.__db_books_filename.c.author))}',
        #                  year= f'{self.__engine.execute(sqlalchemy.select(self.__db_books_filename.c.year))}',
        #                  id=f'{self.__engine.execute(sqlalchemy.select(self.__db_books_filename.c.id))}',
        #                  reader_id= f'{self.__engine.execute(sqlalchemy.select(self.__db_books_filename.c.reader_id))}')
        # print(book_dict)
        # print ('fff', [Book.from_dict(book) for book in book_dict])
    #################
        # for book in self.__engine.execute(sqlalchemy.select(self.__db_books_filename.c.id,
        #                                                     self.__db_books_filename.c.name,
        #                                                     self.__db_books_filename.c.author,
        #                                                     self.__db_books_filename.c.year))
        #
        # return [Book.from_dict(book) for book in select_all]

    def load_readers(self) -> list:

        readers_str = list()
        for reader in self.__engine.execute(sqlalchemy.select(self.__db_people_filename.c.id,
                                                       self.__db_people_filename.c.name,
                                                       self.__db_people_filename.c.surname,
                                                       self.__db_people_filename.c.year, )):

            readers_str.append(str(reader))
        list_all_readers = [SQLStorage.load_readers_from_str(reader) for reader in readers_str]
        # print('list_all_readers', list_all_readers)
        list_dict_readers = []
        for reader in list_all_readers:
            reader_dict = dict(name=f'{reader[1]}',
                               surname= f'{reader[2]}',
                               year= f'{reader[3]}',
                               id=f'{reader[0]}')
            list_dict_readers.append(reader_dict)

        ##возвращаем список в котором каждая книга об'ект Reader
        return [People.from_dict(reader) for reader in list_dict_readers]

        # return reader_dict
        # return list_all_readers

    def save_books(self, list_Books: list):

        for book in list_Books:
            self.__engine.execute(self.__db_books_filename.insert(),
                           name = f'{book.get_name()}', author = f'{book.get_author()}', year = f'{book.get_year()}')#, reader_id = f'{book.get_reader_id()}'
        self.load_books()

    def save_readers(self, list_People: list):

        for reader in list_People:
            # print(f'{reader.get_name()}, {reader.get_surname()}, {reader.get_year()}')
            self.__engine.execute(self.__db_people_filename.insert(), name=f'{reader.get_name()}',
                                                                    surname=f'{reader.get_surname()}',
                                                                    year=f'{reader.get_year()}')

    def add_book(self, name: str, author: str, year: int = None, book_id: int = None): #-> (bool, str)
        self.__engine.execute(self.__db_books_filename.insert(), name=f'{name}', author=f'{author}', year=f'{year}')

    def remove_book(self, book_id):
        self.__engine.execute(self.__db_books_filename.delete().where(self.__db_books_filename.c.id == book_id))

    def add_reader(self, name: str, surname: str, year: int = None, reader_id: int = None): #-> (bool, str)
        self.__engine.execute(self.__db_people_filename.insert(), name=f'{name}', surname=f'{surname}', year=f'{year}')

    def remove_reader(self, reader_id):
        self.__engine.execute(self.__db_people_filename.delete().where(self.__db_people_filename.c.id == reader_id))

    def update_book(self, book_id, reader_id):
        self.__engine.execute(self.__db_books_filename.update().values(reader_id=f'{reader_id}').where(
            self.__db_books_filename.c.id == int(f'{book_id}')))

    def return_book(self, book_id, reader_id):
        self.__engine.execute(self.__db_books_filename.update().values(reader_id=None).where(
            self.__db_books_filename.c.id == int(f'{book_id}')))

    @staticmethod
    def load_books_from_str(book: str, sep: str = "\', ") -> list:
        a = book.strip().split(", \'")
        b = a[2].strip().split(sep)
        c = b[1].strip().split(", ")
        new_list = [a[0], a[1], b[0], c[0], c[1]]
        new_list[0] = new_list[0].replace('(\'', '', 1)
        new_list[4] = new_list[4].replace('\'', '', 2)

        book_list = [int((str(new_list[0])).replace('(', '', 1)),
                    (str(new_list[1])).replace('\'', '', 1),
                    (str(new_list[2])).replace('\'', '', 2),
                    int((str(new_list[3])).replace('\'', '', 2)),
                    (str(new_list[4])).replace(')', '', 1)]
        return book_list

    @staticmethod
    def load_readers_from_str(reader: str, sep: str = '\', ') -> list:
        a = reader.strip().split(", \'")
        b = a[2].strip().split(sep)
        new_list = [a[0], a[1], b[0], b[1]]
        new_list[0] = new_list[0].replace('(\'', '', 1)
        reader_list = [int((str(new_list[0])).replace('(', '', 1)),
                       (str(new_list[1])).replace('\'', '', 2),
                       (str(new_list[2])).replace('\'', '', 2),
                       int((str(new_list[3])).replace(')', '', 1))]
        return reader_list


