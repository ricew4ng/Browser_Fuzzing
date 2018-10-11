#coding:utf8

from html2vectorMatrix import *
import os

if __name__ == '__main__':
	tagList = getTagList() # 读取本地字典
	# html_str = readFile('./index.html') # 读取本地index.html文件
	# 获取向量矩阵，形式:2维list;  矩阵维数: token数 * 字典大小
	# vector_matrix = generateMatrix(html_str,tagList) 
	# html_string = matrix2string(vector_matrix,tagList) # 将矩阵还原成html字符串
	# print(html_string) # 打印html字符串
	# 分析矩阵
	# analyzeMatrix(vector_matrix,tagList)
	
	# 对不在字典中的token分类，得到一个dict，{"token":"token出现次数"}
	
	sample_path = './html_samples' #目标html文件夹
	checkNum = 100 # 要分析的文件数量
	
	lost_token = checkHTML('./html_samples',tagList,checkNum=checkNum)
	token_dict = analyzeTokens(lost_token) # 获取token字典
	
	with open('token_dict','w') as file: # 将字典写入文件
		for k,v in token_dict.items():
			file.write(k+' 出现次数=>'+str(v)+'\n')