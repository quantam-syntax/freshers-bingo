from marshmallow import Schema, fields, validate


class ChallengeSchema(Schema):
    text = fields.String(required=True, validate=validate.Length(min=1, max=500))
