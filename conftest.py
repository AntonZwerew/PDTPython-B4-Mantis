from fixture.application import Application
from fixture.db import DbFixture
from fixture.orm import ORMHelper
import pytest
import json
import os.path
import importlib
import jsonpickle

fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as f:
            target = json.load(f)
    return target


@pytest.fixture
def app(request):
    global fixture
    browser = request.config.getoption("--browser")
    config_app = load_config(request.config.getoption("--target"))["app"]
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=config_app["baseurl"],
                              username=config_app["username"], password=config_app["password"])
    # fixture.session.ensure_login(username=config_app["username"], password=config_app["password"])
    return fixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def finalizer():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(finalizer)
    return fixture


@pytest.fixture(scope="session")
def db(request):
    config_db = load_config(request.config.getoption("--target"))["db"]
    dbfixture = DbFixture(host=config_db["host"], name=config_db["name"],
                          user=config_db["user"], password=config_db["password"])

    def finalizer():
        dbfixture.destroy()
    request.addfinalizer(finalizer)
    return dbfixture


@pytest.fixture(scope="session")
def orm(request):
    config_db = load_config(request.config.getoption("--target"))["db"]
    orm_fixture = ORMHelper(host=config_db["host"], name=config_db["name"],
                            user=config_db["user"], password=config_db["password"])

    def finalizer():
        # dbfixture.destroy()
        pass
    request.addfinalizer(finalizer)
    return orm_fixture


@pytest.fixture
def check_ui(request):
    return request.config.getoption("--check_ui")


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--target", action="store", default="target.json")
    parser.addoption("--check_ui", action="store_true")


def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            testdata = load_from_module(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])
        elif fixture.startswith("json_"):
            testdata = load_from_json(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])


def load_from_module(module):
    return importlib.import_module("data.%s" % module).testdata


def load_from_json(file):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.json" % file)) as f:
        return jsonpickle.decode(f.read())
