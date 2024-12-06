import time
import random

def rolar_pagina_ate_fim(driver):
    altura_inicial = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(random.uniform(1, 2))
        altura_atual = driver.execute_script("return document.body.scrollHeight")
        if altura_atual == altura_inicial:
            break
        altura_inicial = altura_atual
