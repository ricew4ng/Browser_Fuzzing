# BrowserFuzzing

浏览器Fuzzing。隐私项目，所以这里只push一些func代码 —— Sera Wang


<h3>样本下载</h3>
---

仓库下载脚本（单线程） 

1. 先使用 pip install -r requirements.txt 安装所需要的库

2. 具体使用:

	输入 python main.py -h 查看帮助

3. 各参数都有默认值，可以根据需要调整

	eg: 

	>python main.py -k 'test' -l 'javascript' -t 10 -n 40

	-k 设置搜索关键词 默认 'a'

	-l 设置仓库语言，默认 'HTML'

	-t 设置下载超时时间，默认10秒

	-n 设置要下载的仓库数量，默认30个

	-s 设置 仓库下载大小限制，默认40000KB，即40MB左右

4. 例子:

	![](http://p6jpvwsnk.bkt.clouddn.com/18-9-6/73710772.jpg)


<h3>样本提取</h3>
---
distributor.py 脚本用来提取下载好的仓库中的HTML，CSS，JS文件。

同时会对HTML文件中的JS，CSS部分做替换提取。


设置选项

---

146行 repo_path 是要提取的仓库路径

147行 output_dir 是要输出的目录路径。

_split 设置是否要为各个仓库单独创建文件夹


<h3>html文件转向量矩阵</h3>
---

html2vectorMatrix.py 是函数文件

main.py里有使用示例，如何使用请看main.py

index.html是测试文件

all_tag是html标签字典
