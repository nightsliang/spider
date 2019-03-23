# -*- coding: utf-8 -*-
import scrapy
# 1. 导入Item类
from tencent.items import TencentItem

"""
1. 生成腾讯scrapy爬虫项目
    scrapy startproject tencent
2. 生成腾讯招聘爬虫
   cd tencent
   scrapy genspider hr tencent.com
3. 完善爬虫
   3.1. 完善起始URL
   3.2  完善解析函数
4. 处理数据


使用Item类
1. 导入Item类
2. 创建Item类对象
3. 使用: 与字典相同

"""

class HrSpider(scrapy.Spider):
    name = 'hr'
    allowed_domains = ['tencent.com']

    #   3.1. 完善起始URL
    start_urls = ['https://hr.tencent.com/position.php']

    def parse(self, response):
        # 3.2  完善解析函数
        # 职位名称, 职位类别, 发布时间信息
        # 1. 获取包含职位信息的标签列表
        trs = response.xpath('//*[@id="position"]/div[1]/table/tr')[1:-1]
        # print(len(trs))
        # tbody: 是浏览器在渲染的时候自动添加的, 在响应页面中没有tbody.
        # 2. 遍历标签列表, 获取需要的数据
        for tr in trs:
            # 定义字典, 用于存储招聘信息
            # item = {}
            # 2. 创建Item类对象
            item = TencentItem()
            # 职位名称
            item['name'] = tr.xpath('./td[1]/a/text()').extract_first()
            # 职位类别
            item['category'] = tr.xpath('./td[2]/text()').extract_first()
            # 发布时间信息
            item['publish_date'] = tr.xpath('./td[last()]/text()').extract_first()
            # print(item)
            # 把数据交给引擎
            yield item

        # 实现翻页:
        # 1. 提取下一页的URL
        next_url = response.xpath('//*[@id="next"]/@href').extract_first()
        print(next_url)
        if next_url != 'javascript:;':
            # "position.php?&start=10#a"
            # 如果有下一页, 补全URL
            next_url = 'https://hr.tencent.com/' + next_url
            print(next_url)
            # 2. 构建请求对象, 交给引擎
            # callback: 用于指定URL对应的响应数据的解析函数
            # 由于第1页, 和后面所有页的页面结构都是一样的, 就可用使用同一个解析函数, 进行解析
            yield scrapy.Request(next_url, callback=self.parse)
