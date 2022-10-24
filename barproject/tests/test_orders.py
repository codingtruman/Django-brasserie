import pytest
from api.models import OrderItems, Orders, Stock

@pytest.mark.django_db
def test_regular(client, create_test_staff):

    # check db record
    assert 0 == Orders.objects.count()
    assert 0 == OrderItems.objects.count()
    assert 10 == Stock.objects.get(bar=1, reference=1).stock
    assert 8 == Stock.objects.get(bar=1, reference=2).stock

    payload = {
        "bar": 1,
        "items": [
            {
                "reference": 1,
                "count": 2
            },
            {
                "reference": 2,
                "count": 1
            },
        ]
    }

    # authenticated users are not allowed to post:
    client.force_login(create_test_staff)
    response = client.post("/api/orders/", payload, content_type="application/json")
    assert 403 == response.status_code

    # anonymous users are allowed to post:
    client.logout()
    response = client.post("/api/orders/", payload, content_type="application/json", follow=True)
    assert isinstance(response.data["pk"], int)
    assert 1 == response.data["bar"]
    assert isinstance(response.data["items"], list)
    assert 1 == response.data["items"][0]["reference"]
    assert 1 == response.data["items"][1]["count"]
    
    # check 1 entry in Orders table and multiple entries in OrderItems table
    assert 1 == Orders.objects.count()
    assert 2 == OrderItems.objects.count()
    # check stock decrease
    assert 8 == Stock.objects.get(bar=1, reference=1).stock
    assert 7 == Stock.objects.get(bar=1, reference=2).stock

    # anonymous users are not allowed to get, put, or delete:
    response = client.get("/api/orders/")
    assert 403 == response.status_code
    response = client.put("/api/orders/1/", payload, content_type="application/json")
    assert 403 == response.status_code
    response = client.delete("/api/orders/1/", content_type="application/json")
    assert 403 == response.status_code

    # authenticated users are allowed to get:
    client.force_login(create_test_staff)
    response = client.get("/api/orders/")
    assert isinstance(response.data, list)
    assert isinstance(response.data[0]["pk"], int)
    assert payload["bar"] == response.data[0]["bar"]
    assert payload["items"] == response.data[0]["items"]

    # authenticated users are not allowed to put or delete
    response = client.put("/api/orders/1/", payload, content_type="application/json")
    assert 403 == response.status_code
    response = client.delete("/api/orders/1/", content_type="application/json")
    assert 403 == response.status_code


@pytest.mark.django_db
def test_exceptions(client, create_test_staff):

    # post an empty order:
    response = client.post("/api/orders/", {}, content_type="application/json")#, follow=True)
    assert 400 == response.status_code

    payload = {
        "bar": 1,
        "items": [
            {
                "reference": 1,
                "count": 20
            },
            {
                "reference": 2,
                "count": 1
            }
        ]
    }

    # insufficient stock
    response = client.post("/api/orders/", payload, content_type="application/json")
    assert 400 == response.status_code

    payload = {
        "bar": 2,
        "items": [
            {
                "reference": 1,
                "count": 2
            },
            {
                "reference": 2,
                "count": 3
            }
        ]
    }

    # record doesn't exist in Stock:
    response = client.post("/api/orders/", payload, content_type="application/json")
    assert 400 == response.status_code
