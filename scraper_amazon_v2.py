
from playwright.sync_api import sync_playwright
import json
import time

def run():
    with sync_playwright() as p:
        # Abre o navegador visível para você ver o que acontece
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
        page = context.new_page()

        try:
            print("Abrindo Amazon Brasil...")
            # Vai direto para a página de busca
            page.goto("https://www.amazon.com.br", wait_until="domcontentloaded")

            # ESPERA IMPORTANTE: Se aparecer CAPTCHA, resolva na tela agora!
            print("Aguardando carregamento dos itens (Resolva o CAPTCHA se aparecer)...")
            page.wait_for_selector('div[data-component-type="s-search-result"]', timeout=30000)

            # Rola a página para carregar preços que ficam 'escondidos'
            page.evaluate("window.scrollBy(0, 800)")
            time.sleep(2)

            items = page.query_selector_all('div[data-component-type="s-search-result"]')
            dados = []

            for item in items:
                try:
                    # Seletores focados na estrutura da Amazon
                    titulo = item.query_selector('h2 span').inner_text()
                    preco_inteiro = item.query_selector('.a-price-whole')

                    if titulo and preco_inteiro:
                        valor = preco_inteiro.inner_text().strip().replace('\n', '')
                        dados.append({"Produto": titulo[:70] + "...", "Preço (R$)": valor})
                except:
                    continue

            # Salva o resultado em JSON
            with open("dados_amazon.json", "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False)

            print(f"Sucesso! {len(dados)} produtos encontrados.")

        except Exception as e:
            print(f"Erro durante a extração: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run()
