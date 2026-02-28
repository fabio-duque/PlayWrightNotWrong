
from playwright.sync_api import sync_playwright
import json
import time

def run():
    with sync_playwright() as p:
        # Abrindo o navegador (recomendo False para você ver o que está travando)
        browser = p.chromium.launch(headless=False) 
        page = browser.new_page()

        try:
            print("Acessando o site...")
            page.goto("https://www.mercadolivre.com.br", wait_until="networkidle", timeout=60000)

            # Tenta encontrar o campo de busca por diferentes seletores
            # O ML às vezes usa 'as_word' ou 'search'
            search_box = page.wait_for_selector('input.nav-search-input', timeout=15000)

            print("Digitando pesquisa...")
            search_box.fill('pedal de guitarra')
            search_box.press('Enter')

            # Aguarda os resultados
            print("Aguardando resultados...")
            page.wait_for_selector('.ui-search-layout__item', timeout=20000)

            produtos = page.query_selector_all('.ui-search-layout__item')
            dados = []

            for item in produtos[:20]:
                try:
                    # Seletores mais genéricos para garantir a captura
                    nome = item.query_selector('.ui-search-item__title').inner_text()
                    # Captura o preço inteiro
                    preco_elem = item.query_selector('.andes-money-amount__fraction')
                    preco = preco_elem.inner_text() if preco_elem else "N/A"

                    dados.append({"Produto": nome, "Preco_R$": preco})
                except:
                    continue

            # Salva em um arquivo temporário para o Notebook ler
            with open("dados_ml.json", "w", encoding="utf-8") as f:
                json.dump(dados, f)

            print(f"Sucesso! {len(dados)} produtos encontrados.")

        except Exception as e:
            print(f"Erro durante a execução: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run()
