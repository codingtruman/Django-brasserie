import pytest
from api.models import Beer
from api.paginators import CustomPagination


@pytest.mark.django_db
def test_get_references(client, create_test_staff):

    # check db load
    assert 3 == Beer.objects.count()

    # anonymous users:
    response = client.get("/api/references/")
    assert isinstance(response.data, list)
    assert "Leffe blonde" == response.data[0]["name"]
    assert "available" == response.data[1]["availability"]

    # check the orderings
    response = client.get("/api/references/?ordering=ref")
    assert "brewdogipa" == response.data[0]["ref"]
    assert "outofstock" == response.data[1]["availability"]

    response = client.get("/api/references/?ordering=-ref")
    assert "brewdogipa" == response.data[2]["ref"]
    assert "outofstock" == response.data[1]["availability"]

    response = client.get("/api/references/?ordering=name")
    assert "brewdogipa" == response.data[0]["ref"]
    assert "outofstock" == response.data[1]["availability"]

    response = client.get("/api/references/?ordering=-name")
    assert "brewdogipa" == response.data[2]["ref"]
    assert "outofstock" == response.data[1]["availability"]

    # check available and unavailable ones
    response = client.get("/api/references/?available=true")
    assert 2 == len(response.data)
    assert "available" == response.data[1]["availability"]

    response = client.get("/api/references/?available=false")
    assert 1 == len(response.data)
    assert "outofstock" == response.data[0]["availability"]

    # check bar filter
    response = client.get("/api/references/?bar=2")
    assert 1 == len(response.data)
    assert 2 == response.data[0]["pk"]

    # authenticated users:
    client.force_login(create_test_staff)
    response = client.get("/api/references/")
    assert isinstance(response.data, list)
    assert "Leffe blonde" == response.data[0]["name"]
    assert "available" == response.data[1]["availability"]

    # check the pagination
    CustomPagination.page_size = 1
    response = client.get("/api/references/?page=2")
    assert 2 == response.data[0]["pk"]
    CustomPagination.page_size = 10


@pytest.mark.django_db
def test_post_references(client, create_test_staff):

    payload = {
        "ref": "test_ref", 
        "name": "test_name", 
        "description": "test_des"
    }
    
    # anonymous users are not allowed to alter db:
    response = client.post("/api/references/", payload, content_type="application/json")
    assert 403 == response.status_code

    # authenticated users:
    client.force_login(create_test_staff)
    response = client.post("/api/references/", payload, content_type="application/json")
    assert 201 == response.status_code
    assert 4 == Beer.objects.count()

    # check added data
    response = client.get("/api/references/")
    assert "test_name" == response.data[3]["name"]
    assert "test_des" == response.data[3]["description"]


@pytest.mark.django_db
def test_put_references(client, create_test_staff):

    payload = {
        "ref": "altered_ref", 
        "name": "altered_name", 
        "description": "altered_des"
    }

    # anonymous users are not allowed to alter db:
    response = client.put("/api/references/3/", payload, content_type="application/json")
    assert 403 == response.status_code

    # authenticated users:
    client.force_login(create_test_staff)
    response = client.put("/api/references/3/", payload, content_type="application/json")
    assert 200 == response.status_code

    response = client.get("/api/references/3/")
    assert "altered_name" == response.data["name"]
    assert "altered_des" == response.data["description"]


@pytest.mark.django_db
def test_delete_references(client, create_test_staff):

    # anonymous users are not allowed to alter db:
    response = client.delete("/api/references/3/")
    assert 403 == response.status_code

    # authenticated users:
    client.force_login(create_test_staff)
    response = client.delete("/api/references/3/")
    assert 204 == response.status_code

    response = client.get("/api/references/3/")
    assert 404 == response.status_code
