from marshmallow import Schema, fields


class CostSchema(Schema):
    total = fields.Decimal(default=0)
    gold = fields.Integer(default=0)
    silver = fields.Integer(default=0)
    copper = fields.Integer(default=0)
