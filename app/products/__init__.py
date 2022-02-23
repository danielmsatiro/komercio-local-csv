from hmac import new
from os import getenv
from flask import jsonify
import math
import csv

FILEPATH = getenv('FILEPATH')

def extract_formated_products():
    data = []

    with open(FILEPATH,'r') as products_csv:
        csv_dict_reader = csv.DictReader(products_csv)

        for row in csv_dict_reader:
            formated_row = row.copy()
            for key, value in formated_row.items():
                if key=='id': formated_row.update({key: int(value)})
                if key=='price': formated_row.update({key: float(value)})

            data.append(formated_row)

    return data

def get_products_csv(product_id,page,per_page):
    data_csv = extract_formated_products()

    if product_id:     
        product = [product for product in data_csv if product['id']==product_id]
        return jsonify(*product)

    if isinstance(page,str) or isinstance(per_page,str):
        return {'msg': f'Algum dado não está de acordo'}, 400

    number_of_pages = math.ceil(len(data_csv)/per_page)
    pages = [data_csv[index*per_page:(index+1)*per_page] for index in range(number_of_pages)]
    
    if page > number_of_pages:
        return {'msg': f'Ultrapassou o número de páginas.', 'Nº da última página': number_of_pages}, 400
    
    return jsonify(pages[page-1]),200

def create_product_csv(payload):
    #check payload
    error = ({'msg': f'Algum dado não está de acordo'}, 400)
    if 'name' not in payload or 'price' not in payload: return error
    for key in payload.keys():
        if key not in ['name','price']:
            return error
    if type(payload['price'])!=float: return error

    data_csv = extract_formated_products()
    payload.update({'id': data_csv[-1]['id']+1})

    with open(FILEPATH,'a') as products_csv:
        fieldnames = ['id','name','price']
        csv_dict_writer = csv.DictWriter(products_csv, fieldnames=fieldnames)
        csv_dict_writer.writerow(payload)
         
    return payload, 201

def update_product_csv(payload, product_id):
    #check payload:
    error = ({'msg': f'Algum dado não está de acordo'}, 400)
    for key in payload.keys():
        if key not in ['name','price']:
            return error
    if type(payload['price'])!=float: return error
    
    data_csv = extract_formated_products()
    new_data_csv = []
    
    #Search the product:
    not_found = ({'error': f'product id {product_id} not found'}, 404)
    for product in data_csv:
        if product['id']==product_id:
            product.update(payload)
            new_data_csv.append(product)
            break
        else:
            new_data_csv.append(product)
    else:
        return not_found

    #Reuse the previous loop if it breaks before finishing data_csv:
    if len(data_csv) != len(new_data_csv):
        for product in data_csv[len(new_data_csv):]:
            new_data_csv.append(product)
    
    with open(FILEPATH,'w') as products_csv:
        fieldnames = ['id','name','price']
        csv_dict_writer = csv.DictWriter(products_csv, fieldnames=fieldnames)
        csv_dict_writer.writeheader()
        csv_dict_writer.writerows(new_data_csv)
        
    return payload

def delete_product_csv(product_id):
    data_csv = extract_formated_products()
    new_data_csv = []
    deleted_product = None

    #Search the product:
    not_found = ({'error': f'product id {product_id} not found'}, 404)
    for product in data_csv:
        if product['id']==product_id:
            deleted_product = product
            break
        else:
            new_data_csv.append(product)
    else:
        return not_found
    
    #Reuse the previous loop if it breaks before finishing data_csv:
    if len(data_csv)-1 != len(new_data_csv):
        for product in data_csv[len(new_data_csv)+1:]:
            new_data_csv.append(product)
    
    with open(FILEPATH,'w') as products_csv:
        fieldnames = ['id','name','price']
        csv_dict_writer = csv.DictWriter(products_csv, fieldnames=fieldnames)
        csv_dict_writer.writeheader()
        csv_dict_writer.writerows(new_data_csv)

    return deleted_product


