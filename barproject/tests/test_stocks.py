import pytest
from api.models import Stock
from api.paginators import CustomPagination


@pytest.mark.django_db
def test_get_stocks(client, create_test_staff):

    # check db load
    assert 4 == Stock.objects.count()

    # anonymous users are not allowed to access:
    response = client.get("/api/stocks/")
    assert 403 == response.status_code

    # authenticated users:
    client.force_login(create_test_staff)
    response = client.get("/api/stocks/")
    assert isinstance(response.data, list)
    assert 1 == response.data[0]["bar"]
    assert 8 == response.data[1]["stock"]

    # check the orderings
    response = client.get("/api/stocks/?ordering=reference")
    assert 1 == response.data[0]["bar"]
    assert 8 == response.data[1]["stock"]

    response = client.get("/api/stocks/?ordering=-reference")
    assert 2 == response.data[0]["bar"]
    assert 5 == response.data[1]["stock"]

    response = client.get("/api/stocks/?ordering=bar")
    assert 1 == response.data[0]["reference"]
    assert 8 == response.data[1]["stock"]

    response = client.get("/api/stocks/?ordering=-bar")
    assert 2 == response.data[0]["bar"]
    assert 2 == response.data[1]["reference"]

    response = client.get("/api/stocks/?ordering=stock")
    assert 0 == response.data[0]["stock"]
    assert 2 == response.data[1]["bar"]

    response = client.get("/api/stocks/?ordering=-stock")
    assert 1 == response.data[0]["bar"]
    assert 8 == response.data[1]["stock"]

    # check the pagination
    CustomPagination.page_size = 1
    response = client.get("/api/stocks/?page=2")
    assert 2 == response.data[0]["reference"]
    CustomPagination.page_size = 10


@pytest.mark.django_db
def test_post_stocks(client, create_test_staff):

    payload = {"reference": 1, "bar": 2, "stock": 1}

    # anonymous users are not allowed to alter db:
    response = client.post("/api/stocks/", payload, content_type="application/json")
    assert 403 == response.status_code

    # authenticated users are not allowed to alter db:
    client.force_login(create_test_staff)
    response = client.post("/api/stocks/", payload, content_type="application/json")
    assert 403 == response.status_code


@pytest.mark.django_db
def test_put_stocks(client, create_test_staff):

    payload = {"reference": 1, "bar": 1, "stock": 11}

    # anonymous users are not allowed to alter db:
    response = client.put("/api/stocks/1/", payload, content_type="application/json")
    assert 403 == response.status_code

    # authenticated users are not allowed to alter db:
    client.force_login(create_test_staff)
    response = client.put("/api/stocks/1/", payload, content_type="application/json")
    assert 403 == response.status_code


@pytest.mark.django_db
def test_delete_stocks(client, create_test_staff):

    # anonymous users are not allowed to alter db:
    response = client.delete("/api/stocks/1/")
    assert 403 == response.status_code

    # authenticated users are not allowed to alter db:
    client.force_login(create_test_staff)
    response = client.delete("/api/stocks/1/")
    assert 403 == response.status_code
