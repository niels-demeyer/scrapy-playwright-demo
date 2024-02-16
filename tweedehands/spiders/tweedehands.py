import os
from random import random

import scrapy
from scrapy_playwright.page import PageMethod

from tweedehands.items import TweedehandsItem
from tweedehands.settings import TWEEDHANDS_USERNAME, TWEEDHANDS_PASSWORD

screenshot = "./log/screenshots/"  # folder to save the screenshots


class TweedeHandsSpider(scrapy.Spider):
    name = 'tweedehands'

    def start_requests(self):
        screenhot_path = os.path.join(screenshot, "after_login.png")
        url = "https://www.2dehands.be/account/login.html?target=https%3A%2F%2Fwww.2dehands.be%2F"
        yield scrapy.Request(
            url,
            callback=self.logged_in,
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                errback=self.errback,
                playwright_page_methods=[
                    PageMethod('wait_for_timeout', 10000),
                    PageMethod('screenshot', path=os.path.join(screenshot, "before_login.png"), full_page=True),
                    PageMethod('fill', 'input[name=j_username]', value=TWEEDHANDS_USERNAME),
                    PageMethod('fill', 'input[name=j_password]', value=TWEEDHANDS_PASSWORD),
                    PageMethod('click', '#account-login-button'),
                    PageMethod('wait_for_timeout', 10000),
                    PageMethod('screenshot', path=os.path.join(screenshot, "after_login.png"), full_page=True),
                ],

            )
        )

    async def logged_in(self, response):
        page = response.meta["playwright_page"]
        await page.close()
        yield scrapy.Request(
            "https://www.2dehands.be/my-account/saved-searches/index.html",
            callback=self.parse_my_search_links,
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod('wait_for_timeout', 10000),
                    PageMethod('screenshot', path=os.path.join(screenshot, "my_searches.png"), full_page=True),
                ],
                errback=self.errback,
            )
        )

    async def parse_my_search_links(self, response):
        page = response.meta["playwright_page"]
        await page.close()
        links = response.css('.SavedSearchesContainer-searches_overview a::attr(href)').getall()
        counter = 0
        for link in links:
            counter += 1
            yield scrapy.Request(
                link,
                callback=self.parse_my_search_lists,
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        PageMethod('wait_for_timeout', 10000),
                        PageMethod(
                            'screenshot',
                            path=os.path.join(screenshot, f"my-searh-list-{counter}.png"),
                            full_page=True
                        ),
                    ],
                    errback=self.errback,
                )
            )

    async def parse_my_search_lists(self, response):
        """parse the search list results: get the ad links and the next page link"""
        page = response.meta["playwright_page"]
        await page.close()

        # get the ad links
        add_links = response.css('li.hz-Listing a.hz-Listing-coverLink::attr(href)').getall()
        add_links = [f"https://www.2dehands.be{link}" for link in add_links]
        for add_link in add_links:
            yield scrapy.Request(
                add_link,
                callback=self.parse_add,
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        PageMethod('wait_for_timeout', 10000),
                    ],
                    errback=self.errback,
                )
            )

        # get next page
        next_page_css_selector = '.hz-PaginationControls-pagination a:has(i.hz-SvgIconArrowRight)::attr(href)'
        next_page_link = response.css(next_page_css_selector).get()
        next_page_link = f"https://www.2dehands.be{next_page_link}"
        yield scrapy.Request(
            next_page_link,
            callback=self.parse_my_search_lists,
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod('wait_for_timeout', 10000),
                    # generate a random number to avoid overwriting the same file
                    PageMethod(
                        'screenshot',
                        path=os.path.join(screenshot, f"next-page-{random()}.png"),
                        full_page=True),
                ],
                errback=self.errback,
            )
        )

    async def parse_add(self, response):
        page = response.meta["playwright_page"]
        await page.close()

        item = TweedehandsItem()
        item['title'] = response.css('h1.Listing-title::text').get()
        item['price'] = response.css('div.Listing-root div.Listing-price::text').get()
        item['description'] = response.css('div.Description-root div.Description-description').get()
        item['location'] = response.css('div.SellerInfo-rowWithIcon:has(i.hz-SvgIconLocation) span::text').get()
        item['url'] = response.url
        yield item

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
