import todo_app
from todo_app.data import itemstatus
from todo_app.data.itemstatus import ItemStatus
from todo_app.model.viewModel import ViewModel
from todo_app.data.item import Item
import pytest
from dotenv import load_dotenv, find_dotenv

from unittest.mock import patch, Mock
import todo_app.app

@pytest.fixture
def client():
 # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
 # Create the new app.
    test_app = todo_app.app.create_app()
 # Use the app to create a test_client that can be used in our

    with test_app.test_client() as client:
        yield client

    
@patch('requests.get')
def test_index_page(mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_lists
    response = client.get('/')
    response_data = response.data.decode()
    assert 'T1' in response_data


def mock_get_lists(url, params):
    if url == 'https://api.trello.com/1/boards/board_id/lists':
        response = Mock()
        response.json.return_value = {'value': 1}
        return response
    return None