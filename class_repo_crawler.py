#coding:utf8

import requests
import zipfile
import time
import os
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
#禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

'''-------------------------------------------------------------------------------------'''

class repo_crawler():
	def __init__(self,repo_num=20,keyword='a',language='HTML',repo_size=40000,timeout=10):
		self.keyword = keyword #搜索关键词
		self.language = language #仓库的编程语言
		self.repo_num = repo_num #要爬取的仓库数量
		self.repo_size = repo_size #限制仓库实际大小(小于repo_size，单位是kb)
		self.timeout = timeout #限制仓库下载时间 (超时则停止下载)
		
		self.count = 0 # 下载计数器
		
		#github搜索页面基本url
		self.base_url = 'https://github.com/search?type=Repositories'
		
	def run(self):
		repo_list = self.get_repo_list() #爬取仓库得到仓库名的一维list
		
		if os.path.exists('./result') == False:
			os.makedirs('./result')
		
		isAllDown = False
		
		for repo_name in repo_list:
			# if self.isOverSize(repo_name) == False:
				# self.download_repo(repo_name)
			self.download_repo(repo_name)
			
			if self.count == self.repo_num:
				isAllDown = True
				break
			
		if isAllDown == False:
			print('[*] download stop.')
		else:
			print('[*] download OK !')
			
	# 下载目标仓库解压并删除zip
	def download_repo(self,repo_name):
		repo_url = 'https://github.com'+repo_name+'/archive/master.zip'
		file_name = './result/'+repo_name[1:].replace('/','-')+'.zip'
		
		print('[-] downloading repo: '+repo_name+' ...')
		
		req = requests.get(url=repo_url,verify=False,stream=True)
		
		start_time = int(time.time()) #起始时间戳
		
		isOk = True #下载成功标志
		with open(file_name,'wb') as file:
			for chunk in req.iter_content(chunk_size=2048):
				if chunk:
					download_time = int(time.time()) - start_time #已下载时间
					if download_time > self.timeout:
						print('[!] '+repo_name+' download timeout. Stop downloading...')
						isOk = False
						break
					file.write(chunk)
					file.flush()
		if isOk:	
			self.count+=1
		try:
			repo_zip = zipfile.ZipFile(file_name,'r')
			for file in repo_zip.namelist():
				repo_zip.extract(file,'./result/')
			repo_zip.close()
		except:
			pass
		
		if os.path.exists(file_name):
			os.remove(file_name)
		
		'''
	#输入类似 77Sera/helpme 这样的 user/repo 字符串
	#判断仓库大小是否超过设定的self.repo_size大小
	def isOverSize(self,repo_name):
		url = 'https://api.github.com/repos'+repo_name
		
		size_pat = '"size":([0-9]+)'
		
		isOverSize = True
		
		try:
			req = requests.get(url=url,verify=False)
			size = int(re.compile(size_pat,re.S).findall(req.text)[0])
			if size < self.repo_size:
				isOverSize = False
		except:
			pass
			
		return isOverSize
		'''
		
	# 爬取 repo_num数量的 repo_name，返回一个list
	def get_repo_list(self):
		repo_list = [] #初始化 repo_name_list
		
		repo_list_pat = '<ul class="repo-list">(.*?)</ul>' #第一次过滤文本的正则
		repo_name_pat = '<div.*?<div.*?<h3>.*?href="(.*?)">' #过滤仓库名的正则
		
		url = self.base_url+'&l='+self.language+'&q='+self.keyword+'+size%3A<='+str(self.repo_size)
		page_num = self.get_page_num(url) #获取总页数
		count = 0 #计数器
		isOk = False #break标志
		
		print('[-] processing repo_list ...')
		
		if page_num == 0:
			print('[-] Crawler is banned by Github. plz try again later.')
		
		for p in range(page_num):
			# print('[-] processing '+str(p+1)+' page...')
			
			#根据关键词和页数组成搜索页url
			url = self.base_url+'&l='+self.language+'&q='+self.keyword+'+size:<='+str(self.repo_size)+'&p='+str(p+1)
			
			try:
				req = requests.get(url=url,verify=False) #获得响应
				
				# 获取第一次过滤文本
				filt_text = re.compile(repo_list_pat,re.S).findall(req.text)[0] 
				
				#得到一个仓库名的list
				repo_name_list = re.compile(repo_name_pat,re.S).findall(filt_text)
				
				for i in range(len(repo_name_list)):
					repo_list.append(repo_name_list[i])
					count+=1
					if count == self.repo_num+20: #爬取到足够数量的仓库名
						isOk = True
						break
			except:
				pass
			if isOk:
				break
		return repo_list
		
	# 获取github总页数
	# 输入一个github搜索页的url，返回一个int型数据（0-100）
	def get_page_num(self,url):
		pat = '.*>([0-9]{1,3})</a>.*?<a class="next_page"'
		try:
			req = requests.get(url=url,verify=False) #获得响应
			page_num = re.compile(pat,re.S).findall(req.text)[0] #正则获取最大页数
			page_num = int(page_num)
		except:
			page_num = 0
		return page_num