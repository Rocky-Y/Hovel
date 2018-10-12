
import threading
from queue import Queue
from lxml import etree
import requests
import json
import time

#  创建采集类
class ThreadCrawl(threading.Thread):  # 继承threading.Thread 父类
    def __init__(self, threadName, pageQueue, dataQueue):
        super(ThreadCrawl, self).__init__()
        self.threadName = threadName
        self.pageQueue = pageQueue
        self.dataQueue = dataQueue
        self.headers = {"User-Agent" : "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;" }

    def run(self):
        print("启动" + self.threadName)
        while not CRAWL_EXIT:
            try:
                page = self.pageQueue.get(False)
                url = "http://www.qiushibaike.com/8hr/page/" + str(page) + "/"
                content = requests.get(url, headers=self.headers ).text
                time.sleep(1.5)
                self.dataQueue.put(content)
            except:
                pass
        print("退出" + self.threadName)

#  创建解析类
class ThreadParse(threading.Thread):
    def __init__(self, threadName, dataQueue, filename, lock):
        super(ThreadParse, self).__init__()
        self.threadName = threadName
        self.dataQueue = dataQueue
        self.filename = filename
        self.lock = lock

    def run(self):
        print("启动" + self.threadName)
        while not PARSE_EXIT:
            try:
                html =self.dataQueue.get(False)
                self.parse(html)
            except:
                pass
        print("退出" + self.threadName)

    def parse(self, html):
        html = etree.HTML(html)
        node_list = html.xpath('//div[contains(@id, "qiushi_tag")]')

        for node in node_list:
            # 用户名
            username = node.xpath('.//div[@class="author clearfix"]//h2/text()')[0].strip()
            # 图片连接
            image = node.xpath('.//div[@class="author clearfix"]//@src')[0].strip()
            # 取出标签下的内容,段子内容
            content = node.xpath('.//div[@class="content"]/span[1]/text()')[0].strip()
            # 取出标签里包含的内容，点赞
            zan = node.xpath('.//span[@class="stats-vote"]/i/text()')[0].strip()
            # 评论
            comments = node.xpath('.//span[@class="stats-comments"]/a/i/text()')[0].strip()
            items = {
                "username": username,
                "image": image,
                "content": content,
                "zan": zan,
                "comments": comments
            }

            with self.lock:
                self.filename.write(json.dumps(items, ensure_ascii=False).encode("utf-8") +b","+ b"\n")

CRAWL_EXIT = False
PARSE_EXIT = False

def main():
    pageQueue = Queue(10)
    for i in range(1,11):
        pageQueue.put(i)
    dataQueue = Queue()
    filename = open('duanzi.json', 'wb+')
    lock = threading.Lock()


    #  创建采集线程
    crawlList = ["Collection thread_1", "Collection thread_2", "Collection thread_3"]
    threadcrawl = []
    for threadName in crawlList:
        thread = ThreadCrawl(threadName, pageQueue, dataQueue)
        thread.start()
        threadcrawl.append(thread)

    while not pageQueue.empty():
        pass
    global  CRAWL_EXIT
    CRAWL_EXIT = True
    print("pageQueue为空")

    for thread in  threadcrawl:
        thread.join()
        print("1")

    #  创建解析线程
    parseList = ["Parsing thread_1", "Parsing thread_2", "Parsing thread_3"]
    threadparse = []
    for threadName in parseList:
        thread = ThreadParse(threadName, dataQueue, filename, lock)
        thread.start()
        threadparse.append(thread)

    while not dataQueue.empty():
        pass
    global PARSE_EXIT
    PARSE_EXIT = True
    print("dataQueue为空")
    for thread in threadparse:
        thread.join()
        print ("2")

    with lock:
        filename.close()
    print ("谢谢使用！")

if __name__ == '__main__':
    main()




