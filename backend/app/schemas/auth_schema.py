from marshmallow import Schema, fields, validate


class SignupSchema(Schema):
    roll_no = fields.String(required=True, validate=validate.Length(min=1, max=50))
    name = fields.String(required=True, validate=validate.Length(min=1, max=200))
    socials = fields.Dict(keys=fields.String(), values=fields.String(), load_default=None)


class AdminLoginSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=1))
    password = fields.String(required=True, validate=validate.Length(min=1))
