from tortoise import fields
from tortoise.models import Model

class User(Model):
    id = fields.IntField(pk=True)
    tg_id = fields.BigIntField(unique=True)
    name = fields.CharField(max_length=50)

    class Meta:
        table = "users"
