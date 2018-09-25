# Browser Fuzzing

浏览器Fuzzing。隐私项目，所以这里只push一些func代码 —— Sera Wang



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
