import os
from Library.storages.json_storage import JSONStorage
from Library.utils import logprint
from Library.utils.inputs import input_numeric

from Library.library import Library


def user_choice():
    while True:
        print(os.linesep)
        _choice = input('What do you want?\n'
                        '1 - show all books in the library\n'
                        '2 - show available books in the library\n'
                        '3 - show all readers in the library\n'
                        '4 - give book\n'
                        '5 - return book\n'
                        '6 - add book to library\n'
                        '7 - remove book from library\n'
                        '8 - register reader\n'
                        '9 - remove reader from library\n'
                        '0 - exit\n'
                        'make your choice: ')

        if not _choice.isnumeric() or int(_choice) < 0 or int(_choice) > 9:
            logprint.print_fail('invalid input!')
            input('Press Enter to continue...')
        else:
            return int(_choice)


def main_loop(lib: Library):
    while True:
        _choice = user_choice()

        # 1 - show all books in the library
        if _choice == 1:
            for book in lib.get_all_books():
                print(book)

        # 2 - show available books in the library
        if _choice == 2:
            for book in lib.get_available_books():
                print(book)

        # 3 - show all readers in the library
        if _choice == 3:
            for reader in lib.get_all_readers():
                print(reader)

        # 4 - give book
        if _choice == 4:
            id_book = input_numeric('Enter id book: ')
            id_reader = input_numeric('Enter id reader: ')

            lib.book_for_reader(id_book, id_reader)

        # 5 - return book
        if _choice == 5:
            id_book = input_numeric('Enter id book: ')
            id_reader = input_numeric('Enter id reader: ')

            lib.return_to_library(id_book, id_reader)

        # 6 - add book to library
        if _choice == 6:
            title = input('Enter the title of the book: ')
            author = input('Enter the author of the book: ')
            years = input_numeric('Enter the year of publication of the book: ')

            lib.add_book(title, author, years)

        # 7 - remove book from library
        if _choice == 7:
            id_book = input_numeric('Enter id book: ')

            lib.remove_book(id_book)

        # 8 - register reader
        if _choice == 8:
            name = input('Enter the name of the reader: ')
            surname = input('Enter the surname of the reader: ')
            year = input_numeric(f'Enter the year of {name}\'s birth: ')

            lib.add_reader(name, surname, year)

        # 9 - remove reader from library
        if _choice == 9:
            id_reader = input_numeric('Enter id reader: ')

            lib.remove_reader(id_reader)

        # 0 - exit
        if _choice == 0:
            exit(0)


if __name__ == '__main__':
    storage = JSONStorage('db_books.db', 'db_readers.db')

    lib = Library(storage)
    if not lib.load_books():
        lib.load_books_from_txt_file('LibraryITEA/init_data/books.txt', sep='$!$')

    if not lib.load_readers():
        lib.load_readers_from_txt_file('LibraryITEA/init_data/readers.txt')

    main_loop(lib)
