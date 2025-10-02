from marshmallow import Schema, fields

class LinkSchema(Schema):
    id = fields.Int(dump_only=True)
    url = fields.Str(required=True)
    title = fields.Str(required=False, allow_none=True)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(load_only=True, required=True)
    nickname = fields.Str(required=True)
    email = fields.Email(required=True)
    role = fields.Str(dump_only=True)
    links = fields.List(fields.Nested(LinkSchema), dump_only=True)