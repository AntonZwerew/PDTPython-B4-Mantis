from fixture.application import Application
from fixture.db import DbFixture
from fixture.orm import ORMHelper
import pytest
import json
import os.path
import importlib
import jsonpickle
import ftputil

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
def app(request, config):
    global fixture
    browser = request.config.getoption("--browser")
    config_app = config["app"]
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, config=config)
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
def config(request):
    return load_config(request.config.getoption("--target"))


@pytest.fixture(scope="session", autouse=True)
def configure_ftp_server(request, config):
    install_server_configuration(config["ftp"]["host"], config["ftp"]["username"], config["ftp"]["password"])

    def finalizer():
        restore_server_configuration(config["ftp"]["host"], config["ftp"]["username"], config["ftp"]["password"])
    request.addfinalizer(finalizer)


# Можно ли вместо замены всего файла изменять только строчку с настройкой капчи?
def install_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            remote.remove("config_inc.php.bak")
        if remote.path.isfile("config_inc.php"):
            remote.rename("config_inc.php", "config_inc.php.bak")
        remote.upload(os.path.join(os.path.dirname(__file__), "resources\\config_inc.php"), "config_inc.php")


def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php"):
            remote.remove("config_inc.php")
        if remote.path.isfile("config_inc.php.bak"):
            remote.rename("config_inc.php.bak", "config_inc.php")


@pytest.fixture(scope="session")
def db(request, config):
    config_db = config["db"]
    dbfixture = DbFixture(host=config_db["host"], name=config_db["name"],
                          user=config_db["user"], password=config_db["password"])

    def finalizer():
        dbfixture.destroy()
    request.addfinalizer(finalizer)
    return dbfixture


@pytest.fixture(scope="session")
def orm(request, config):
    config_db = config["db"]
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
