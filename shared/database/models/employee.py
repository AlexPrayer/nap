from peewee import PrimaryKeyField
from peewee import CharField
from peewee import IntegerField

from shared.database import BaseModel


class Employee(BaseModel):
    class Meta:
        # indexes = (
        #     (('name', 'age'), False),   # Non-unique indexes
        # )
        schema = 'napol'
        db_table = 'employees'

    id = PrimaryKeyField()
    name = CharField()
    age = IntegerField()

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
        }


idx = Employee.index(
    Employee.name,
    Employee.age,
    unique=False)
Employee.add_index(idx)
