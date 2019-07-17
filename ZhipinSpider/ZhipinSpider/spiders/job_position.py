# -*- coding: utf-8 -*-
import scrapy
from ZhipinSpider.items import ZhipinspiderItem

class JobPositionSpider(scrapy.Spider):
    # 定义该蜘蛛的名字
    name = 'job_position'
    # 定义该蜘蛛允许爬取域名
    allowed_domains = ['zhipin.com']
    # 定义该蜘蛛爬取的首页列表
    start_urls = ['https://www.zhipin.com/c101280600/?ka=sel-city-101280600']

    # 该方法负责提取response所包含的信息
    # response 代表下载器从 start_urls 中的每个URL下载得到的响应
    def parse(self, response):
        # 遍历页面中所有 //div[@class="job-primary"]节点
        for job_primary in response.xpath('//div[@class="job-primary"]'):
            item = ZhipinspiderItem()

            # 匹配 //div[@class="job-primary"]节点下的 /div[@class="info-primary"]节点
            # 也就是匹配到包含工作信息的<div.../>元素
            info_primary = job_primary.xpath('./div[@class="info-primary"]')
            item['title'] = info_primary.xpath('./h3/a/div[@class="job-title"]/text()').extract_first()
            item['salary'] = info_primary.xpath('./h3/a/span[@class="red"]/text()').extract_first()
            item['work_addr'] = info_primary.xpath('./p/text()').extract_first()
            item['url'] = info_primary.xpath('./h3/a/@href').extract_first()

            # 匹配 //div[@class="job-primary"]节点下 ./div[@class="info-company"] 节点下
            # 的 /div[@class="company-text" 节点
            # 也就是匹配到包含公司信息的<div.../>元素
            company_text = job_primary.xpath('./div[@class="info-company"]/div[@class="company-text"]')
            item['company'] = company_text.xpath('./h3/a/text()').extract_first()
            company_info = company_text.xpath('./p/text()').extract()
            if company_info and len(company_info) > 0:
                item['industry'] = company_text.xpath('./p/text()').extract()[0]
            if company_info and len(company_info) > 1:
                item['company_size'] = company_text.xpath('./p/text()').extract()[2]
            
            # 匹配 //div[@class="job-primary"]节点下的 /div[@class="info-publis"]节点
            # 也就是匹配到包含发布人信息的<div.../>元素
            info_publis = job_primary.xpath('./div[@class="info-publis"]')
            item['recruiter'] = info_publis.xpath('./h3/text()').extract_first()
            yield item
        
        # 解析下一页链接
        new_links = response.xpath('//div[@class="page"]/a[@class="next"]/@href').extract()
        if new_links and len(new_links) > 0:
            # 获取下一页的链接
            new_links = new_links[0]
            # 再次发送请求获取下一页数据
            yield scrapy.Request("http://www.zhipin.com" + new_links,callback = self.parse)


