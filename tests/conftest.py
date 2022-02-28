import csv
from os import getenv

from dotenv import load_dotenv
from flask import Flask
from pytest import fail, fixture

from tests.database_for_reset import default_products

load_dotenv(dotenv_path="tests/.env.example")

FILEPATH = getenv("FILEPATH")


def reset_database():
    with open(FILEPATH, "w") as products_csv:
        fieldnames = ["id", "name", "price"]
        csv_dict_writer = csv.DictWriter(products_csv, fieldnames=fieldnames)
        csv_dict_writer.writeheader()
        csv_dict_writer.writerows(default_products)


@fixture
def database_filename():
    return FILEPATH


@fixture
def app():
    try:
        return __import__("app").app
    except ModuleNotFoundError:
        fail('Verifique se o arquivo "app.py" existe na raiz do projeto')
    except AttributeError:
        fail('Verifique se a variável "app" existe dentro do arquivo "app.py"')


@fixture
def client(app: Flask):
    with app.test_client() as client:
        reset_database()
        return client


@fixture
def app_get_routes(app: Flask):
    return app.url_map.bind("", default_method="GET")


@fixture
def app_post_routes(app: Flask):
    return app.url_map.bind("", default_method="POST")


@fixture
def app_patch_routes(app: Flask):
    return app.url_map.bind("", default_method="PATCH")


@fixture
def app_delete_routes(app: Flask):
    return app.url_map.bind("", default_method="DELETE")
