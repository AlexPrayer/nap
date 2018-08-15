import logging

from flask import jsonify
from flask.views import MethodView
from peewee import fn

from shared.database.models import Coordinate


log = logging.getLogger(__name__)
logging_format = '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -50s %(lineno) -5d: %(message)s'
logging.basicConfig(level=logging.INFO, format=logging_format)


class LastPositionHTTPHandler(MethodView):
    @staticmethod
    def get():
        return jsonify([x.as_dict() for x in
                        Coordinate.select(
                            Coordinate.user,
                            fn.MAX(Coordinate.date).alias('max_date')
                        ).group_by(Coordinate.user)])
