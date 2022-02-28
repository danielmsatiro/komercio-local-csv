from flask.testing import FlaskClient


def test_without_query_params(client: FlaskClient):
    response = client.get("/products")

    assert (
        response.status_code == 200
    ), "Verifique se está retornando 200 quando bem sucedido na rota GET /products"
    assert response.json == [
        {"id": 1, "name": "sabonete", "price": 5.99},
        {"id": 2, "name": "perfume", "price": 39.9},
        {"id": 3, "name": "tapete", "price": 10.3},
    ], "Verifique se a mensagem de sucesso de GET /products está formatada corretamente"


def test_with_query_params(client: FlaskClient):
    response = client.get("/products?page=3&per_page=4")

    assert (
        response.status_code == 200
    ), "Verifique se está retornando 200 quando bem sucedido na rota GET /products?page=3&per_page=4"
    assert response.json == [
        {"id": 9, "name": "bola", "price": 25.99},
        {"id": 10, "name": "cantil", "price": 55.99},
        {"id": 11, "name": "copo", "price": 5.99},
        {"id": 12, "name": "panela", "price": 25.99},
    ], "Verifique se a mensagem de sucesso de GET /products?page=3&per_page=4 está formatada corretamente"


def test_specific_product(client: FlaskClient):
    response = client.get("/products/5")

    assert (
        response.status_code == 200
    ), "Verifique se está retornando 200 quando bem sucedido na rota GET /products"
    assert response.json == {
        "id": 5,
        "name": "chuveiro",
        "price": 119.19,
    }, "Verifique se a mensagem de sucesso de GET /products está formatada corretamente"
