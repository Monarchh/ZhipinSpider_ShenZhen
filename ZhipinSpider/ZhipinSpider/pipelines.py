# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class ZhipinspiderPipeline(object):
    # 定义构造器，初始化要写入的文件
    def __init__(self):
        self.json_file = open("job_position.json", "wb+")
        self.json_file.write('[\n'.encode("utf-8"))
    # 重写close_spider回调方法，用于关闭文件
    def close_spider(self, spider):
        print('----------关闭文件----------')
        # 后退两个字符，也就是去掉最后一条记录之后的换行符和逗号
        self.json_file.seek(-2, 1)
        self.json_file.write('\n]'.encode("utf-8"))
        self.json_file.close()
    def process_item(self, item, spider):
        # 将 item 对象转换为JSON字符串
        text = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        # 写入JSON字符串
        self.json_file.write(text.encode("utf-8"))

        
        # print ('工作:' , item['title'])
        # print ('工资:' , item['salary'])
        # print ('工作地点:' , item['work_addr'])
        # print ('详情链接:' , item['url'])

        # print ('公司:' , item['company'])
        # print ('行业:' , item['industry'])
        # print ('公司规模:' , item['company_size'])

        # print ('招聘人:' , item['recruiter'])
