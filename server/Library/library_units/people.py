
class People:
    def __init__(self, name: str, surname: str, year: int = None, _id: int = None):

        self.__name = name
        self.__surname = surname
        self.__year = year
        self.__id = _id if _id is not None else int(id(self))

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_surname(self):
        return self.__surname

    def get_year(self):
        return self.__year

    def __str__(self):
        return f'reader № {self.__id}: {self.__surname} {self.__name}, {self.__year}'

    def to_dict(self):
        reader_dict = {
            'name': self.get_name(),
            'surname': self.get_surname(),
            'year': self.get_year(),
            'id': self.get_id(),
        }
        return reader_dict

    @classmethod
    def from_dict(cls, dict_obj):
        return cls(
            name=dict_obj['name'],
            surname=dict_obj['surname'],
            year=dict_obj['year'],
            _id=dict_obj['id'],
        )

    def repr(self):
        cls_name = __class__.__name__

        return ' '.join(
            [
                f'{attr.replace(f"_{cls_name}", "")}={getattr(self, attr)}'
                for attr in dir(self) if attr.startswith(f'_{cls_name}')
            ]
        )