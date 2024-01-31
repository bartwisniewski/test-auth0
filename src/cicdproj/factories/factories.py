from cicdapp.models import Entry
from factory import Faker
from factory.django import DjangoModelFactory


class EntryFactory(DjangoModelFactory):
    class Meta:
        model = Entry

    text = Faker("text")
