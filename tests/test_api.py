import pytest

@pytest.mark.api
def test_get_endpoint(api_setup):
    response = api_setup.get('endpoint')
    assert response['key'] == 'expected_value' 