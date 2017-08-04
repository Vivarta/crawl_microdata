# -*- coding: utf-8 -*-
import scrapy


class MicrodataSpider(scrapy.Spider):
    name = 'microdata'
    start_urls = [
        'http://variety.com/2017/film/features/detroit-kathryn-bigelow-john-boyega-1202511077/',
        'http://www.mynet.com/haber/guncel/abdullah-gulden-mehmet-gormez-aciklamasi-3177125-1',
        'http://www.newsweek.com/trumps-voter-fraud-commission-doesnt-know-what-doing-state-official-644804',
    ]

    def parse(self, response):
        for itemscope in response.xpath('//*[@itemscope][@itemtype]'):
            item = {"itemtype": itemscope.xpath('@itemtype').extract()[0]}
            item["item_id"] = int(float(itemscope.xpath("""count(preceding::*[@itemscope])
                                                        + count(ancestor::*[@itemscope])
                                                        + 1""").extract()[0]))
            properties = []
            for itemprop in itemscope.xpath("""set:difference(.//*[@itemprop],
                                                            .//*[@itemscope]//*[@itemprop])"""):
                property = {"itemprop": itemprop.xpath('@itemprop').extract()[0]}
                if itemprop.xpath('@itemscope'):
                    property["value_ref"] = {
                        "item_id": int(float(itemprop.xpath("""count(preceding::*[@itemscope])
                                                            + count(ancestor::*[@itemscope])
                                                            + 1""").extract()[0]))
                    }
                else:
                    value = itemprop.xpath('normalize-space(.)').extract()[0]
                    if value:
                        property["value"] = value
                attributes = []
                for index, attribute in enumerate(itemprop.xpath('@*'), start=1):
                    propname = itemprop.xpath('name(@*[%d])' % index).extract()[0]
                    if propname not in ("itemprop", "itemscope"):
                        attributes.append((propname, attribute.extract()))
                if attributes:
                    property["attributes"] = dict(attributes)
                properties.append(property)
            item["properties"] = properties
            yield item
