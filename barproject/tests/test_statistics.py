import pytest
# from api.models import 


@pytest.mark.django_db
def test_get_statistics(client, create_test_staff):

    # anonymous users are not allowed to access:
    response = client.get("/api/statistics/")
    assert 403 == response.status_code

    # authenticated users are allowed to access:
    client.force_login(create_test_staff)
    response = client.get("/api/statistics/")
    assert isinstance(response.data, dict)
    assert [1] == response.data["all_stocks"]["bars"]
    assert [2] == response.data["miss_at_least_one"]["bars"]


@pytest.mark.django_db
def test_post_statistics(client, create_test_staff):

    payload = {
        "test_attr": {
            "description": "test_des",
            "bars": [1]
        }
    }
    
    # anonymous users are not allowed to alter db:
    response = client.post("/api/statistics/", payload, content_type="application/json")
    assert 403 == response.status_code

    # authenticated users are not allowed to alter db:
    client.force_login(create_test_staff)
    response = client.post("/api/statistics/", payload, content_type="application/json")
    assert 403 == response.status_code


@pytest.mark.django_db
def test_put_statistics(client, create_test_staff):

    payload = {
        "test_attr": {
            "description": "test_des",
            "bars": [1]
        }
    }

    # anonymous users are not allowed to alter db:
    response = client.put("/api/statistics/1/", payload, content_type="application/json")
    assert 403 == response.status_code

    # authenticated users are not allowed to alter db:
    client.force_login(create_test_staff)
    response = client.put("/api/statistics/1/", payload, content_type="application/json")
    assert 403 == response.status_code


@pytest.mark.django_db
def test_delete_statistics(client, create_test_staff):

    # anonymous users are not allowed to alter db:
    response = client.delete("/api/statistics/1/")
    assert 403 == response.status_code

    # authenticated users are not allowed to alter db:
    client.force_login(create_test_staff)
    response = client.delete("/api/statistics/1/")
    assert 403 == response.status_code
