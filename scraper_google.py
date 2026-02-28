
from playwright.sync_api import sync_playwright
import json
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
        page = context.new_page()

        try:
            print("Abrindo Google...")
            page.goto("https://www.google.com.br")

            # Aceita cookies se aparecer (comum em novas instâncias)
            try:
                page.click('button:has-text("Aceitar tudo")', timeout=3000)
            except:
                pass

            # Digita a busca
            search_box = page.wait_for_selector('textarea[name="q"]', timeout=10000)
            search_box.fill('pedal de guitarra preço')
            search_box.press('Enter')

            # Espera os resultados de "Shopping" ou resultados orgânicos
            page.wait_for_selector('#search', timeout=10000)
            time.sleep(2)

            # Extrai os títulos e links dos resultados orgânicos principais
            results = page.query_selector_all('div.g')
            dados = []

            for res in results[:8]: # Pega os 8 primeiros
                titulo_elem = res.query_selector('h3')
                link_elem = res.query_selector('a')

                if titulo_elem and link_elem:
                    dados.append({
                        "Título": titulo_elem.inner_text(),
                        "Link": link_elem.get_attribute('href')
                    })

            with open("dados_google.json", "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False)

            print(f"Sucesso! {len(dados)} links encontrados no Google.")

        except Exception as e:
            print(f"Erro no Google: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run()
