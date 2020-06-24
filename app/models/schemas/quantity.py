from marshmallow import fields, Schema


class QuantitySchema(Schema):
    quantity = fields.Integer(default=1, missing=1)
