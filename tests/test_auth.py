import pytest
from unittest import mock
from aiohttp import ClientResponseError
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from .auth import OAuth2Session

# thingy91-api-brown/app/test_auth.py

class TestOAuth2Session(AioHTTPTestCase):

    def setUp(self):
        self.client_id = 'test_client_id'
        self.client_secret = 'test_client_secret'
        self.authorization_base_url = 'https://example.com/auth'
        self.token_url = 'https://example.com/token'
        self.redirect_uri = 'https://example.com/callback'
        self.session = OAuth2Session(
            client_id=self.client_id,
            client_secret=self.client_secret,
            authorization_base_url=self.authorization_base_url,
            token_url=self.token_url,
            redirect_uri=self.redirect_uri
        )

    @unittest_run_loop
    async def test_fetch_token_success(self):
        code = 'test_code'
        token_response = {'access_token': 'test_token', 'token_type': 'Bearer'}

        with mock.patch.object(self.session, 'post', return_value=mock.MagicMock()) as mock_post:
            mock_response = mock.MagicMock()
            mock_response.json = mock.AsyncMock(return_value=token_response)
            mock_post.return_value.__aenter__.return_value = mock_response

            token = await self.session.fetch_token(code)
            assert token == token_response

    @unittest_run_loop
    async def test_fetch_token_http_error(self):
        code = 'test_code'

        with mock.patch.object(self.session, 'post', return_value=mock.MagicMock()) as mock_post:
            mock_response = mock.MagicMock()
            mock_response.raise_for_status.side_effect = ClientResponseError(
                request_info=mock.MagicMock(), history=(), status=400, message='Bad Request'
            )
            mock_post.return_value.__aenter__.return_value = mock_response

            with pytest.raises(ClientResponseError):
                await self.session.fetch_token(code)

    def test_authorization_url(self):
        expected_url = f'{self.authorization_base_url}?response_type=code&client_id={self.client_id}&redirect_uri={self.redirect_uri}'
        assert self.session.authorization_url() == expected_url