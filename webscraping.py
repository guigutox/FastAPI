import requests
from bs4 import BeautifulSoup
from database import get_db
from model import Model_Menu

def scrape():
    # URL da página que contém as categorias
    url = "https://ufu.br/graduacao"
    
    # Realiza uma requisição HTTP GET para a URL
    response = requests.get(url)
    
    # Cria um objeto BeautifulSoup para fazer parsing do HTML
    soup = BeautifulSoup(response.content, "html.parser")

    categorias = []

    # Seleciona todos os elementos de menu usando um seletor CSS
    for item in soup.select("#block-menu-block-2 ul.menu li.leaf a"):
        # Obtém o texto do link
        menuNav = item.get_text()
        # Constrói o link absoluto para a categoria
        link = "https://ufu.br" + item['href']
        # Adiciona a categoria à lista
        categorias.append({"menuNav": menuNav, "link": link})

    return categorias

def saveDB(categorias):
    # Obtém uma instância do banco de dados
    db = next(get_db())

    # Itera sobre cada categoria e a adiciona ao banco de dados
    for categoria in categorias:
        nova_categoria = Model_Menu(
            menuNav=categoria["menuNav"],
            link=categoria["link"]
        )
        # Adiciona a nova categoria à sessão do banco de dados
        db.add(nova_categoria)
    
    # Salva todas as mudanças no banco de dados
    db.commit()
    # Fecha a conexão com o banco de dados
    db.close()

if __name__ == "__main__":
    # Executa a função de scraping para obter as categorias
    categorias = scrape() 
    # Salva as categorias no banco de dados
    saveDB(categorias)
