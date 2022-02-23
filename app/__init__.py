from flask import Flask, request
from app.products import get_products_csv, create_product_csv, update_product_csv, delete_product_csv

app = Flask(__name__)

@app.get('/products')
@app.get('/products/<int:product_id>')
def products(product_id=None):
    page = request.args.get("page")
    per_page = request.args.get("per_page")

    try:
        page = int(page)
        per_page = int(per_page)
    finally:
        return get_products_csv(product_id, page or 1, per_page or 3)

@app.post('/products')
def create_product():
    data = request.get_json()
    return create_product_csv(data)

@app.patch('/products/<int:product_id>')
def update_product(product_id):
    data = request.get_json()
    return update_product_csv(data, product_id)


@app.delete('/products/<int:product_id>')
def delete_product(product_id):
    return delete_product_csv(product_id)