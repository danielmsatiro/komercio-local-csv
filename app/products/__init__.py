from os import getenv
from flask import jsonify
import math
import csv

def get_products_csv(product_id,page,per_page):
    FILEPATH = getenv('FILEPATH')
    data = []
    
    with open(FILEPATH,'r') as products_csv:
        csv_dict_reader = csv.DictReader(products_csv)

        for row in csv_dict_reader:
            data.append(row)

    if product_id:
        product = [product for product in data if product['id']==product_id]
        return jsonify(*product)

    if type(page)==str or type(per_page)==str:
        return {'msg': f'Algum dado não está de acordo'}, 400

    number_of_pages = math.ceil(len(data)/per_page)
    pages = [data[index*per_page:(index+1)*per_page] for index in range(number_of_pages)]
    
    if page > number_of_pages:
        return {'msg': f'Ultrapassou o número de páginas.', 'Nº da última página': number_of_pages}, 400
    
    return jsonify(pages[page-1]),200