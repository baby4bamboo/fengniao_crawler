#-*-coding=utf-8-*-
from bs4 import BeautifulSoup
import urllib2,sys,StringIO,gzip,time,random,re,urllib,os,random
reload(sys)
sys.setdefaultencoding('utf-8')
class Fengniao():
    def __init__(self):
        self.url="http://bbs.fengniao.com"
        user_agent="Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
        self.headers={"User-Agent":user_agent}


    def __getContentAuto(self,url):
        print url
        req=urllib2.Request(url,headers=self.headers)
        resp=urllib2.urlopen(req)
        content=resp.read()
        info=resp.info().get("Content-Encoding")
        if info==None:
            return content
        else:
            t=StringIO.StringIO(content)
            gziper=gzip.GzipFile(fileobj=t)
            html = gziper.read()
            return html

    def __findbest(self):
        content=[]
        for j in range(8,22):
            if j==0:
                url_best="http://bbs.fengniao.com/jinghua-101.html"
            else:
                url_best="http://bbs.fengniao.com/jinghua-101-"+str(j)+".html"
            posts_best=self.__getContentAuto(url_best)
            p=re.compile(r'href="(\S+)" class="pic"')
            list_of_best = p.findall(posts_best)
            for i in list_of_best:
                try:
                    page_best=self.__getContentAuto(i)
                    p=re.compile(r'href="(\S+)" class="return"')
                    content_item = p.findall(page_best)
                    if content_item != []:
                        content.append(content_item[0])
                except :
                    pass
                    print "this posts was deleted"
        return content

    def __store2dic(self,url):
        
        html=self.__getContentAuto(url)
        bs=BeautifulSoup(html,"html.parser")
        theme=bs.find('span',class_="h1").string
        forum_dic={}
        forum_dic["theme"]=theme
        forum_dic["theme_number"]=101


        p=re.compile(r'href="/(forum/\d+.html)"')
        #content = p.findall(html)
        content=self.__findbest()

        posts_number=0
        for i in content:
            posts=self.__getContentAuto(self.url+i)
            bs=BeautifulSoup(posts,"html.parser")
            all_img=bs.find_all('img',class_="thread-img")
            if all_img!=[]:
                posts_number+=1
                posts_title=bs.find('p',class_="title").string
                posts_dic={}
                posts_dic["title"]=posts_title
                posts_dic["pic_number"]=len(all_img)
                for j in range(len(all_img)):
                    download_link = all_img[j]['src']
                    posts_dic[j]=download_link
                forum_dic[posts_number]=posts_dic
                forum_dic["posts_number"]=posts_number
        return forum_dic

    def __download(self,html_dic):
        forum_dic={}
        forum_dic=html_dic

        forum_folder = os.path.join(os.getcwd(), forum_dic["theme"])
        if not os.path.exists(forum_folder):
            os.mkdir(forum_folder)
            os.chdir(forum_folder)
        print forum_folder
        for i in range(1,forum_dic["posts_number"]+1):
            posts_dic=forum_dic[i]   
            post_folder=os.path.join(forum_folder,str(i))
            print post_folder            
            if not os.path.exists(post_folder):
                os.mkdir(post_folder)
                os.chdir(post_folder)
            for j in range(1,posts_dic["pic_number"]):
                download_link=posts_dic[j]
                filename=str(j)+".jpg"
                print filename
                print download_link
                try:
                    if download_link != "" and filename != "":
                        urllib.urlretrieve(download_link,filename)
                        time.sleep(4)
                except :
                    pass
                    print "download file fail"


    def getPhoto(self):
        url="http://bbs.fengniao.com/forum/forum_101.html"
        html_dic = self.__store2dic(url)
        self.__download(html_dic)
        #self.__findbest()


def main():
    obj=Fengniao()
    obj.getPhoto()


if __name__=="__main__":
    main()




