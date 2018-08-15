import json
import logging
import traceback

from flask import jsonify, request, Response
from flask.views import MethodView

from shared.database.models import Employee


log = logging.getLogger(__name__)
logging_format = '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -50s %(lineno) -5d: %(message)s'
logging.basicConfig(level=logging.INFO, format=logging_format)


class EmployeeHTTPHandler(MethodView):
    @staticmethod
    def get():
        name = request.args.get('name', None)
        if name is not None:
            return jsonify([x.as_dict() for x in
                            Employee.select(
                                            Employee.name,
                                            Employee.age
                                            )
                                            .where(Employee.name == name)])
        else:
            return jsonify([x.as_dict() for x in Employee.select()])

    @staticmethod
    def post():
        required_fields = {
            'name',
            'age',
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
                response='Not enough params to create user. Set params <name> and <age> to the request\'s body.',
                status=400)
        try:
            Employee.get_or_create(**data)
        except Exception as e:
            log.error('Error during creating user. Exception: %s.' % traceback.format_exc(str(e)))
            return Response(
                response='Error during creating user.',
                status=500)
        return Response(status=201)

    @staticmethod
    def patch():
        required_fields = {
            'name',
            'age',
        }
        data = request.get_data()
        try:
            data = json.loads(data)
        except Exception as e:
            return Response(
                response='Not JSON format. Exception: %s' % str(e),
                status=400)
        if not any(field in data for field in required_fields):
            return Response(
                response='Not enough params to create user. Set params <name> or <age> to the request\'s body.',
                status=400)

        if data.get('id', None) is not None:
            try:
                Employee.update(**data).where(Employee.id == data['id']).execute()
            except Exception as e:
                log.error('Error during employee updates. Exception: %s' % traceback.format_exc(str(e)))
                return Response(status=500)
            else:
                return Response(status=200)
        return Response(response='Not enough params to delete user. Set param <id> to the request\'s body.',
                        status=400)

    @staticmethod
    def delete():
        _id = request.args.get('id', None)
        if _id is not None:
            employee = Employee.get(Employee.id == _id)
            try:
                employee.delete_instance()
            except Exception as e:
                log.error('Error during deleting employee. Exception: %s' % traceback.format_exc(str(e)))
                return Response(status=500)
            else:
                return Response(status=200)
        return Response(response='Not enough params to delete user. Set param <id> to the request\'s body.',
                        status=400)
