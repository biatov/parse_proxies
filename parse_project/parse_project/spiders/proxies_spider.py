import scrapy
from parse_project.search import get_ip


class ProxiesSpider(scrapy.Spider):
    name = "proxies"
    start_urls = [
        'http://proxylist.hidemyass.com/',
    ]

    def parse(self, response):

        page = response.url.split("/")[-2]
        filename = 'proxies-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)

        for proxy in response.selector.css('table.hma-table tbody tr'):
            item = dict()

            item['port'] = proxy.css('td')[2].xpath('text()').extract()[0].strip()

            dirty_elements = proxy.css('td')[1].css('span style::text').extract()[0].split()
            inline_elements = list(filter(lambda s: 'none' not in s, dirty_elements))
            clear_elements = list(map(lambda s: s.split('{')[0][1:], inline_elements))

            spans_garbage = proxy.css('td')[1].css('span').extract()
            divs = proxy.css('td')[1].css('span div').extract()

            div = divs
            span = spans_garbage[1:]
            garbage = spans_garbage[:1]

            item['ip'] = get_ip(garbage, span, div, clear_elements)

            yield item

