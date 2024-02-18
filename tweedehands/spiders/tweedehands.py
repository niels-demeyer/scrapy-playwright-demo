import logging
import os
from random import random

import scrapy
from scrapy_playwright.page import PageMethod

from tweedehands.items import TweedehandsItem
from tweedehands.settings import TWEEDHANDS_USERNAME, TWEEDHANDS_PASSWORD

screenshot = "./log/screenshots/"  # folder to save the screenshots

DELAY = 5000

# The links of the adds will only be generated in the html if the add is hovered
# bellow is the hover script to trigger all the add links to be generated
hover_script = """
document.querySelectorAll('li.hz-Listing a.hz-Listing-coverLink').forEach(function(element) {
  // Trigger mouseover event
  element.dispatchEvent(new MouseEvent('mouseover', {
    'view': window,
    'bubbles': true,
    'cancelable': true
  }));
});
"""


class TweedeHandsSpider(scrapy.Spider):
    name = 'tweedehands'


    excluded_domains = ['www.2dehands.benone']

    def start_requests(self):
        """Start the spider by logging in to the website and call the logged_in method."""

        # remove all the screenshots from the previous run
        screenshot_path = os.path.join('log', 'screenshots')
        for file in os.listdir(screenshot_path):
            os.remove(os.path.join(screenshot_path, file))

        url = "https://www.2dehands.be/account/login.html?target=https%3A%2F%2Fwww.2dehands.be%2F"
        logging.info(f"loading log in page {url} and logging in.")
        yield scrapy.Request(  # login in call back logged in with the response
            url,
            callback=self.logged_in,
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                errback=self.errback,
                playwright_page_methods=[
                    PageMethod('wait_for_timeout', DELAY),
                    PageMethod('screenshot', path=os.path.join(screenshot, "before_login.png"), full_page=True),
                    PageMethod('fill', 'input[name=j_username]', value=TWEEDHANDS_USERNAME),
                    PageMethod('fill', 'input[name=j_password]', value=TWEEDHANDS_PASSWORD),
                    PageMethod('screenshot', path=os.path.join(screenshot, "about_to_login.png"), full_page=True),
                    PageMethod('click', '#account-login-button'),
                    PageMethod('wait_for_timeout', DELAY),
                    PageMethod('screenshot', path=os.path.join(screenshot, "after_login.png"), full_page=True),
                ],
            )
        )

    async def logged_in(self, response):
        """After logging in, go to the saved searches page. and call parse_my_search_links"""
        page = response.meta["playwright_page"]
        await page.close()

        url = "https://www.2dehands.be/my-account/saved-searches/index.html"
        logging.info(f"loading saved searches page {url}")
        yield scrapy.Request(  # load saved searches and call back parse_my_search_links
            url,
            callback=self.parse_my_search_links,
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod('wait_for_timeout', DELAY),
                    PageMethod('screenshot', path=os.path.join(screenshot, "my_searches.png"), full_page=True),
                ],
                errback=self.errback,
            )
        )

    async def parse_my_search_links(self, response):
        """parse the saved searches page and get all the saved
        searches links and call parse_my_search_lists for them"""
        page = response.meta["playwright_page"]
        await page.close()
        links = response.css('.SavedSearchesContainer-searches_overview a::attr(href)').getall()
        logging.info(f"found {len(links)} saved search links on {response.url}")
        counter = 0
        for link in links:
            counter += 1
            logging.info(f"loading saved search link: {link}")
            yield scrapy.Request(  # load a search list and call back parse_my_search_lists
                link,
                callback=self.parse_my_search_lists,
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        PageMethod('wait_for_timeout', DELAY),
                        PageMethod("evaluate", hover_script),
                        PageMethod('wait_for_timeout', 1000),
                        # take a screenshot for debugging
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
        """parse the search list:
            get all the add links and call parse_add for them
            get the next page link and recurse by calling parse_my_search_lists"""
        page = response.meta["playwright_page"]
        await page.close()

        # get the ad links
        add_links = response.css('li.hz-Listing a.hz-Listing-coverLink::attr(href)').getall()

        logging.info(f"found {len(add_links)} add links on search page: {response.url}")
        add_links = [f"https://www.2dehands.be{link}" for link in add_links]
        for add_link in add_links:
            logging.info(f"loading add link: {add_link}")
            yield scrapy.Request(
                add_link,
                callback=self.parse_add,
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        PageMethod('wait_for_timeout', DELAY),
                        # take a screenshot for debugging
                        # PageMethod(
                        #     'screenshot',
                        #     path=os.path.join(screenshot, f"add-{random()}.png"),
                        #     full_page=True
                        # ),
                    ],
                    errback=self.errback,
                )
            )

        # get next page
        next_page_css_selector = '.hz-PaginationControls-pagination a:has(i.hz-SvgIconArrowRight)::attr(href)'
        next_page_link = response.css(next_page_css_selector).get()
        next_page_link = f"https://www.2dehands.be{next_page_link}" if next_page_link else None
        logging.info(f"found next page link: {next_page_link} on {response.url}")
        if next_page_link:
            logging.info(f"loading next page: {next_page_link}")
            yield scrapy.Request(
                next_page_link,
                callback=self.parse_my_search_lists,
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        PageMethod('wait_for_timeout', 10000),
                        # take a screenshot for debugging
                        PageMethod(
                            'screenshot',
                            path=os.path.join(screenshot, f"next-page-{random()}.png"),
                            full_page=True
                        ),
                    ],
                    errback=self.errback,
                )
            )

    async def parse_add(self, response):
        """parse the add page and yield the TweedehandsItem"""
        page = response.meta["playwright_page"]
        await page.close()

        item = TweedehandsItem()
        item['title'] = response.css('h1.Listing-title::text').get()
        item['price'] = response.css('div.Listing-root div.Listing-price::text').get()
        item['description'] = response.css('div.Description-root div.Description-description').get()
        item['location'] = response.css('div.SellerInfo-rowWithIcon:has(i.hz-SvgIconLocation) span::text').get()
        item['url'] = response.url
        logging.info(f"yielding item: {item.get('title', item)}")
        yield item

    async def errback(self, failure):
        logging.error(f"Error callback An error occurred: {failure.getErrorMessage()}, closing playwright page.")
        page = failure.request.meta["playwright_page"]
        await page.close()
