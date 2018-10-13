# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request,FormRequest
import urllib.request


class DbSpider(scrapy.Spider):
    name = 'db'
    allowed_domains = ['douban.com']
    header = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}
    # start_urls = ['http://douban.com/']

    def start_requests(self):
        return [Request("https://accounts.douban.com/login",callback=self.parse(),meta={"cookiejar":1})]

    def parse(self, response):
        captcha = response.xpath("//img[@id='captcha_image']/@src").extract()
        url = "https://accounts.douban.com/login"

        if len(captcha) > 0:
            print("此时验证码")
            localpath = "D:/captcha.jpg"
            urllib.request.urlretrieve(captcha[0],filename=localpath)
            print("请查看本地验证码图片并输入验证码")
            captcha_value=input()

            data = {
                "form_email":"************",
                "from_password":"************",
                "captcha-solution": captcha_value,
                "redir":"https://www.douban.com/people/***********/", # 个人中心主页地址
            }
            print("登陆中……")

        else:
            print("此时没有验证码")
            data = {
                "form_email":"****************",   
                "from_password":"*********************************",
                "redir":"https://www.douban.com/people/***********/", # 个人中心主页地址
            }

        print("登陆中……")
        return [FormRequest.from_response(response,
                                              meta = {"cookiejar":response.meta["cookiejar"]},
                                              headers = self.header,
                                              formdata=data,
                                              callback = self.next,
                                              )]
    def next(self,response):
        print("此时已经登陆完成，并爬取了个人中心的数据")
        title = response.xpath("//htmi/head/title/text()").extract()
        note = response.xpath("//div[@class='note']/text()").extract()
        print(title[0])
        print(note[0])




