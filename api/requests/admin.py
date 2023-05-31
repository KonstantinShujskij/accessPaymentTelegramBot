from api.request import send_admin_request
from data import config
from utils import Struct


def create_access(name, course, min_value, max_value):
    end_point = '/api/access/create'
    url = config.API_URL + end_point

    body = {
        'name': name,
        'course': course,
        'min': min_value,
        'max': max_value,
        'access': {
            'make': True
        }
    }

    data = send_admin_request(url, body)
    access = Struct(**data)

    return access


def refresh_access(access_id):
    end_point = '/api/access/refresh'
    url = config.API_URL + end_point

    body = {'id': access_id}

    data = send_admin_request(url, body)
    access = Struct(**data)

    return access


def get_orders(start, stop, partner_id):
    end_point = '/api/admin/get-orders'
    url = config.API_URL + end_point

    body = {'timeStart': start, 'timeStop': stop, 'partner': partner_id}

    data = send_admin_request(url, body)
    orders = []

    for order in data:
        orders.append(Struct(**order))

    return orders
