import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command


@pytest.fixture
def create_test_staff():

    user_model = get_user_model()
    test_staff = user_model.objects.create(
        username = "staff_1", 
        password = "djangorest",
        )
    return test_staff

@pytest.fixture(scope='module')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'api.json')
