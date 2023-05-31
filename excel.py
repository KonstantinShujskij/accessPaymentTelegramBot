import pandas as pd

from utils import parse_date


def create_report(orders, file_name):
    data = {
        'id': [],
        'value': [],
        'card': [],
        'currency': [],
        'course': [],
        'status': [],
        'maker': [],
        'create': [],
        'update': []
    }

    for order in orders:
        data['id'].append(order.id)
        data['value'].append(order.value)
        data['card'].append(order.card),
        data['currency'].append(order.currency),
        data['course'].append(order.course),
        data['status'].append(order.status),
        data['maker'].append(order.maker),
        data['create'].append(parse_date(order.create)),
        data['update'].append(parse_date(order.update)),

    df = pd.DataFrame({
        'Id': data['id'],
        'Value': data['value'],
        'Card': data['card'],
        'Currency': data['currency'],
        'Course': data['course'],
        'Status': data['status'],
        'Maker': data['maker'],
        'Create': data['create'],
        'Update': data['update']
    })

    df.to_excel(f"./{file_name}.xlsx")

    return open(f"./{file_name}.xlsx", 'rb')
