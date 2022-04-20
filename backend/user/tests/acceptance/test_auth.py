import pytest

from django.urls import reverse


pytestmark = pytest.mark.acceptance


@pytest.mark.django_db
class TestJWTAuthentication:
    def test_create_jwt_token_pair(
            self, user_factory, client, default_password
    ):
        # GIVEN an active EO user
        eo_user = user_factory(is_active=True)

        # WHEN the user requests a JWT to authenticate using the correct
        # credentials
        response = client.post(
            reverse('token_obtain_pair'),
            {'username': eo_user.username, 'password': default_password},
            content_type="application/json"
        )

        # THEN an access and refresh token are returned
        assert response.status_code == 200
        assert "access" in response.json()
        assert "refresh" in response.json()

    def test_get_user_info_with_token(self, authenticated_client):
        # WHEN a user requests user information using a client
        # authenticated with a valid JWT header
        response = authenticated_client.get(reverse('user-me'))

        # THEN the request is granted
        assert response.status_code == 200

    def test_user_info_is_declined_without_token(self, client):
        # WHEN a user requests user information using a client
        # not authenticated with a valid JWT header
        response = client.get(reverse('user-me'))

        # THEN the request is denied
        assert response.status_code == 401
