import os
import sys
import json
import requests

def get_token(username, password):
    payload = f"{{\"username\":\"{username}\",\"password\":\"{password}\"}}"
    token_api = 'https://services.packtpub.com/auth-v1/users/tokens'

    r = requests.post(token_api, data=payload)
    json = r.json()

    if json is not None:
        if 'data' in json and 'access' in json['data']:
            access = json['data']['access']
            return access
    return None


def get_products(access, offset, limit):
    products = []
    product_api = f'https://services.packtpub.com/entitlements-v1/users/me/products?sort=createdAt:DESC&offset={offset}&limit={limit}'
    headers = {
        "accept":"application/json, text/plain, */*",
        "accept-language":"en-US,en;q=0.9",
        "authorization":f"Bearer {access}",
        "sec-fetch-mode":"cors",
        "sec-fetch-site":"same-site"
    }
    r = requests.get(product_api, headers=headers)
    json = r.json()

    if json is not None:
        if 'data' in json:
            for item in json['data']:
                productName = item['productName']
                productId = item['productId']
                products.append({'productName': productName, 'productId': productId})
    return products


def download(access, product, api):
    productId = product['productId']
    productName = product['productName']
    
    api = f'https://services.packtpub.com/products-v1/products/{productId}/files/{api}'
    headers = {
        "accept":"application/json, text/plain, */*",
        "accept-language":"en-US,en;q=0.9",
        "authorization":f"Bearer {access}",
        "sec-fetch-mode":"cors",
        "sec-fetch-site":"same-site"
    }
    r = requests.get(api, headers=headers)
    json = r.json()
    
    if json is not None:
        if 'data' in json:
            r = requests.get(json['data'])
            
            return r.content


def download_epub(access, product, path):
    data = download(access, product, 'epub')
    productName = product['productName']
    
    if data is not None:
        with open(f'{path}/{productName}.epub', 'wb') as file:
            file.write(data)


def download_mobi(access, product, path):
    data = download(access, product, 'mobi')
    productName = product['productName']
    
    if data is not None:
        with open(f'{path}/{productName}.mobi', 'wb') as file:
            file.write(data)


def download_pdf(access, product, path):
    data = download(access, product, 'pdf')
    productName = product['productName']
    
    if data is not None:
        with open(f'{path}/{productName}.pdf', 'wb') as file:
            file.write(data)


def download_code(access, product, path):
    data = download(access, product, 'code')
    productName = product['productName']
    
    if data is not None:
        with open(f'{path}/{productName}_Code.zip', 'wb') as file:
            file.write(data)


def get_access():
    # Get username/passwords
    with open('access.json', 'rt') as json_file:
        data = json_file.read()
        data = json.loads(data)
        username = data['username']
        password = data['password']
    return get_token(username, password)


def download_all_books():
    access = get_access()

    # Make download dir if not exist
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    
    # Start from 0
    start = 0
    while True:
        products = get_products(access, start, 10)
        if len(products) == 0:
            break
        
        for product in products:
            download_book(product)
        start += 10
    print('All done.')


def download_book(access, product):
    name = product['productName']
    path = f'downloads/{name}'

    if not os.path.exists(path):
        os.makedirs(path)

    download_epub(access, product, path)
    download_mobi(access, product, path)
    download_pdf(access, product, path)
    download_code(access, product, path)

    print(f'Downloading {name} done.')


def download_one_book(productName, productId):
    access = get_access()

    # Make download dir if not exist
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    
    product = {'productName': productName, 'productId': productId}
    download_book(access, product)
    
def main():
    download_all_books()
    # download_one_book('Learn Linux Shell Scripting - Fundamentals of Bash 4.4', '9781788995597')


if __name__ == '__main__':
    if len(sys.argv) == 3:
        print(f"Downloading {sys.argv[1]}")
        download_one_book(sys.argv[1], sys.argv[2])
    else:
        main()

