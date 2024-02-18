import re

import bs4

from itemadapter import ItemAdapter


class GueuzeOnlyFilter:
    def __init__(self, feed_options):
        self.feed_options = feed_options

    def accepts(self, item):
        gueuze_in_description = ("description" in item
                                 and re.match(r'.*(gueuz|geuz|lambi|kriek|).*', item["description"], re.IGNORECASE))
        gueuze_in_title = ("title" in item
                           and re.match(r'.*(gueuz|geuz|lambi|kriek|).*', item["title"], re.IGNORECASE))

        if gueuze_in_description or gueuze_in_title:
            return True
        return False


class TweedehandsPipeline:
    def __init__(self):
        self.items_count = 0

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        field_names = adapter.field_names()
        for field_name in field_names:
            # clean the title
            if field_name == 'title':
                value = adapter[field_name] if adapter[field_name] else ''
                adapter[field_name] = value.capitalize()

            # clean the price
            if field_name == 'price':
                value = adapter[field_name] if adapter[field_name] else ''
                value = re.sub(r'[^\d,]', '', value).replace(',', '.')
                try:
                    value = float(value)
                except ValueError:
                    value = None
                adapter[field_name] = value

            # clean the location
            if field_name == 'location':
                value = adapter[field_name] if adapter[field_name] else ''
                adapter[field_name] = value.capitalize()

            # clean the description
            if field_name == 'description':
                value = adapter[field_name] if adapter[field_name] else ''
                soup = bs4.BeautifulSoup(value.replace('<br>', ' '), parser='lxml', features="lxml")
                value = soup.get_text()
                adapter[field_name] = value.strip()

            # clean the url
            if field_name == 'url':
                value = adapter[field_name] if adapter[field_name] else ''
                adapter[field_name] = value

        return item
