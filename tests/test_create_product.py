import csv
from typing import Dict

from flask.testing import FlaskClient
from pytest import mark


def test_thirty_products(client: FlaskClient, database_filename: str):
    payload = {"name": "teste", "price": 15.99}
    response = client.post("/products", json=payload)
    expected = {
        "id": 31,
        "name": "teste",
        "price": 15.99,
    }

    with open(database_filename, "r") as products_csv:
        last_product = list(csv.reader(products_csv))[-1]

    assert (
        response.status_code == 201
    ), "Verifique se está retornando 201 quando bem sucedido na rota POST /products"
    assert (
        response.json == expected
    ), "Verifique se a mensagem de sucesso de POST /products está formatada corretamente"
    assert [
        str(value) for value in expected.values()
    ] == last_product, (
        "Verifique se o product_id 31 foi inserido corretamente no fim do arquivo .cvs"
    )


def test_thirty_products_and_deleted_product_id_5(
    client: FlaskClient, database_filename: str
):
    with open(database_filename, "r") as products_csv:
        products = list(csv.reader(products_csv))
        with open(database_filename, "w") as products_csv:
            buffer = csv.writer(products_csv)
            buffer.writerows([row for row in products if "5" not in row])
    payload = {"name": "teste", "price": 15.99}
    response = client.post("/products", json=payload)
    expected = {
        "id": 31,
        "name": "teste",
        "price": 15.99,
    }

    with open(database_filename, "r") as products_csv:
        last_product = list(csv.reader(products_csv))[-1]

    assert (
        response.status_code == 201
    ), "Verifique se está retornando 201 quando bem sucedido na rota POST /products"
    assert (
        response.json == expected
    ), "Verifique se a mensagem de sucesso de POST /products está formatada corretamente"
    assert [
        str(value) for value in expected.values()
    ] == last_product, (
        "Verifique se o product_id 31 foi inserido corretamente no fim do arquivo .cvs"
    )


def test_thirty_one_products(client: FlaskClient, database_filename: str):
    with open(database_filename, "a") as products_csv:
        buffer = csv.writer(products_csv)
        buffer.writerow(["31", "teste1", "37.00"])

    payload = {"name": "teste2", "price": 52.69}
    response = client.post("/products", json=payload)
    expected = {
        "id": 32,
        "name": "teste2",
        "price": 52.69,
    }

    with open(database_filename, "r") as products_csv:
        last_product = list(csv.reader(products_csv))[-1]

    assert (
        response.status_code == 201
    ), "Verifique se está retornando 201 quando bem sucedido na rota POST /products"
    assert (
        response.json == expected
    ), "Verifique se a mensagem de sucesso de POST /products está formatada corretamente"
    assert [
        str(value) for value in expected.values()
    ] == last_product, (
        "Verifique se o product_id 32 foi inserido corretamente no fim do arquivo .cvs"
    )


@mark.parametrize(
    "payload",
    [
        {"name1": "teste", "price2": 52.69},
        {"name": "teste", "price2": 52.69},
        {"name1": "teste", "price": 52.69},
        {"name1": "teste"},
        {"name": "teste"},
        {"price1": 52.69},
        {"price": 52.69},
        {},
    ],
)
def test_without_correct_keys(
    client: FlaskClient, database_filename: str, payload: Dict
):
    response = client.post("/products", json=payload)
    expected = {"error": "Algum dado não está de acordo"}

    with open(database_filename, "r") as products_csv:
        last_product = list(csv.reader(products_csv))[-1]

    assert (
        response.status_code == 400
    ), "Verifique se está retornando 400 quando error na rota POST /products"
    assert (
        response.json == expected
    ), "Verifique se a mensagem de error de POST /products está formatada corretamente"
    assert [
        [31].extend(payload.values())
    ] != last_product, (
        "Verifique se foi evitada a inserção de um novo produto no fim do arquivo .cvs"
    )
    pass


@mark.parametrize(
    "payload",
    [
        {"name": "teste", "price": 52.69, "teste": 5.7},
        {"name": "teste", "price": 52.69, "teste": 5.7, "teste2": "teste2"},
    ],
)
def test_with_more_keys(client: FlaskClient, database_filename: str, payload: Dict):
    response = client.post("/products", json=payload)
    expected = {"id": 31, "name": payload["name"], "price": payload["price"]}

    with open(database_filename, "r") as products_csv:
        last_product = list(csv.reader(products_csv))[-1]

    assert (
        response.status_code == 201
    ), "Verifique se está retornando 201 quando bem sucedido na rota POST /products"
    assert (
        response.json == expected
    ), "Verifique se a mensagem de sucesso de POST /products está formatada corretamente"
    assert [
        str(value) for value in expected.values()
    ] == last_product, (
        "Verifique se o product_id 31 foi inserido corretamente no fim do arquivo .cvs"
    )
