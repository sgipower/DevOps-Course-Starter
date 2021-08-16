from logging import log
import todo_app
from todo_app.data import itemstatus
from todo_app.data.itemstatus import ItemStatus
from todo_app.model.viewModel import ViewModel
from todo_app.data.item import Item
import pytest
from dotenv import load_dotenv, find_dotenv
import requests,os

from selenium import webdriver
from threading import Thread

import todo_app.app

load_dotenv()


def add_board():
    response = requests.post(
        url=f'https://api.trello.com/1/boards',
        params={
            'name': 'Selenium',
            'key': os.environ['TRELLO_KEY'],
            'token': os.environ['TRELLO_TOKEN']
        }
    )
    return response.json()['id']


def del_board(board_id):
    requests.delete(
        url=f'https://api.trello.com/1/boards/{board_id}',
        params={
            'key': os.environ['TRELLO_KEY'],
            'token': os.environ['TRELLO_TOKEN']
        }
    )

@pytest.fixture(scope='module')
def app_with_temp_board():
    # Create the new board & update the board id environment variable
    board_id = add_board()
    os.environ['TRELLO_BOARD'] = board_id

    # construct the new application
    application = todo_app.app.create_app()
    application.boardId = board_id
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application

    # Tear Down
    thread.join(1)
    del_board(board_id)

@pytest.fixture
def driver():
    driver = webdriver.Firefox()
    yield driver
    # this will close the windows after the test is done.
    driver.quit()

def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'

def test_new_task(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    new_task_input = driver.find_element_by_xpath("//*[@id='new-task-input']")
    new_task_input.send_keys('Selenium Task')

    driver.find_element_by_xpath("//button[contains(text(), 'Submit')]").click()
    #find task
    section = driver.find_element_by_xpath("//*[@id='todo-tasks']")
    tasks = section.find_elements_by_xpath("//*[@id='todo-task']")

    assert next(task for task in tasks if 'Selenium Task' in task.text) is not None
