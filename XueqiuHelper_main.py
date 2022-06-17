#encoding: utf-8
#projectname: A Spider to Get Xueqiu.com Users' Post
#Author：@slingthy
#Contact:slinthy@qq.com

 
import os,re,requests,json,time,datetime,urllib3,fake_useragent,random
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
urllib3.disable_warnings()

def get_range(m_maxPage):
	mP = m_maxPage
	while True:
		answer = input('是否全部页面？（回答是或否）')
		if answer == '是':
			startPage = 1
			endPage = mP
			break

		elif answer == '否':
			while True:
				print('该用户博客页为1-%s'%str(mP))
				startPage,endPage = (map(int,input('请输入爬取起始页面的页码，用“-”隔开，例如“1-10”：').split('-')))
				if (startPage <= endPage) and (startPage >= 1) and (endPage <= mP):
					break
				else:
					print('警告：页码范围错误或超出区间！请重新输入……')
					continue
			break

		else:
			print('警告：输入值错误！请回答“是”或“否”')
			continue

	return startPage, endPage


def get_response_text(url):
	response = requests.get(url, headers = headers, proxies=proxy, verify=False)
	return json.loads(response.text)

def get_maxPage(url):
	maxPage = get_response_text(url)['maxPage']
	return maxPage

def get_userName(url):
	userName = get_response_text(url)['statuses'][0]['user']['screen_name']
	return userName


def get_content(m_startPage,m_endPage):
	digi = 0
	for m_page in range(m_startPage,m_endPage+1): 
		m_DDL = 'https://xueqiu.com/v4/statuses/user_timeline.json'+'?page='+str(m_page)+'&user_id='+userid+'&type='+str(type)
		m_list_onepage = get_response_text(m_DDL)['statuses']
		print('正在爬取第%s页动态...'%str(m_page))

		for m_column in m_list_onepage:
			digi += 1
			MINDEX = m_list_onepage.index(m_column)+1
			CID = m_column['id']
			MTEXT = m_column['text']
			MTIME = datetime.datetime.fromtimestamp(int(m_column['created_at']) / 1000).strftime('%Y-%m-%d %H:%M:%S')
			ABpath = '%s\\%s.html'%(path,userName)
			with open(ABpath,"a",encoding="utf-8") as userblog:
				userblog.write('<h1>%s</h1>%s<br/>'%(MTIME,MTEXT))
				get_comments(CID,MINDEX,userblog,m_page) #无需评论区时加上注释标记
				userblog.close()
			
			if digi % 20 == 0:#开始、关闭评论区的参数分别设置为20、100
				print('------休息一会儿------')
				time.sleep(random.randint(10,20))
				print('-------继续工作-------')
			
		print('当前爬取量:%s条'%str(digi))
		
	print('------已导出文件至%s------'%ABpath)

def get_comments(CID,MINDEX,userblog,m_page):
	c_maxPage = get_maxPage('https://xueqiu.com/statuses/comments.json?id='+str(CID)+'&count=10&page=1')
	for c_page in range(1,c_maxPage+1):
		c_DDL = 'https://xueqiu.com/statuses/comments.json?id='+str(CID)+'&count=10&page='+str(c_page)
		print('正在爬取第%s页第%s条：第%s页评论...'%(str(m_page),str(MINDEX),str(c_page)))
		for c_column in get_response_text(c_DDL)['comments']:
			CNAME = c_column['user']['screen_name']
			CTEXT = c_column['text']
			userblog.write('<h4>%s</h4>%s<br/>'%(CNAME,CTEXT))
		
		


if __name__ == '__main__':
	# -----------------------  ↓  Config Zone  ↓------------------------------------------------------
	cookie = ''
	proxy = {'http':"127.0.0.1:8888",'https':"127.0.0.1:8888",} 
	headers = {
	    'Host':"xueqiu.com",
	    'Referer': 'https://xueqiu.com/',
	    'User-Agent': fake_useragent.UserAgent().chrome,
	    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
	    'Connection':'keep-alive',
	    'Cookie': cookie
	}
	type = 0
	userid = input("填写用户主页链接").split('/')[-1] #提取要爬取的用户UID
	path = os.path.join(os.getcwd(),userid)
	if not os.path.exists(path):
		os.makedirs(path)
	URL_maininfo = 'https://xueqiu.com/v4/statuses/user_timeline.json?page=1'+'&user_id='+userid
	m_maxPage, userName = get_maxPage(URL_maininfo), get_userName(URL_maininfo)
	startPage,endPage = get_range(m_maxPage)
	get_content(startPage,endPage)
	






    

