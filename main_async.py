import os
import json
import aiohttp
import asyncio
import requests


def get_access():
    if not os.path.isfile('access.json'):
        with open('access.json', 'wt') as json_file:
            json_file.write('{ "username":"", "password":"" }')

    # Get username/passwords
    with open('access.json', 'rt') as json_file:
        data = json_file.read()
        data = json.loads(data)
        username = data['username']
        password = data['password']

        if len(username) == 0 or len(password) == 0:
            print("[Error] Username or Password is empty in access.json file.")
            return None
    return get_token(username, password)


def get_token(username, password):
    payload = f"{{\"username\":\"{username}\",\"password\":\"{password}\"}}"
    token_api = 'https://services.packtpub.com/auth-v1/users/tokens'

    r = requests.post(token_api, data=payload)
    json = r.json()

    if json is not None:
        if 'data' in json and 'access' in json['data']:
            token = json['data']['access']
            return token
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


async def fetch(session, token, product, api):
    productId = product['productId']
    productName = product['productName']
    
    url = f'https://services.packtpub.com/products-v1/products/{productId}/files/{api}'
    headers = {
        "accept":"application/json, text/plain, */*",
        "accept-language":"en-US,en;q=0.9",
        "authorization":f"Bearer {token}",
        "sec-fetch-mode":"cors",
        "sec-fetch-site":"same-site"
    }

    async with session.get(url, headers=headers) as response:
        json = await response.json()
    
    if json is not None and 'data' in json:
        timeout = aiohttp.ClientTimeout()
        async with session.get(json['data'], timeout=timeout) as response:
            try:
                return await response.content.read()
            except(aiohttp.ClientPayloadError) as e:
                print(response.content.exception())
                print(f"{productName} for {api} has failed")
    return None


async def fetch_epub(session, token, product, path):
    productName = product['productName']
    content = await fetch(session, token, product, "epub")
    if content:
        with open(f'{path}/{productName}.epub', 'wb') as fd:
            fd.write(content)


async def fetch_mobi(session, token, product, path):
    productName = product['productName']
    content = await fetch(session, token, product, "mobi")
    if content:
        with open(f'{path}/{productName}.mobi', 'wb') as fd:
            fd.write(content)


async def fetch_pdf(session, token, product, path):
    productName = product['productName']
    content = await fetch(session, token, product, "pdf")
    if content:
        with open(f'{path}/{productName}.pdf', 'wb') as fd:
            fd.write(content)


async def fetch_code(session, token, product, path):
    productName = product['productName']
    content = await fetch(session, token, product, "code")
    if content:
        with open(f'{path}/{productName}_Code.zip', 'wb') as fd:
            fd.write(content)


async def download_task(token, products):
    timeout = aiohttp.ClientTimeout(total=15*60)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = []
        for product in products:
            name = product['productName']
            path = f'downloads/{name}'

            if not os.path.exists(path):
                os.makedirs(path)

            # tasks.append(fetch_epub(session, token, product, path))
            # tasks.append(fetch_mobi(session, token, product, path))
            # tasks.append(fetch_pdf(session, token, product, path))
            tasks.append(fetch_code(session, token, product, path))
            # Will wait for all tasks to complete
        await asyncio.gather(*tasks)


def download_all_books():
    access = get_access()
    if access is not None:
        # Make download dir if not exist
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        print("Getting products ...")
        # Start from 0
        start = 0
        limit = 10
        products = []
        while True:
            current_page = get_products(token, start, limit)
            if len(current_page) == 0:
                break
            
            for product in current_page:
                products.append(product)
            start += limit

        print("Getting books ...")
        asyncio.run(download_task(token, products))


if __name__ == '__main__':
    download_all_books()

