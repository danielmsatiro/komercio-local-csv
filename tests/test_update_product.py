import csv
from random import randint

from flask.testing import FlaskClient
from pytest import mark


@mark.parametrize("test_id", [1, 8, 13, 15, 21, 30])
def test_existed_id(client: FlaskClient, database_filename: str, test_id: int):
    payload = {"name": "teste", "price": 15.99}
    response = client.patch(f"/products/{test_id}", json=payload)
    expected = {
        "id": test_id,
        "name": "teste",
        "price": 15.99,
    }

    with open(database_filename, "r") as products_csv:
        last_product = list(csv.reader(products_csv))[test_id]

    assert (
        response.status_code == 200
    ), "Verifique se está retornando 200 quando bem sucedido na rota PATCH /products"
    assert (
        response.json == expected
    ), "Verifique se a mensagem de sucesso de PATCH /products está formatada corretamente"
    assert [
        str(value) for value in expected.values()
    ] == last_product, f"Verifique se o product_id {test_id} foi inserido corretamente no fim do arquivo .cvs"


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

