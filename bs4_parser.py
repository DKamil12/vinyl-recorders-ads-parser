import requests
from bs4 import BeautifulSoup

'''
Этот парсер находит все объявления по запросу "виниловый проигрыватель" в Алматы на сйте www.olx.kz
Извлекаемые данные: название объявления, месторасположение и цена. 
'''

def get_html(url : str):
    try:
        response = requests.get(url)
        return response.text
    except Exception as e:
        print(f'Something went wrong when calling {url}. The error: {e}')
        return None


# a function to get html items by passing a tag and a classname
def get_items(soup: BeautifulSoup, tag: str, classname: str) -> list[str] | None:
    items = []

    try:
        all_tags = soup.find_all(tag, classname)
        if tag == 'a':
            for tag in all_tags:
                items.append(tag.get('href'))
        else:
            for tag in all_tags:
                items.append(tag.text)
        
        return items
    except Exception as e:
        print('Something went wrong:', e)
        return None


def get_pager(soup: BeautifulSoup) -> int | None:
    try:
        pager = int(soup.find('ul', 'pagination-list').find_all('a')[-2].text)
        return pager
    except Exception as e:
        print('Something went wrong:', e)
        return None


def write_data_to_file(bs: BeautifulSoup) -> None:
    # get product details
    product_titles = get_items(soup=bs, tag='h6', classname='css-1wxaaza')
    product_locations = get_items(soup=bs, tag='p', classname='css-1mwdrlh')
    product_prices = get_items(soup=bs, tag='p', classname='css-13afqrm')

    # write parsed data to a file
    try:
        with open('./parsed_data.txt', 'a', encoding="utf-8") as file:
            for i in range(len(product_titles)):
                file.write(f"{product_titles[i]},\n {product_locations[i]},\n {product_prices[i]},\n\n")
    except Exception as e:
        print(e)


def parse_product(url: str, filter: str) -> None:
    html = get_html(url + filter)
    
    if html:
        bs = BeautifulSoup(html, 'html.parser')

        # call a func to write data
        write_data_to_file(bs=bs)
        
        pager = get_pager(bs)

        # check if pager exists
        if pager:
            for i in range(2, pager + 1):
                # create new url by adding page number and filter
                new_url = url + f'page={i}' + '&' + filter
                html = get_html(new_url)
                bs = BeautifulSoup(html, 'html.parser')

                # call a func to write data
                write_data_to_file(bs=bs)
    else:
        print('Something went wrong!')


url = 'https://www.olx.kz/alma-ata/q-виниловый-проигрыватель/?'
# filter to remove ads about repair services, because they don't have price including tag
filter = 'search%5Bfilter_float_price:from%5D=10'
parse_product(url, filter)
