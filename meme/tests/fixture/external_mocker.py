import pytest
from _pytest.fixtures import SubRequest
from pytest_mock import MockerFixture


@pytest.fixture()
def external_mocker(request: SubRequest, mocker: MockerFixture):
    function = mocker.patch(request.param['function_path'])
    function.return_value = request.param['return_value']
    return request.param['return_value']