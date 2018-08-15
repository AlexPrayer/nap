import datetime
import json
import logging
import traceback

from flask import jsonify, request, Response
from flask.views import MethodView

from shared.database.models import Coordinate


log = logging.getLogger(__name__)
logging_format = '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -50s %(lineno) -5d: %(message)s'
logging.basicConfig(level=logging.INFO, format=logging_format)


class MovingHTTPHandler(MethodView):
    @staticmethod
    def post():
        required_fields = {
            'id',
            'date_from',
            'date_to',
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
                         ' Set params <id>, <date_from> and <date_to> to the request\'s body.',
                status=400)
        if data.get('id', None) is not None:
            try:
                date_from = datetime.datetime.strptime(request.args.get('date_from'), '%m/%d/%Y')
                date_to = datetime.datetime.strptime(request.args.get('date_to'), '%m/%d/%Y')
            except ValueError as v:
                log.error('Error during formatting dates. Exception: %s.' % traceback.format_exc(str(v)))
                return Response(response='Error during formatting dates.', status=400)
            response = [x.as_dict() for x in Coordinate.select()
                .where(
                    (Coordinate.date.between(date_from, date_to) &
                    (Coordinate.user == data['id']))
            )]
            return jsonify(response)
        return Response(
            response='Not enough params to get user\'s moving. Set param <id> to the request\'s body.',
            status=400)

