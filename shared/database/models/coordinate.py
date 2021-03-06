from peewee import PrimaryKeyField
from peewee import DecimalField
from peewee import ForeignKeyField
from peewee import DateTimeField

import datetime

from shared.database.models import Employee

from shared.database import BaseModel


class Coordinate(BaseModel):
    class Meta:
        schema = 'napol'
        db_table = 'coordinates'

    id = PrimaryKeyField()
    latitude = DecimalField(max_digits=8, decimal_places=6)
    longtitude = DecimalField(max_digits=8, decimal_places=6)
    date = DateTimeField(default=datetime.datetime.utcnow())
    user = ForeignKeyField(Employee, related_name='employee')

    def as_dict(self):
        return {
            'id': self.id,
            'latitude': str(self.latitude),
            'longtitude': str(self.longtitude),
            'user_id': self.user_id,
            'date': str(self.date),
            'user_name': self.user.name,
        }
