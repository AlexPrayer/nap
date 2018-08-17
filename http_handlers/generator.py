import datetime
import json
import logging
import traceback

from decimal import Decimal
from flask import request, Response
from flask.views import MethodView
from random import randint
from shared.database.models import Coordinate


log = logging.getLogger(__name__)
logging_format = '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -50s %(lineno) -5d: %(message)s'
logging.basicConfig(level=logging.INFO, format=logging_format)


class GeneratorHTTPHandler(MethodView):
    def post(self):
        required_fields = {
            'user',
            'date_from',
            'date_to',
            'latitude',
            'longtitude',
        }
        data = request.get_data()
        try:
            data = json.loads(data)
        except json.JSONDecodeError as e:
            log.error('Error during decoding from JSON. Exception: %s.' % traceback.format_exc(str(e)))
            return Response(
                response='Not JSON format.',
                status=400)
        if not all(field in data for field in required_fields):
            return Response(
                response='Not enough params to create user.'
                         ' Set params <id>, <date_from>, <date_to>, <latitude> and <longtitude> to the request\'s body.',
                status=400)
        try:
            date_from = datetime.datetime.strptime(data['date_from'], '%Y/%m/%d_%H:%M:%S')
            date_to = datetime.datetime.strptime(data['date_to'], '%Y/%m/%d_%H:%M:%S')
        except ValueError as v:
            log.error('Error during formatting dates. Exception: %s.' % traceback.format_exc(str(v)))
            return Response(response='Error during formatting dates.', status=400)

        try:
            latitude = Decimal(data['lat'])
            longtitude = Decimal(data['long'])
        except TypeError as t:
            log.error('Error during converting latitude/longtitude from String to Decimal. Exception: %s.'
                      % traceback.format_exc(str(t)))
            return Response(response='Error during converting latitude/longtitude from String to Decimal.', status=400)

        rows = []
        for single_date in self._generate_daterange(date_from, date_to):     # Use generator to iterate via dates.
            x_axis, y_axis = self._generate_coordinates()
            longtitude += x_axis
            latitude += y_axis
            rows.append({
                'user': data['user'],
                'latitude': latitude,
                'longtitude': longtitude,
                'date': single_date,
            })
        try:
            Coordinate.insert_many(rows).execute()                          # Insert them all!
        except Exception as e:
            log.error('Something went wrong during the insert operation. Exception: %s.' % traceback.format_exc(str(e)))
            return Response(response='Something went wrong during the insert operation.', status=500)

        return Response(status=200)

    @staticmethod
    def _generate_daterange(date_from, date_to):
        for n in range(int((date_to - date_from).seconds / 60)):
            yield date_from + datetime.timedelta(seconds=n * 60)

    @staticmethod
    def _generate_coordinates():
        x_axis = randint(-100, 100)
        y_axis = randint(100 - abs(x_axis), - 100 - abs(x_axis))
        return round(Decimal(x_axis / 100000), 6), round(Decimal(y_axis / 100000), 6)

