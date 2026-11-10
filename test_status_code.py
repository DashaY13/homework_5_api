import pytest
import requests


def pytest_addoption(parser):
    parser.addoption("--url", default="https://ya.ru")
    parser.addoption("--status_code", default="200")


@pytest.fixture
def url(request):
    return request.config.getoption("--url")


@pytest.fixture
def status_code(request):
    return int(request.config.getoption("--status_code"))


def test_url_status_code(url, status_code):
    response = requests.get(url)
    assert response.status_code == status_code