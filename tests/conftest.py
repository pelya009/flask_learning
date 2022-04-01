import pytest
import subprocess
from create_tables import prepare_db


@pytest.fixture(scope='session', autouse=True)
def create_tables():
    prepare_db()


@pytest.fixture(scope='session', autouse=True)
def run_app():
    process = subprocess.Popen(
        args='python app.py',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf-8')
    # TODO: Add smart wait
    import time
    time.sleep(3)
    yield
    process.kill()
    print(process.pid)
