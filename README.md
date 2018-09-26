# Browser Fuzzing

浏览器Fuzzing，private project。 so only functional codes will be pushed.

---------------------------------------------

<h3>样本下载</h3>

Sample_downloader（single thread） ————download repositories from github as web-samples   用来下载web样本

1. use pip install -r requirements.txt install the requirements.

2. see help 查看帮助

use => python main.py -h

3. each argument has a default value. 参数都具有默认值

	eg: 

	>python main.py -k 'test' -l 'javascript' -t 10 -n 40	示例

	-k set default search-keyword ， default=> 'a'		设置搜索关键词

	-l set repositories-language ，default=> 'HTML'	

	-t set download timeout ，default=> 10 (seconds)

	-n set the num of the repositories to download ，default=>30  (repositories will be downloaded)

	-s set the size of the repositories in order to prevent downloading timeout ，default => 40000 (KB，about 40MB)

4. examples:

	![](http://p6jpvwsnk.bkt.clouddn.com/18-9-6/73710772.jpg)

-------------------------------------------------

<h3>样本提取</h3>

distributor.py 脚本用来提取下载好的仓库中的HTML，CSS，JS文件。

同时会对HTML文件中的JS，CSS部分做替换提取。


设置选项

146行 repo_path 是要提取的仓库路径

147行 output_dir 是要输出的目录路径。

_split 设置是否要为各个仓库单独创建文件夹

--------------------------------------------------------------

<h3>html文件转向量矩阵</h3>


html2vectorMatrix.py 是函数文件

main.py里有使用示例，如何使用请看main.py

index.html是测试文件

all_tag是html标签字典


<h4>使用示例</h4>
<br/>

<code>

	#coding:utf8

	from html2vectorMatrix import *
</code>

1. 打印向量矩阵，矩阵维数=>提取出的"token"数 * 字典大小 (即all_tag大小，222)

<code>
	
  	tagList = getTagList() # 读取本地字典
  
	html_str = readFile('./index.html') # 读取本地index.html文件
	
	vector_matrix = generateMatrix(html_str,tagList) # 获取向量矩阵
</code>

对于不在字典中的token，会将其字符串输出，可以以此来分类或者扩充字典

-------------------------------------------------------------

2. 将向量矩阵还原为原来的 html字符串

<code>
	
	html_string = matrix2string(vector_matrix,tagList) 

	print(html_string)
</code>

3. 分析向量矩阵，主要是看不在字典中的token是哪些，便于日后分类，还可以设置精度查看其对应的上下文

<code>
	
	analyzeMatrix(vector_matrix,tagList)
</code>
<br/>


![](http://p6jpvwsnk.bkt.clouddn.com/18-9-22/37298078.jpg)


以上~ 函数示例，查看main文件即可
