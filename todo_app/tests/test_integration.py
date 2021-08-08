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
    assert 'FINISHED CARD' in response_data

trello_lists = [
    {
        "id":"60eacfe2a3dd2132b75a4b2a",
        "name":"TODO"
    },
      {
        "id":"60eacfe2a3dd2132b75a4b2b",
        "name":"DOING"
    },
      {
        "id":"60eacfe2a3dd2132b75a4b2c",
        "name":"FINISHED"
    }
] 
trello_cards = [
    {
        "idList":"60eacfe2a3dd2132b75a4b2d",
        "id":"60eacfe2a3dd2132b75a4b2d",
        "idShort":"1",
        "name":"FINISHED CARD",
        "closed":False,
        "pos":4096,
        "softLimit":None,
        "idBoard":"60eacfe2a3dd2132b75a4b2c",
        "subscribed":False
    }
] 
trello_boards = [
    {
        "id":"60eacfe2a3dd2132b75a4b2a",
        "name":"board_id"
    }
] 


def mock_get_lists(url, data):
    print("call to me:" + url)
    if url == 'https://api.trello.com/1/boards/board_id/lists':
        response = Mock(ok=True)
        response.json.return_value = trello_lists
        response.status_code=200
        return response
    if url == 'https://api.trello.com/1/boards/board_id':
        response = Mock(ok=True)
        response.json.return_value = trello_boards
        response.status_code=200
        return response
    if url == 'https://api.trello.com/1/boards/board_id/cards':
        response = Mock(ok=True)
        response.json.return_value = trello_cards
        response.status_code=200
        return response
    return None


