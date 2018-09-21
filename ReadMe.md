仓库下载脚本（单线程） —— Sera Wang

---

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