from logging import log
import todo_app,pymongo,uuid
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


def get_board():
    client = pymongo.MongoClient(f"mongodb+srv://{os.getenv('MONGO_USERNAME')}:{os.getenv('MONGO_PASS')}@{os.getenv('MONGO_HOST')}/?w=majority")
    db = client[os.getenv('DEFAULT_DATABASE')]
    os.environ['TRELLO_BOARD'] = "test_board" + uuid.uuid1().hex
    col = os.environ['TRELLO_BOARD']
    return db[col]
   

def del_board(db):
    db.drop()

@pytest.fixture(scope='module')
def app_with_temp_board():
    # Create the new board & update the board id environment variable
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    os.environ['LOGIN_DISABLED'] = 'True'
    db = get_board()
    # construct the new application
    application = todo_app.app.create_app()
    #application.boardId = board_id
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application

    # Tear Down
    thread.join(1)
    del_board(db)

@pytest.fixture
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome('./chromedriver', options=opts) as driver:
    #with webdriver.Chrome() as driver:
        yield driver

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
