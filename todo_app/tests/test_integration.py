from logging import log
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
    #assert 'FINISHED CARD' in response_data

def mock_get_lists(data):
    return [
        Item("60eacfe2a3dd2132b75a4b2a",ItemStatus.FINISHED,'FINISHED CARD'),
        Item("60eacfe2a3dd2132b75a4b2b",ItemStatus.DOING,'doing CARD'),
        Item("60eacfe2a3dd2132b75a4b2c",ItemStatus.TODO,'todo CARD'),
    ]

       


