
from playwright.sync_api import sync_playwright
import json

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.mercadolivre.com.br")

        page.fill('input[name="as_word"]', 'pedal de guitarra')
        page.press('input[name="as_word"]', 'Enter')

        page.wait_for_selector('.ui-search-layout__item')

        produtos = page.query_selector_all('.ui-search-layout__item')
        dados = []

        for item in produtos[:10]:
            try:
                nome = item.inner_text('.ui-search-item__title')
                preco = item.inner_text('.andes-money-amount__fraction')
                dados.append({"Produto": nome, "Preco": preco})
            except:
                continue

        browser.close()
        print(json.dumps(dados)) # Retorna os dados como string JSON

if __name__ == "__main__":
    run()
