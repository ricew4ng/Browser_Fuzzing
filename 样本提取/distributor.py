# coding:utf8

'''
输入一个仓库(文件夹路径):

1. 提取其中的html，js，css文件
2. 提取script标签内容为js文件，提取style标签内容为css文件
3. 变量替换 href，src等引用部分 以及 script片段 (用任意变量名替换)
'''

import shutil
import random
import sys
import os
import re

# 输入仓库路径，返回三个一维list，分别对应此仓库的html，css，js文件
def get_html_css_js_files(repo_path):
	html_files = []  # html文件路径
	css_files = []  # css文件路径
	js_files = []  # js文件路径

	pat = '.*\.(.*?)$'  # 文件后缀正则

	if os.path.isdir(repo_path):  # 判断repo_path是否是一个文件夹
		for root, dirs, files in os.walk(repo_path):  # 遍历目录
			for file in files:  # 遍历当前文件
				r = re.compile(pat).findall(file)  # 获取文件后缀
				if len(r) != 0:  # 存在后缀
					file_path = os.path.join(root, file)
					if r[0] == 'html':  # 是html文件
						html_files.append(file_path)
					elif r[0] == 'css':  # 是css文件
						css_files.append(file_path)
					elif r[0] == 'js':  # 是js文件
						js_files.append(file_path)
	else:
		print('[!] repo path error. ')
	return html_files, css_files, js_files


# 输入文件路径的list，将它们移至目标文件夹target_dir
def shift_files(file_list, target_dir):
	file_pat='.*[\\\\|/](.*?\..*?)$'	# 文件(包括后缀)正则

	if os.path.isdir(target_dir):  # 判断目标文件夹是否存在
		for file_path in file_list:  # 遍历文件路径
			file = re.compile(file_pat).findall(file_path)  # 获取文件名(包括后缀)
			if len(file) != 0:
				file = file[0]
				temp = target_dir + '/' + file

				if os.path.exists(temp):  # 如果目标目录，已存在同名文件
					pat = '(.*?)\.'  # 文件名 正则
					try:
						file_name = re.compile(pat).findall(file)[0]
						file = file.replace(file_name, file_name + str(random.random())[2:8])  # 将文件名命名为 原文件名+6位随机数 避免同名
					except:
						pass

				new_file_path = target_dir + '/' + file

				shutil.copyfile(file_path, new_file_path)

# 从文件中提取script和style内容，生成新文件
# 输入 1. 文件路径的list; 2.新文件所在目标 js,css目录
def extract_js_css(html_files, js_dir, css_dir):
	js_pat = '<script[^<]*?>(.+?)</script>'  # 正则 script脚本
	css_pat = '<style[^<]*?>(.+?)</style>'  # 正则 style标签

	for html_file in html_files:
		try:
			with open(html_file, 'r') as file:
				js_fragment = ''.join(re.compile(js_pat, re.S).findall(file.read()))
				css_fragment = ''.join(re.compile(css_pat, re.S).findall(file.read()))

			if js_fragment != '':
				with open(js_dir + '/js-' + str(random.random())[2:8] + '.js', 'w') as file:
					file.write(js_fragment)
			if css_fragment != '':
				with open(css_dir + '/css-' + str(random.random())[2:8] + '.css', 'w') as file:
					file.write(css_fragment)
		except:
			pass

# 输入html文件路径的list，将其中所有文件的引用部分和script片段替换为任意变量
def replace_quote(html_files):
	js_pat = '="[^<>"\']*?\.js"|=\'[^<>"\']*?\.js\''  # 正则替换js
	css_pat = '="[^<>"\']*?\.css"|=\'[^<>"\']*?\.css\''  # 正则替换css
	pic_pat = '="[^<>"\']*?\.(png|jpg|gif)"|=\'[^<>"\']*?\.(png|jpg|gif)\''  # 正则替换图片
	script_pat = '<script[^<]*?>.+?</script>'  # 正则替换script脚本
	style_pat = '<style[^<]*?>.+?</style>'  # 正则替换style标签
	code_pat = '<code[^<]*?>.+?</code>' # 正则替换code标签
	pre_pat = '<pre[^<]*?>.+?</pre>' # 正则替换pre标签
	comment_pat = '<!--.*?-->' # 正则替换注释标签

	for html_file in html_files:
		try:
			with open(html_file, 'r') as file:
				text = file.read()
				text = re.compile(js_pat, re.S).sub('="a.js"', text) # 替换js引用
				text = re.compile(css_pat, re.S).sub('="a.css"', text) # 替换css引用
				text = re.compile(pic_pat, re.S).sub('="a.png"', text) # 替换图片引用
				# 替换script片段
				text = re.compile(script_pat, re.S).sub('<script>script</script>', text)
				# 替换style片段
				text = re.compile(style_pat, re.S).sub('<style>style</style>', text) 
				# 替换code片段				
				text = re.compile(code_pat, re.S).sub('<code>code</code>', text) 
				# 替换pre片段
				text = re.compile(pre_pat, re.S).sub('<pre>pre</pre>',text) 
				# 替换注释片段
				text = re.compile(comment_pat, re.S).sub('',text)
			with open(html_file, 'w') as file:
				file.write(text)
		except:
			pass
			
# 对输入的一个目录做一次提取处理
def process_repo(repo_path, output_dir,split=True):
    output_html_dir = output_dir + '/html'
    output_css_dir = output_dir + '/css'
    output_js_dir = output_dir + '/js'

    if not os.path.exists(output_dir):  # 若文件不存在则新建文件夹
        os.makedirs(output_dir)
    else:
        if split:
            shutil.rmtree(output_dir)
            os.makedirs(output_dir)
    if not os.path.exists(output_html_dir):  # 若文件不存在则新建文件夹
        os.makedirs(output_html_dir)
    if not os.path.exists(output_css_dir):  # 若文件不存在则新建文件夹
        os.makedirs(output_css_dir)
    if not os.path.exists(output_js_dir):  # 若文件不存在则新建文件夹
        os.makedirs(output_js_dir)

    html_files, css_files, js_files = get_html_css_js_files(repo_path)  # 获取h,c,j文件
    shift_files(html_files, output_html_dir)  # 复制html文件到新目录下
    shift_files(css_files, output_css_dir)  # 复制css文件到新目录下
    shift_files(js_files, output_js_dir)  # 复制js文件到新目录下
    # 获取新目录下的h,c,j文件
    html_files, css_files, js_files = get_html_css_js_files(output_dir)
    # 提取js,css到新目录下
    extract_js_css(html_files, output_js_dir, output_css_dir)
    replace_quote(html_files)  # 对html文件做变量替换


if __name__ == '__main__':
	repo_path = 'set your path here' #输入目录
	output_dir = 'set your path here'  # 输出目录
	
	#按仓库分html,css,js 或者  统一html,css,js; 
	_split = False
	
	repos = [] #二维list，repos[x][0]是目录路径，repos[x][1]是目录名
	for i in os.listdir(repo_path): #获取所有仓库
		path = repo_path+'/'+i
		if os.path.isdir(path):
			repos.append([path,i]) 
			
	count = 1 #计数器
	for repo_path,repo_name in repos:
		print('[*] Processing '+str(count)+' repo...')
		if _split:
			dir = output_dir + '/' + repo_name
		else:
			dir = output_dir
		process_repo(repo_path,dir,_split)
		count+=1