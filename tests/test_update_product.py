import csv
from random import randint
from typing import Dict

from flask.testing import FlaskClient
from pytest import mark


@mark.parametrize(
    "test_id,payload",
    [
        (1, {"name": "teste", "price": 15.99}),
        (8, {"name": "teste"}),
        (13, {"price": 15.99}),
        (15, {"name1": "teste", "price": 15.99}),
        (21, {"name": "teste", "price": 15.99, "price2": 15.99}),
        (30, {}),
    ],
)
def test_existed_id(
    client: FlaskClient, database_filename: str, test_id: int, payload: Dict
):
    with open(database_filename, "r") as products_csv:
        updated_product = list(csv.reader(products_csv))[test_id]

    expected = {
        "id": test_id,
        "name": payload.get("name", updated_product[1]),
        "price": payload.get("price", float(updated_product[2])),
    }
    response = client.patch(f"/products/{test_id}", json=payload)

    with open(database_filename, "r") as products_csv:
        updated_product = list(csv.reader(products_csv))[test_id]

    assert (
        response.status_code == 200
    ), "Verifique se está retornando 200 quando bem sucedido na rota PATCH /products"
    assert (
        response.json == expected
    ), "Verifique se a mensagem de sucesso de PATCH /products está formatada corretamente"
    assert sorted(str(value) for value in expected.values()) == sorted(
        updated_product
    ), f"Verifique se o product_id {test_id} foi inserido corretamente no fim do arquivo .cvs"


def test_id_not_found(client: FlaskClient, database_filename: str):
    test_id = randint(31, 100)
    payload = {"name": "teste", "price": 15.99}
    response = client.patch(f"/products/{test_id}", json=payload)
    expected = {"error": f"product id {test_id} not found"}

    assert (
        response.status_code == 404
    ), "Verifique se está retornando 404 quando id_test não existente"
    assert (
        response.json == expected
    ), f"Verifique se a mensagem de error de PATCH /products{test_id} está formatada corretamente"
