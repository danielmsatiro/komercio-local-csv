import csv
from random import randint

from flask.testing import FlaskClient
from pytest import mark


@mark.parametrize("test_id", [1, 8, 13, 15, 21, 30])
def test_existed_id(client: FlaskClient, database_filename: str, test_id: int):
    with open(database_filename, "r") as products_csv:
        payload = list(csv.reader(products_csv))[test_id]

    response = client.delete(
        f"/products/{test_id}",
    )
    expected = {
        "id": int(payload[0]),
        "name": payload[1],
        "price": float(payload[2]),
    }

    with open(database_filename, "r") as products_csv:
        products = list(csv.reader(products_csv))
        for product in products:
            if product[0] == test_id:
                delete_product = product
        else:
            delete_product = None

    assert (
        response.status_code == 200
    ), "Verifique se está retornando 200 quando bem sucedido na rota DELETE /products"
    assert (
        response.json == expected
    ), f"Verifique se a mensagem de sucesso de DELETE /products/{test_id} está formatada corretamente"
    assert (
        delete_product == None
    ), f"Verifique se o product_id {test_id} foi deletado corretamente no fim do arquivo .cvs"


def test_id_not_found(client: FlaskClient, database_filename: str):
    test_id = randint(31, 100)

    response = client.delete(
        f"/products/{test_id}",
    )
    expected = {"error": f"product id {test_id} not found"}

    assert (
        response.status_code == 404
    ), f"Verifique se está retornando 404 error na rota DELETE /products/{test_id}"
    assert (
        response.json == expected
    ), f"Verifique se a mensagem de erro de DELETE /products/{test_id} está formatada corretamente"
