#coding:utf8

from class_repo_crawler import repo_crawler
import sys

def xhelp():
    print("[*] -k, --keyword       Github搜索关键词    <> 默认 'a'")
    print("[*] -l, --language      仓库使用的语言      <> 默认'HTML'")
    print("[*] -t, --timeout       下载超时时间        <> 默认10秒")
    print("[*] -n, --num           要下载的仓库数量    <> 默认30个")
    print("[*] -s, --size          要下载的仓库大小    <> 默认40000KB")
    print("[*] -h, --help          help帮助            <> print this help")
    print("[*] Example : python main.py -l 'javascript' -n 10 -l 'html'")
    sys.exit(1)

if __name__ == '__main__':
	repo_num = 20
	keyword = 'a'
	language = 'HTML'
	timeout = 10
	repo_size = 40000
	
	try:
		for argv in sys.argv:
			if argv.lower() == "-k" or argv.lower() == "--keyword":
				keyword = sys.argv[sys.argv.index(argv)+1]
			elif argv.lower() == "-l" or argv.lower() == "--language":
				language = sys.argv[sys.argv.index(argv)+1]
			elif argv.lower() == "-t" or argv.lower() == "--timeout":
				timeout = int(sys.argv[sys.argv.index(argv)+1])
			elif argv.lower() == "-n" or argv.lower() == "--num":
				repo_num = int(sys.argv[sys.argv.index(argv)+1])
			elif argv.lower() == "-s" or argv.lower() == "--size":
				repo_size = int(sys.argv[sys.argv.index(argv)+1])
			elif argv.lower() == "-h" or argv.lower() == "--help":
				xhelp()
	except SystemExit:
		print("[!] Cheak your parametars input")
		sys.exit(0)
	except Exception:
		xhelp()
	
	r = repo_crawler(keyword=keyword,language=language,timeout=timeout,repo_num=repo_num)
	r.run()