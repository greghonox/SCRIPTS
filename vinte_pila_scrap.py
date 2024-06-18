# %%
from re import findall
from bs4 import BeautifulSoup
from requests import Session, Response
import logging
import coloredlogs

# %%
URL_BASE = 'https://www.vintepila.com.br/'

# %%
data_login = {
    "log": "",
    "miniorange_login_nonce": "",
    "redirect_to": "https://www.vintepila.com.br/minha-conta/",
    "pwd": "wUC5NY/2E6",
    "miniorange_login_nonce": "",
}
session = Session()
log = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
coloredlogs.install(level="INFO", logger=log)

# %%
def get_request(url: str, cookies: dict = None, **args: dict) -> Response:
    return session.get(url, cookies=cookies, **args)

def post_request(url: str, cookies: dict = None, data: dict = None, **args: dict) -> Response:
    return session.post(url, cookies=cookies, data=data, **args)

# %%
def login_page():
    return session.post(URL_BASE + 'login/?wpe-login=btcuser', data=data_login)

# %%
def get_pages() -> int:
    response = get_request(URL_BASE+'trabalhos-freelance')
    soup = BeautifulSoup(response.text, 'html.parser')
    pages = soup.find_all('a', class_='page-numbers')[2].text
    return int(pages)


# %%
def extract_data_link(url: str, page: int) -> list:
    response = get_request(url + 'trabalhos-freelance?page={}'.format(page))
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('div', class_='ui segment')
    return [link.find('a')['href'] for link in links if link.find('a')]


# %%
extract_name_candidate = lambda soup: soup.find('div', class_='header').text

def get_content_page(url: str) -> dict:
    response = get_request(url)
    if response.status_code != 200:
        return {}
    response.status_code
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find_all('div', class_='header')[1].text
    description = soup.find('div', class_='description').text
    candidate = soup.find('div', class_='extra').find_all('span')[2].text
    data_published = soup.find('div', class_='extra').find_all('span')[0].text
    price = soup.find_all('span', class_='ui green header')[0].text.split(' ')[-1][:-1]
    project = soup.find_all('div', class_='ui fluid container')[0].find('span').text.split(' ')[-1]
    delivery = soup.find('span', {'data-content':'Prazo máximo estipulado pelo cliente para a entrega do serviço'}).text
    candiatures_name = [extract_name_candidate(candidate) for candidate in soup.find_all('div', class_='ui segment')]
    return {'title': title,
            'candiates_name': candiatures_name,
            'description': description,
            'price': price,
            'data_published': data_published,
            'candidate': candidate,
            'delivery': delivery,
            'project': project,
            'link': url
    }


# %%
def caditate_job(url: str, price: str, delivery: str, associate_project_id: str) ->bool:
    url += 'wp-admin/admin-ajax.php'
    payload = {
        "price": price,
        "delivery": delivery,
        "action": "custom_project_offer_submit",
        "formrandomid": "1",
        "user": "652909",
        "associate_project_id": associate_project_id,
    }
    response = post_request(url, data=payload)
    if response.status_code != 200:
        log.error(f'Error found with {payload} and {url}')
        return False
    log.info(f'Candidated with success in {url}, {payload}')
    return True
   

# %%
login_page()
pages = get_pages()
for page in range(1, pages+1):
    log.warn(f'change page: {page}')
    links = extract_data_link(URL_BASE, page)
    for link in links:
        response = get_content_page(link)
        if 'Gregorio h.' not in response['candiates_name']:
            caditate_job(URL_BASE, response['price'], response['delivery'], response['project'])
            log.info(response)


