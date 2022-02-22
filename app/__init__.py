from flask import Flask, request
from app.products import get_products_csv

app = Flask(__name__)

@app.get('/products')
@app.get('/products/<product_id>')
def products(product_id=None):
    page = request.args.get("page")
    per_page = request.args.get("per_page")

    try:
        page = int(page)
        per_page = int(per_page)
    finally:
        return get_products_csv(product_id, page or 1, per_page or 3)
    


""" @app.post('/products')

@app.patch('/products/<product_id>')

@app.delete('/products/<product_id>') """