from werkzeug.routing import BaseConverter


class StringOrIntConverter(BaseConverter):
    def to_python(self, value):
        try:
            return int(value)
        except ValueError:
            return value
