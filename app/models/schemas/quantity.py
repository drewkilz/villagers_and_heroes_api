from marshmallow import fields, Schema


class QuantitySchema(Schema):
    quantity = fields.Integer(default=1, missing=1)
    stacks = fields.Integer(default=0, missing=0)
    remainder = fields.Integer(default=0, missing=0)
