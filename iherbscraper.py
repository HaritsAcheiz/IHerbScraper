import asyncio
import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass, field
from typing import List
from random import choice

@dataclass
class IHerbScraper:
    useragent: List[str] = field(default_factory=lambda: [
        'Mozilla/5.0 (Wayland; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.137 Safari/537.36 Ubuntu/22.04 (5.0.2497.35-1) Vivaldi/5.0.2497.35',
        'Mozilla/5.0 (Wayland; Linux x86_64; System76 Galago Pro (galp2)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.175 Safari/537.36 Ubuntu/22.04 (5.0.2497.48-1) Vivaldi/5.0.2497.48',
        'Mozilla/5.0 (Wayland; Linux x86_64; System76 Galago Pro (galp2)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.175 Safari/537.36 Ubuntu/22.04 (5.0.2497.51-1) Vivaldi/5.0.2497.51,',
        'Mozilla/5.0 (Wayland; Linux x86_64; System76) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36 Ubuntu/22.04 (5.2.2623.34-1) Vivaldi/5.2.2623.39',
        'Mozilla/5.0 (Wayland; Linux x86_64; System76) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.92 Safari/537.36 Ubuntu/22.04 (5.2.2623.34-1) Vivaldi/5.2.2623.34'
    ])
    proxies: List[str] = field(default_factory=lambda: [
        '192.126.194.95:8800', '154.12.113.202:8800', '154.12.113.32:8800', '192.126.196.93:8800', '192.126.196.137:8800',
        '154.12.113.169:8800', '154.12.112.208:8800', '154.12.112.163:8800', '192.126.194.135:8800', '154.12.113.91:8800'
    ])

    async def fetch(self, client, url):
        # async with client.get(url) as r:
        #     if r.status_code != 200:
        #         r.raise_for_status()
        #     return await r.text()
        r = await client.get(url)
        if r.status_code != 200:
            r.raise_for_status()
        return r.text

    async def fetch_all(self, client, urls):
        tasks = []
        for url in urls:
            task = asyncio.create_task(self.fetch(client, url))
            tasks.append(task)
        response = await asyncio.gather(*tasks)
        return response

    async def extract(self):
        proxy = choice(self.proxies)

        proxies = {
            "http://": f"http://{proxy}",
            "https://": f"http://{proxy}",
        }

        ua = choice(self.useragent)
        headers = {
            'user-agent': ua
        }

        urls = []
        for page in range(1, 2):
            url = f'https://www.iherb.com/specials?p={page}'
            urls.append(url)

        async with httpx.AsyncClient(headers=headers, proxies=proxies, timeout=10) as client:
            htmls = await self.fetch_all(client, urls)
        return htmls

if __name__ == '__main__':
    scraper = IHerbScraper()
    htmls = asyncio.run(scraper.extract())
    print(htmls)