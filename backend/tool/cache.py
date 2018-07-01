from django.core.cache import cache

def set_login_account(id, account):
    cache.set('login_account_' + str(id), account)

def get_login_account(id):
    return cache.get('login_account_' + str(id))