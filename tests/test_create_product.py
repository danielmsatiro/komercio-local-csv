import csv

from flask.testing import FlaskClient


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
