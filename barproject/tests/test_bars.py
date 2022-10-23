import pytest
from api.models import Bar
from api.paginators import CustomPagination

@pytest.mark.django_db
def test_get_bars(client, create_test_staff):

    # check db load
    assert 2 == Bar.objects.count()

    # anonymous users:
    response = client.get("/api/bars/")
    assert isinstance(response.data, list)
    assert "1er étage" == response.data[0]["name"]
    assert "2ème étage" == response.data[1]["name"]

    # check the orderings
    response = client.get("/api/bars/?ordering=pk")
    assert "1er étage" == response.data[0]["name"]
    assert "2ème étage" == response.data[1]["name"]

    response = client.get("/api/bars/?ordering=-pk")
    assert "1er étage" == response.data[1]["name"]
    assert "2ème étage" == response.data[0]["name"]

    response = client.get("/api/bars/?ordering=name")
    assert "1er étage" == response.data[0]["name"]
    assert "2ème étage" == response.data[1]["name"]

    response = client.get("/api/bars/?ordering=-name")
    assert "1er étage" == response.data[1]["name"]
    assert "2ème étage" == response.data[0]["name"]

    # authenticated users:
    client.force_login(create_test_staff)
    response = client.get("/api/bars/")
    assert isinstance(response.data, list)
    assert "1er étage" == response.data[0]["name"]
    assert "2ème étage" == response.data[1]["name"]

    # check the pagination
    CustomPagination.page_size = 1
    response = client.get("/api/bars/?page=2")
    assert 2 == response.data[0]["pk"]
    CustomPagination.page_size = 10


@pytest.mark.django_db
def test_post_bars(client, create_test_staff):

    payload = {"name": "3ème étage"}
    
    # anonymous users are not allowed to alter db:
    response = client.post("/api/bars/", payload, content_type="application/json")
    assert 403 == response.status_code

    # authenticated users:
    client.force_login(create_test_staff)
    response = client.post("/api/bars/", payload, content_type="application/json")
    assert 201 == response.status_code
    assert 3 == Bar.objects.count()

    # check added data
    response = client.get("/api/bars/")
    assert 3 == response.data[2]["pk"]
    assert "3ème étage" == response.data[2]["name"]


@pytest.mark.django_db
def test_put_bars(client, create_test_staff):

    payload = {"name": "altered_name"}

    # anonymous users are not allowed to alter db:
    response = client.put("/api/bars/2/", payload, content_type="application/json")
    assert 403 == response.status_code

    # authenticated users:
    client.force_login(create_test_staff)
    response = client.put("/api/bars/2/", payload, content_type="application/json")
    assert 200 == response.status_code

    response = client.get("/api/bars/2/")
    assert "altered_name" == response.data["name"]


@pytest.mark.django_db
def test_delete_bars(client, create_test_staff):

    # anonymous users are not allowed to alter db:
    response = client.delete("/api/bars/2/")
    assert 403 == response.status_code

    # authenticated users:
    client.force_login(create_test_staff)
    response = client.delete("/api/bars/2/")
    assert 204 == response.status_code

    response = client.get("/api/bars/2/")
    assert 404 == response.status_code
