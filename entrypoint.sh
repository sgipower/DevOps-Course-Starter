#!/bin/bash
gunicorn -b 0.0.0.0:$PORT --chdir 'todo_app/' 'app:create_app()'