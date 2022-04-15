import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from user.models import User, Organization


@pytest.fixture
def default_password():
    return "ThisIsAS4f3P4ssw0rd"


@pytest.fixture
def default_username():
    return "user@example.com"


@pytest.fixture
def user_factory(default_password, default_username, **kwargs):
    def create_user(**kwargs):
        attributes = {
            "username": default_username,
            "email": default_username,
            "password": default_password,
            "organization": Organization.objects.all().get(),
            **kwargs
        }
        return User.objects.create_user(**attributes)

    return create_user


@pytest.fixture
def standard_user(user_factory):
    return user_factory(
        username="standard@user.com",
        email="standard@user.com"
    )


@pytest.fixture
def authenticated_client(standard_user):
    """Takes the Django test client and authenticates it with a JWT."""
    token = AccessToken.for_user(standard_user)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client
