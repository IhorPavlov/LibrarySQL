
class Book:

    def __init__(self, name: str, author: str, year: int = None, _id: int = None, reader_id: int = None) -> None:
        self.__name = name
        self.__author = author
        self.__year = year
        self.__id = _id if _id is not None else int(id(self))
        self.__reader_id = reader_id

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_author(self):
        return self.__author

    def get_year(self):
        return self.__year

    def get_reader_id(self):
        return self.__reader_id

    def set_reader_id(self, reader_id: int):
        self.__reader_id = reader_id

    def __str__(self):
        return f'book № {self.__id}: "{self.__name}". {self.__author}, {self.__year}'

    def to_dict(self):
        book_dict = {
            'name': self.get_name(),
            'author': self.get_author(),
            'year': self.get_year(),
            'id': self.get_id(),
            'reader_id': self.get_reader_id()
        }
        return book_dict

    @classmethod
    def from_dict(cls, dict_obj):
        return cls(
            name=dict_obj['name'],
            author=dict_obj['author'],
            year=dict_obj['year'],
            _id=dict_obj['id'],
            reader_id=dict_obj['reader_id']
        )

    def repr(self):
        cls_name = __class__.__name__

        return ' '.join(
            [
                f'{attr.replace(f"_{cls_name}", "")}={getattr(self, attr)}'
                for attr in dir(self) if attr.startswith(f'_{cls_name}')
            ]
        )