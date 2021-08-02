import random
import logging

from configs.derived_vars import proxy_list

def get_proxy():
    if proxy_list and len(proxy_list):
        proxy = random.choice(proxy_list)
        return {
            "http": proxy,
            "https": proxy
        }
    else:
        return None
