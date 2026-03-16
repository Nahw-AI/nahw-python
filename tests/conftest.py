import httpx
import pytest
import respx

from nahw import NahwClient

BASE_URL = "https://api.nahw.ai"


@pytest.fixture()
def mock_api():
    with respx.mock(base_url=BASE_URL) as rsps:
        yield rsps


@pytest.fixture()
def client():
    c = NahwClient(api_key="nhw_test_key", team_id="team_1")
    yield c
    c.close()
