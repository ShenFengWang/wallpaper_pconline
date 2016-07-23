import urllib.request
import gzip
import re
import pymysql

try:
    mysqlConnect = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'wallpaper_pconline', charset = 'utf8', cursorclass = pymysql.cursors.DictCursor)
except pymysql.err.InternalError:
    mysqlConnect = pymysql.connect(host = 'localhost', user = 'root', password = '', cursorclass = pymysql.cursors.DictCursor)
    with mysqlConnect.cursor() as cursor:
        cursor.execute('CREATE DATABASE IF NOT EXISTS `wallpaper_pconline` DEFAULT CHARSET utf8 COLLATE utf8_general_ci')
        cursor.execute('use `wallpaper_pconline`')
        cursor.execute('CREATE TABLE IF NOT EXISTS `list_page` (`id` int not null auto_increment primary key, `page` int not null)')
        cursor.execute('CREATE TABLE IF NOT EXiSTS `paper_data` (`id` int not null auto_increment primary key,\
                                                   `url` varchar(255) not null,\
                                                   `image` varchar(255) not null)')
        cursor.execute('INSERT INTO `list_page` (`page`) VALUE (1)')
        mysqlConnect.commit()
except Exception as e:
    print(e)
    exit()

def mysqlInsert(value):
    try:
        with mysqlConnect.cursor() as cursor:
            for oneAlbum in value:
                for row in oneAlbum:
                    cursor.execute('INSERT INTO `paper_data` (`url`,`image`) VALUES (%s, %s)', row)
            mysqlConnect.commit()
            return mysqlConnect.affected_rows()
    except Exception as e:
        print(e)
        exit()

def getPage():
    try:
        with mysqlConnect.cursor() as cursor:
            cursor.execute("SELECT `page` FROM `list_page` where `id` = 1")
            result = cursor.fetchone()
            return result['page']
    except Exception as e:
        print(e)
        exit()

def updatePage(pageNum):
    try:
        with mysqlConnect.cursor() as cursor:
            cursor.execute("UPDATE `list_page` SET `page` = %s WHERE `id` = 1", pageNum)
            mysqlConnect.commit()
            return mysqlConnect.affected_rows()
    except Exception as e:
        print(e)
        exit()

def getUrlSource(url):
    connectTime = 1
    print("trying to read url: %s" % (url))
    while True:
        if connectTime >= 10:
            writeLog(url)
            return False
        print("connect times: %d, remain: %d" % (connectTime, 10 - connectTime))
        connectTime += 1
        try:
            htmlSourceGet = urllib.request.urlopen(url, timeout = 10)
            if htmlSourceGet.getcode() != 200:
                print("code %d, going to try again")
                continue
            print("code 200: success")
            htmlSourceGzip = htmlSourceGet.read()
            print("check whether Gzip mode")
            htmlSource = gzip.decompress(htmlSourceGzip).decode('gbk')
        except urllib.error.URLError:
            print("urllib request timed out, going to try again")
            continue
        except OSError:
            if "htmlSourceGzip" not in dir():
                print("socket timed out, going to try again")
                continue
            htmlSource = htmlSourceGzip.decode('gbk')
        except Exception as e:
            print(e)
            exit()
        break;
    print("read ok!")
    return htmlSource

def getImageUrl(context):
    try:
        return re.search('<span id="J-BigPic">.*src="(.*?)".*</span>', context).group(1).rstrip()
    except Exception as e:
        return False

def writeLog(context):
    try:
        with open("errurl.data","a") as f:
            f.write(context + "\n")
    except Exception as e:
        print(e)
        exit()


if __name__ == "__main__":
    pageNum = getPage()
    pageEnd = 235
    host = "http://wallpaper.pconline.com.cn"
    while pageNum <= pageEnd:
        listUrl = host + "/list/1_b4_%d_des1.html" % (pageNum)
        listData = []

        listSource = getUrlSource(listUrl)
        if not listSource:
            pageNum += 1
            continue

        htmlUrlList = re.search('<ul class="ul-pic-a">(.*?)</ul>', listSource, 16).group()
        urlList = re.findall('<i class="i-txt"><a href="(.*?)"', htmlUrlList)

        # print(urlList)

        for albumUrl in urlList:
            firstPaperUrl = getUrlSource(host + albumUrl)
            if not firstPaperUrl:continue
            albumPageList = re.findall('"link":"(.*?)"', firstPaperUrl)
            albumImageList = []

            # print(albumPageList)

            for page in albumPageList:
                paperUrl = getUrlSource(host + page)
                if not paperUrl:
                    albumPageList.remove(page)
                    continue
                paperImage = getImageUrl(paperUrl)
                if paperImage:
                    albumImageList.append(paperImage)
                else:
                    albumPageList.remove(page)

            result = list(zip(albumPageList, albumImageList))
            if(albumPageList.__len__() != albumImageList.__len__()):
                exit('list neq')

            # print(mysqlInsert(result))

            listData.append(result)

            # print(listData)

        if mysqlInsert(listData):
            print("save ok!", end = "\n\n\n")
            pageNum += 1
            updatePage(pageNum)

    mysqlConnect.close()

