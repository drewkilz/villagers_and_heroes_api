from decimal import Decimal
from flask.json import JSONEncoder


class Encoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super(Encoder, self).default(o)
