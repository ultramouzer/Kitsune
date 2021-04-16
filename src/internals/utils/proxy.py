import config
import random
import logging

def get_proxy():
    if config.proxies and len(config.proxies):
        proxy = random.choice(config.proxies)
        return {
            "http": proxy,
            "https": proxy
        }
    else:
        return None
