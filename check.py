from data import config


def is_admin(user_id):
    if not user_id == config.admin_id:
        raise Exception('Отказано в доступе!')