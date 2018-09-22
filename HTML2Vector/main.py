#coding:utf8

from html2vectorMatrix import *

if __name__ == '__main__':
	tagList = getTagList() # 读取本地字典
	
	html_str = readFile('./index.html') # 读取本地index.html文件
	
	vector_matrix = generateMatrix(html_str,tagList) # 获取向量矩阵
	
	# 打印向量矩阵
	# for i in vector_matrix:
		# print(i)
	
	# html_string = matrix2string(vector_matrix,tagList) # 将矩阵还原成html字符串
	
	# print(html_string)
	
	# 分析矩阵
	
	analyzeMatrix(vector_matrix,tagList)