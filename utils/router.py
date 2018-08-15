from http_handlers import EmployeeHTTPHandler
from http_handlers import MovingHTTPHandler
from http_handlers import GeneratorHTTPHandler
from http_handlers import LastPositionHTTPHandler

class Router:
    @staticmethod
    def apply_routes(app):
        app.add_url_rule('/api', view_func=EmployeeHTTPHandler.as_view('employees'),
                         methods=['GET', 'POST', 'PATCH', 'DELETE'])
        app.add_url_rule('/api/moving', view_func=MovingHTTPHandler.as_view('moving'),
                         methods=['POST'])
        app.add_url_rule('/api/generate', view_func=GeneratorHTTPHandler.as_view('generation'),
                         methods=['POST'])
        app.add_url_rule('/api/position', view_func=LastPositionHTTPHandler.as_view('last_position'),
                         methods=['GET'])
        return app
