import pytest

from tests.conftests import client


# def test_register():
#     responce_data = client.post("/auth/register", json={
#         "email": "user@example.com",
#         "password": "string",
#         "is_active": True,
#         "is_superuser": False,
#         "is_verified": False
#     })
#     assert responce_data.status_code==201, ""


def test_example():
    assert 1+1==2


