import random
import aiohttp
import asyncio
from bs4 import BeautifulSoup


# заносим категории хабра
HABR_CATEGORIES = [
    'https://habr.com/ru/hub/programming',
    'https://habr.com/ru/hub/python'
]

# получаем прокси из файла в виде списка
# with open('proxy.txt') as file:
#     PROXY_LIST = ''.join(file.readlines()).split('\n')

# send_request с проки
# async def send_request(url, proxy) -> str:
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url, proxy=f'http://{proxy}') as resp:
#             return await resp.text(encoding='utf-8')


async def send_request(url) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text(encoding='utf-8')


async def parse_category(category_url):
    html_response = await send_request(url=category_url)
    soup = BeautifulSoup(html_response, 'lxml')
    pagination_block = soup.find('div', class_='tm-pagination__pages')
    pages_count = pagination_block.find_all('a', class_='tm-pagination__page')[-1].text.strip()
    print(f'category: {category_url} | pages_count: {pages_count}')

    for page in range(int(pages_count)):
        page_response = await send_request(
            url=f'{category_url}/page{page}/'
        )
        soup_page = BeautifulSoup(page_response, 'lxml')
        articles = soup_page.find_all('article', class_='tm-articles-list__item')

        for article in articles:
            info_block = article.find('a', class_='tm-title__link')
            title = info_block.find('span').text.strip()
            link = f'https://habr.com{info_block.get("href")}'

            with open('articles.txt', 'a', encoding='utf-8') as file:
                category_name = category_url.split('/')[-1]
                result_string = f'{category_name} | {title} | {link}\n'
                file.write(result_string)
                print(result_string, end='')


async def main():
    data = [parse_category(category) for category in HABR_CATEGORIES]
    # т.к. это карутина, то будет создаваться объект. чтобы он заработал нужно вызвать через await
    await asyncio.gather(*data)


if __name__ == '__main__':
    # вызов используя прокси
    # res = asyncio.run(send_request('http://duckduckgo.com', random.choice(PROXY_LIST)))
    # res = asyncio.run(send_request('http://duckduckgo.com'))
    # proxy = random.choice(PROXY_LIST)
    # print(proxy)
    # site = 'http://icanhazip.com'
    # res = asyncio.run(send_request(site))
    # print(res)
    asyncio.run(main())


