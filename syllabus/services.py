import os
import requests
from dotenv import load_dotenv
from requests.exceptions import HTTPError, Timeout
from rest_framework import status


def get_prod_id(title, description):
    """
    Функция принимает параметры отдельного продукта и возвращает id данного продукта в виде строки.
    """

    load_dotenv()
    url = os.getenv("PRODUCTS_URL")
    headers = {"Authorization": f"Bearer {os.getenv('STRIPE_SECRET_KEY')}"}
    data = {"name": title, "description": description}
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
    except ConnectionError as err:
        return f"{err}"
    except Timeout:
        return "Request timed out"
    except HTTPError as err:
        return f"HTTP error occurred: {err}"
    if response.status_code == status.HTTP_200_OK:
        data_response = response.json()
        return data_response.get("id")


def get_price_id(product_id, amount):
    """
    Функция принимает id продукта и стоимость единицы продукта, а возвращает id цены в виде строки.
    """

    load_dotenv()
    url = os.getenv("PRICES_URL")
    headers = {"Authorization": f"Bearer {os.getenv("STRIPE_SECRET_KEY")}"}
    data = {
        "currency": "rub",
        "product": product_id,
        "unit_amount": int(amount * 100),
    }
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
    except ConnectionError as err:
        return f"{err}"
    except Timeout:
        return "Request timed out"
    except HTTPError as err:
        return f"HTTP error occurred: {err}"
    if response.status_code == status.HTTP_200_OK:
        data_response = response.json()
        return data_response.get("id")


def get_session(price_id):
    """
    Функция принимает id цены данного продукта, а возвращает объект текущей платежной сессии в виде словаря.
    """

    load_dotenv()
    url = os.getenv("SESSIONS_URL")
    headers = {"Authorization": f"Bearer {os.getenv("STRIPE_SECRET_KEY")}"}
    line_items = [
        {
            "price": price_id,
            "quantity": 1,
        },
    ]
    data = {
        "success_url": "https://localhost:8080/",
        "line_items[0][price]": line_items[0]["price"],
        "line_items[0][quantity]": line_items[0]["quantity"],
        "mode": "payment",
    }
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
    except ConnectionError as err:
        return f"{err}"
    except Timeout:
        return "Request timed out"
    except HTTPError as err:
        return f"HTTP error occurred: {err}"
    if response.status_code == status.HTTP_200_OK:
        data_response = response.json()
        return data_response
