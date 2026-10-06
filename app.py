"""
Help Desk — Sistema de Triagem de Saúde Pública
Aplicativo desktop usando PyWebView.
"""

import webview
from api import Api
import os


def main():
    api = Api()

    # Caminho absoluto do index.html
    base_dir = os.path.abspath(os.path.dirname(__file__))
    html_path = os.path.join(base_dir, "frontend", "index.html")

    # Verifica se o arquivo existe
    if not os.path.exists(html_path):
        print(f"ERRO: Arquivo não encontrado em: {html_path}")
        print("\nArquivos na pasta atual:")
        for item in os.listdir(base_dir):
            print(f"  {item}")
        if os.path.exists(os.path.join(base_dir, "frontend")):
            print("\nArquivos na pasta frontend:")
            for item in os.listdir(os.path.join(base_dir, "frontend")):
                print(f"  {item}")
        return

    # Cria a janela do aplicativo
    window = webview.create_window(
        title="HelpMed — Triagem de Saúde Pública",
        url=html_path,
        js_api=api,
        width=1100,
        height=700,
        min_size=(900, 600),
    )

    webview.start(debug=True)


if __name__ == "__main__":
    main()