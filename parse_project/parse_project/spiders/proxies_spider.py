import scrapy


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

            item['dirty_elements'] = proxy.css('td')[1].css('span style::text').extract()[0].split()
            item['inline_elements'] = list(filter(lambda s: 'none' not in s, item['dirty_elements']))
            item['clear_elements'] = list(map(lambda s: s.split('{')[0][1:], item['inline_elements']))

            item['spans_garbage'] = proxy.css('td')[1].css('span').extract()
            item['divs'] = proxy.css('td')[1].css('span div').extract()

            yield item

