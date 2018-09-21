#coding:utf8

'''
输入一个仓库(文件夹路径)

1. 提取其中的html，js，css文件

2. 提取script标签内容为js文件，提取style标签内容为css文件

3. 变量替换 href，src等引用部分 以及 script片段 (用任意变量名替换)
'''

import shutil
import random
import sys
import os
import re


def xhelp():
    print("[*] -d, --repo_dir       要提取html,css,js的目录路径    <> 如 './target_dir'")
    print("[*] -o, --output_dir     结果输出文件夹                 <> 默认'./result'")
    print("[*] -dL --dir_list      批量提取目标目录下的仓库目录   <> 会对目标目录下一层的所有目录做一次提取")
    print("[*] -h, --help           help帮助                       <> print this help")
    print("[*] Example : python hcj_sep.py -d './repo'")
    print("[*] Example : python hcj_sep.py -dL './repos'")
    sys.exit(1)
	
# 输入仓库路径，返回所有文件的绝对路径（二维list），list[0]是文件名，list[1]是文件路径
def get_hcj_list(repo_path):
	path_list = []
	
	pat = '\.html|\.css|\.js$' #提取html,css,js的正则
	
	if os.path.isdir(repo_path): #判断repo_path是否是一个文件夹
		for root,dirs,files in os.walk(repo_path):
			for file in files:
				r = re.compile(pat).findall(file)
				if len(r) != 0:
					abs_file_path = os.path.join(root,file)
					path_list.append([file,abs_file_path])
	else:
		print('[!] dir path error. ')
	return path_list
	
# 输入文件路径的二维list，将它们移至目标文件夹target_dir
def shift_file(file_list,target_dir):
	if os.path.isdir(target_dir):
		for file_name,file_path in file_list:
			new_file_name = target_dir+'/'+file_name
			if os.path.exists(new_file_name):
				pat = '(.*?)\.'
				try:
					r = re.compile(pat).findall(file_name)[0]
					file_name = file_name.replace(r,r+str(random.random())[2:8])
				except:
					pass
				new_file_name = target_dir+'/'+file_name
			shutil.copyfile(file_path,new_file_name)
		
# 从文件中提取script和style内容，生成新文件
# 输入 表示文件路径的二维list，以及要输出新文件到的目标目录
def extract_quote(file_list,target_dir):
	html_pat = '\.html$' #正则判断是否为html文件
	script_pat = '<scrip.*?>(.*?)</script>' #正则 script脚本
	style_pat = '<styl.*?>(.*?)</style>' #正则 style标签
	
	for f_name,f_path in file_list:
		r = re.compile(html_pat).findall(f_path)
		if len(r) != 0: #是.html文件
			try:
				with open(f_path,'r') as file:
					script_fragment = ''.join(re.compile(script_pat,re.S).findall(file.read()))
					style_fragment = ''.join(re.compile(style_pat,re.S).findall(file.read()))
				
				if script_fragment != '':
					with open(target_dir+'/script-'+str(random.random())[2:8]+'.js','w') as file:
						file.write(script_fragment)
				if style_fragment != '':
					with open(target_dir+'/css-'+str(random.random())[2:8]+'.css','w') as file:
						file.write(style_fragment)
			except:
				pass
		
# 输入文件路径的二维list，将其中所有文件的引用部分和script片段替换为任意变量
def replace_quote(file_list):
	html_pat = '\.html$' #正则判断是否为html文件
	
	all_pat = '=".*?\.!(js|png|jpg|gif)"|=\'.*?\.!(js|png|jpg|gif)\''
	js_pat = '=".*?\.js"|=\'.*?\.js\'|=.*?\.js ' #正则替换js
	pic_pat = '=".*?\.(png|jpg|gif)"|=\'.*?\.(png|jpg|gif)\'|=.*?\.(png|jpg|gif) ' #正则替换图片
	script_pat = '<scrip.*?>.*?</script>' #正则替换script脚本
	style_pat = '<styl.*?>.*?</style>' #正则替换style标签
	
	for f_name,f_path in file_list:
		r = re.compile(html_pat).findall(f_path)
		if len(r) != 0: #是.html文件
			try:
				with open(f_path,'r') as html_file:
					text = re.compile(js_pat,re.S).sub('="a.js"',html_file.read())
					text = re.compile(pic_pat,re.S).sub('="b.png"',text)
					text = re.compile(script_pat,re.S).sub('',text) #替换script片段为空
					text = re.compile(style_pat,re.S).sub('',text) #替换style片段为空
					text = re.compile(all_pat,re.S).sub('="abc"',text)
					
				with open(f_path,'w') as html_file:
					html_file.write(text)
			except:
				pass
		

		
# 对输入的一个目录做一次提取处理
def process_dir(dir_path,output_dir):
	if os.path.exists(output_dir) == False: #若文件不存在则新建文件夹
		os.makedirs(output_dir)
	file_list = get_hcj_list(dir_path) #得到目标文件夹的htmljscss文件路径
	shift_file(file_list,output_dir) #复制文件到新目录下
	new_file_list = get_hcj_list(output_dir) #获取新目录下的文件路径
	extract_quote(new_file_list,output_dir) #提取标签到新目录下
	replace_quote(new_file_list) #变量替换新文件
		
		
if __name__ == '__main__':
	repo_path = ''
	output_dir = './result' #输出目录
	dir_list = ''
	
	try:
		for argv in sys.argv:
			if argv.lower() == "-d" or argv.lower() == "--repo_dir":
				repo_path = sys.argv[sys.argv.index(argv)+1]
			elif argv.lower() == "-o" or argv.lower() == "--output_dir":
				output_dir = sys.argv[sys.argv.index(argv)+1]
			elif argv.lower() == "-dl" or argv.lower() == "--dir_list":
				dir_list = sys.argv[sys.argv.index(argv)+1]
			elif argv.lower() == "-h" or argv.lower() == "--help":
				xhelp()
	except SystemExit:
		print("[!] Check your parametars input")
		sys.exit(0)
	except Exception:
		xhelp()
		
	if repo_path == '' and dir_list == '':
		xhelp()
		sys.exit(0)
		
	if dir_list != '':
		repo_list = []
		count = 1
		for i in os.listdir(dir_list):
			if os.path.isdir(dir_list+'/'+i):
				print('[-] processing '+str(count)+' repo ...')
				dir_path = dir_list+'/'+i
				process_dir(dir_path,output_dir+'/'+i)
				count+=1
	else:
		process_dir(repo_path,output_dir)