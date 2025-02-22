from django import VERSION as DJANGO_VERSION
from django.conf import settings
from django.contrib.postgres.fields import (
    ArrayField, HStoreField,
    IntegerRangeField, DateRangeField,
    DateTimeRangeField)
from django.db.models import (
    Model, CharField, ForeignKey, BooleanField, DateField, DateTimeField,
    ManyToManyField, BinaryField, IntegerField, GenericIPAddressField, TextChoices,
    FloatField, DecimalField, DurationField, UUIDField, SET_NULL, PROTECT)


class SomeChoices(TextChoices):
    foo = 'foo'
    bar = 'bar'

class Test(Model):
    name = CharField(max_length=20)
    owner = ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                       on_delete=SET_NULL)
    public = BooleanField(default=False)
    date = DateField(null=True, blank=True)
    datetime = DateTimeField(null=True, blank=True)
    permission = ForeignKey('auth.Permission', null=True, blank=True,
                            on_delete=PROTECT)

    # We can’t use the exact names `float` or `decimal` as database column name
    # since it fails on MySQL.
    a_float = FloatField(null=True, blank=True)
    a_decimal = DecimalField(null=True, blank=True,
                             max_digits=5, decimal_places=2)
    a_choice = CharField(max_length=3, choices=SomeChoices.choices, null=True)
    bin = BinaryField(null=True, blank=True)
    ip = GenericIPAddressField(null=True, blank=True)
    duration = DurationField(null=True, blank=True)
    uuid = UUIDField(null=True, blank=True)

    try:
        from django.db.models import JSONField
        json = JSONField(null=True, blank=True)
    except ImportError:
        pass

    class Meta:
        ordering = ('name',)


class TestParent(Model):
    name = CharField(max_length=20)


class TestChild(TestParent):
    """
    A OneToOneField to TestParent is automatically added here.
    https://docs.djangoproject.com/en/3.2/topics/db/models/#multi-table-inheritance
    """
    public = BooleanField(default=False)
    permissions = ManyToManyField('auth.Permission', blank=True)


class PostgresModel(Model):
    int_array = ArrayField(IntegerField(null=True, blank=True), size=3,
                           null=True, blank=True)

    hstore = HStoreField(null=True, blank=True)
    if DJANGO_VERSION < (4, 0):
        from django.contrib.postgres.fields import JSONField
        json = JSONField(null=True, blank=True)

    int_range = IntegerRangeField(null=True, blank=True)
    try:
        from django.contrib.postgres.fields import FloatRangeField
        float_range = FloatRangeField(null=True, blank=True)
    except ImportError:
        pass

    try:
        from django.contrib.postgres.fields import DecimalRangeField
        decimal_range = DecimalRangeField(null=True, blank=True)
    except ImportError:
        pass
    date_range = DateRangeField(null=True, blank=True)
    datetime_range = DateTimeRangeField(null=True, blank=True)

    class Meta:
        # Tests schema name in table name.
        db_table = '"public"."cachalot_postgresmodel"'


class UnmanagedModel(Model):
    name = CharField(max_length=50)

    class Meta:
        managed = False
