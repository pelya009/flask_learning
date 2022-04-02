import pytest
import subprocess
import time

from requests.exceptions import ConnectionError

from create_tables import prepare_db
from tests.utils.api_client import api_client


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

    status_code = None
    now = time.time()
    while status_code != 200:
        try:
            status_code = api_client.get_home().status_code
        except ConnectionError:
            pass
        time.sleep(1)
        if time.time() - now > 10:
            raise Exception('App not started')

    yield process
    process.terminate()
    process.kill()
    print(process.pid)
