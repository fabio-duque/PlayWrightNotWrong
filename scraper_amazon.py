
from playwright.sync_api import sync_playwright
import json
import time

def run():
    with sync_playwright() as p:
        # Abrimos o navegador com um User Agent comum para evitar bloqueios
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(user_agent=user_agent)
        page = context.new_page()

        try:
            print("Acessando Amazon Brasil...")
            page.goto("https://www.amazon.com.br", wait_until="domcontentloaded", timeout=60000)

            # Busca o produto
            search_box = page.wait_for_selector('#twotabsearchtextbox', timeout=20000)
            search_box.fill('pedal de guitarra')
            search_box.press('Enter')

            # Aguarda os resultados carregarem (container principal da busca)
            page.wait_for_selector('[data-component-type="s-search-result"]', timeout=20000)
            time.sleep(2) # Pausa para renderização de preços

            # Coleta os blocos de produtos
            items = page.query_selector_all('[data-component-type="s-search-result"]')

            dados = []
            for item in items:
                try:
                    # Título na Amazon geralmente está em um h2
                    titulo_elem = item.query_selector('h2 a span')
                    # Preço: Classe padrão para o valor inteiro
                    preco_inteiro = item.query_selector('.a-price-whole')
                    preco_fracao = item.query_selector('.a-price-fraction')

                    if titulo_elem and preco_inteiro:
                        preco_txt = preco_inteiro.inner_text().replace(',', '').replace('.', '')
                        fracao_txt = preco_fracao.inner_text() if preco_fracao else "00"

                        dados.append({
                            "Produto": titulo_elem.inner_text().strip(),
                            "Preço (R$)": f"{preco_txt},{fracao_txt}"
                        })
                except Exception:
                    continue

            with open("dados_amazon.json", "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False)

            print(f"Sucesso! {len(dados)} produtos encontrados na Amazon.")

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run()
