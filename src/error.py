from data import data


class InputError(Exception):
    pass


class AccessError(Exception):
    pass


def clear():
    data['users'] = []
    data['channels'] = []
