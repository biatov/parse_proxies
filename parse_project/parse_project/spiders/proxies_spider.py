import scrapy

from parse_project.search import get_ip, without_style_garb
from parse_project.items import ParseProjectItem
from parse_project.pipelines import ParseProjectPipeline


class ProxiesSpider(scrapy.Spider):
    name = "proxies"

    allowed_domains = ['http://proxylist.hidemyass.com/']
    start_urls = [
        'http://proxylist.hidemyass.com/1#listable',
    ]

    def parse(self, response):

        for proxy in response.selector.css('table.hma-table tbody tr'):
            item = ParseProjectItem()

            dirty_elements = proxy.css('td')[1].css('span style::text').extract()[0].split()
            inline_elements = list(filter(lambda s: 'none' not in s, dirty_elements))
            clear_elements = list(map(lambda s: s.split('{')[0][1:], inline_elements))

            spans_garbage = proxy.css('td')[1].css('span').extract()

            div = proxy.css('td')[1].css('span div').extract()  # [<div...>...</div>...</div>]
            span = spans_garbage[1:]  # [<span...>...</span>...</span>]
            garbage = spans_garbage[:1]  # [<style>...<span>...<div>]

            item['ip_address'] = get_ip(garbage, span, div, clear_elements)
            item['port'] = proxy.css('td')[2].xpath('text()').extract()[0].strip()

            record_to_db = ParseProjectPipeline()
            record_to_db.process_item(item, scrapy.Spider)

            yield item

