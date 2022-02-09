from sqlalchemy import Column, Integer, Text
from Library.library_units.base import Base


class Reader(Base):
    __tablename__ = 'readers'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', Text, nullable=False)
    surname = Column('surname', Text, nullable=False)
    year = Column('year', Integer, nullable=False)

    def __init__(self, name: str, surname: str, year: int):
        self.name = name
        self.surname = surname
        self.year = year
        # self.id = _id if _id is not None else int(id(self))

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_surname(self):
        return self.surname

    def get_year(self):
        return self.year

    def __str__(self):
        return f'reader № {self.id}: {self.surname} {self.name}, {self.year}'

    # def to_dict(self):
    #     reader_dict = {
    #         'name': self.get_name(),
    #         'surname': self.get_surname(),
    #         'year': self.get_year(),
    #         'id': self.get_id(),
    #     }
    #     return reader_dict
    #
    # @classmethod
    # def from_dict(cls, dict_obj):
    #     return cls(
    #         name=dict_obj['name'],
    #         surname=dict_obj['surname'],
    #         year=dict_obj['year'],
    #         _id=dict_obj['id'],
    #     )

    def repr(self):
        cls_name = __class__.__name__

        return ' '.join(
            [
                f'{attr.replace(f"_{cls_name}", "")}={getattr(self, attr)}'
                for attr in dir(self) if attr.startswith(f'_{cls_name}')
            ]
        )