import requests
from bs4 import BeautifulSoup

def main():
    res = requests.get('https://ve.soccerway.com/venezuela/liga-futve-2005-2006/resultados/')
    soup = BeautifulSoup(res.content, 'html.parser')
    print(soup.prettify())  



if __name__ == "__main__":
    main()