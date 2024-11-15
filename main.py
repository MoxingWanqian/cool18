import os
import re
import time
import requests
from tqdm import tqdm
from config import *
from lxml import etree
from functools import wraps

def retry(max_attempts=5, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

class COOL18:

	# 初始化变量
	def __init__(self):
		self.page = START_PAGE
		self.time_sleep = TIME_SLEEP
		self.save_path = SAVE_PATH
		self.host = HOST
		self.proxy = PROXY

	# 获取网页
	@retry()
	def get_tree(self, url='', params={}, proxy={}):
		resp = requests.get(url=url, params=params, proxies=proxy)
		resp.encoding = resp.apparent_encoding
		tree = etree.HTML(resp.text)
		time.sleep(self.time_sleep)
		return tree
	
	# 获取多页结果
	def get_results(self, page_num:int=1):
		results = []
		for i in range(self.page, self.page+page_num):
			self.page = i
			tree = self.get_tree(url=self.host, params={'app': 'forum','act': 'gold','p': self.page}, proxy=self.proxy)
			result = self.get_result(tree=tree)
			for j in result:
				results.append(j)
		return results

	# 获取单页结果
	def get_result(self, tree):
		hrefs = tree.xpath('//li/a/@href')
		titles = tree.xpath('//li/a/text()[2]')
		titles = [re.search('【.*?】', i).group(0) for i in titles]
		return zip(titles, hrefs)
	
	# 获取完整作品
	def get_novel(self, title:str):
		result = []
		novel = re.search('【.*?】', title).group(0)
		params = {
			'action': 'search',
			'act': 'threadsearch',
			'app': 'forum',
			'keywords': novel
		}
		tree = self.get_tree(url=self.host, params=params, proxy=self.proxy)
		hrefs = tree.xpath('//span[@class="t_subject"]/a/@href')
		for href in hrefs:
			title = tree.xpath(f'string(//a[@href="{href}"])')
			result.append((novel, href, title))
		return result

	# 获取单章内容
	def get_content(self, href:str):
		tree = self.get_tree(url=self.host+href, proxy=self.proxy)
		content = tree.xpath('//pre//text()')
		content = list(filter(lambda x: x != 'cool18.com', content))
		return content

	# 创建文件夹
	def mkdir(self, path):
		if not os.path.exists(os.path.dirname(path)):
			self.mkdir(path=os.path.dirname(path))
			self.mkdir(path)
		else:
			if not os.path.exists(path):
				os.mkdir(path)
		return path

	# 下载小说
	def download(self, novel):
		articles = self.get_novel(title=novel)
		for article in articles:
			path = self.mkdir(f'{self.save_path}/{article[0]}')
			content = self.get_content(href=article[1])
			name=article[2].replace('/', '-')
			with open(f'{path}/{name}.txt', 'w', encoding='utf-8') as f:
				for i in content:
					f.write(i+'\r\n')
		return None

	# 更新已下载
	def update_local(self):
		print(len(os.listdir(f'{self.save_path}')))

	# 更新指定作品
	def update_one(self, title:str):
		result = self.get_novel(title=title)
		title = re.search('【.*?】', title).group(0)
		try:
			if len(list(result)) != len(os.listdir(f'{self.save_path}/{title}')):
				for i in result:
					i[2]
			else:
				print(False)
		except FileNotFoundError:
			print(None)

	# 更新所有
	def update_all(self, page_num=5):
		results = self.get_results(page_num=page_num)
		for i in results:
			self.update_one(title=i[1])

	# 搜索关键词
	def search(self):
		pass

	# 日志
	def log(self, error):
		pass

def main():
	c18 = COOL18()
	# c18.update_one('【17岁的夏天】')
	c18.update_all()
	# results = c18.get_results(page_num=5)
	# pro = tqdm(results[347:], desc='Total')
	# for i in pro:
	# 	result = c18.download(novel=i[0])

if __name__ == '__main__':
	main()
