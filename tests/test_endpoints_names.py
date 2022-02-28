from random import randint


def test_route_get_exists(app_get_routes):
    assert app_get_routes.match(
        "/products"
    ), 'Verifique se existe uma rota "/products apta para GET"'
    assert app_get_routes.match(
        f"/products/{randint(1,100)}"
    ), 'Verifique se existe uma rota "/products/<product_id apta para GET"'


def test_route_post_exists(app_post_routes):
    assert app_post_routes.match(
        "/products"
    ), 'Verifique se existe uma rota "/products apta para POST"'


def test_route_patch_exists(app_patch_routes):
    assert app_patch_routes.match(
        f"/products/{randint(1,100)}"
    ), 'Verifique se existe uma rota "/products/<product_id apta para PATCH"'


def test_route_delete_exists(app_delete_routes):
    assert app_delete_routes.match(
        f"/products/{randint(1,100)}"
    ), 'Verifique se existe uma rota "/products/<product_id apta para DELETE"'
