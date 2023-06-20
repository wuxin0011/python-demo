'''
王者荣耀官方 英雄壁纸爬取
'''
from os import getcwd as os_getcwd, path as os_path, makedirs as os_makedirs
from random import choice as random_choice
from re import search as re_search, match as re_match, sub as re_sub, M as re_M, I as re_I
from time import sleep as time_sleep

from bs4 import BeautifulSoup
from requests import get as req_get

# 默认hero
hero_info = [{'name': '云中君', 'url': 'https://pvp.qq.com/web201605/herodetail/506.shtml', 'hero_id': '506'},
             {'name': '瑶', 'url': 'https://pvp.qq.com/web201605/herodetail/505.shtml', 'hero_id': '505'},
             {'name': '盘古', 'url': 'https://pvp.qq.com/web201605/herodetail/529.shtml', 'hero_id': '529'},
             {'name': '猪八戒', 'url': 'https://pvp.qq.com/web201605/herodetail/511.shtml', 'hero_id': '511'},
             {'name': '嫦娥', 'url': 'https://pvp.qq.com/web201605/herodetail/515.shtml', 'hero_id': '515'},
             {'name': '上官婉儿', 'url': 'https://pvp.qq.com/web201605/herodetail/513.shtml', 'hero_id': '513'},
             {'name': '李信', 'url': 'https://pvp.qq.com/web201605/herodetail/507.shtml', 'hero_id': '507'},
             {'name': '沈梦溪', 'url': 'https://pvp.qq.com/web201605/herodetail/312.shtml', 'hero_id': '312'},
             {'name': '伽罗', 'url': 'https://pvp.qq.com/web201605/herodetail/508.shtml', 'hero_id': '508'},
             {'name': '盾山', 'url': 'https://pvp.qq.com/web201605/herodetail/509.shtml', 'hero_id': '509'},
             {'name': '司马懿', 'url': 'https://pvp.qq.com/web201605/herodetail/137.shtml', 'hero_id': '137'},
             {'name': '孙策', 'url': 'https://pvp.qq.com/web201605/herodetail/510.shtml', 'hero_id': '510'},
             {'name': '元歌', 'url': 'https://pvp.qq.com/web201605/herodetail/125.shtml', 'hero_id': '125'},
             {'name': '米莱狄', 'url': 'https://pvp.qq.com/web201605/herodetail/504.shtml', 'hero_id': '504'},
             {'name': '狂铁', 'url': 'https://pvp.qq.com/web201605/herodetail/503.shtml', 'hero_id': '503'},
             {'name': '弈星', 'url': 'https://pvp.qq.com/web201605/herodetail/197.shtml', 'hero_id': '197'},
             {'name': '裴擒虎', 'url': 'https://pvp.qq.com/web201605/herodetail/502.shtml', 'hero_id': '502'},
             {'name': '杨玉环', 'url': 'https://pvp.qq.com/web201605/herodetail/176.shtml', 'hero_id': '176'},
             {'name': '公孙离', 'url': 'https://pvp.qq.com/web201605/herodetail/199.shtml', 'hero_id': '199'},
             {'name': '明世隐', 'url': 'https://pvp.qq.com/web201605/herodetail/501.shtml', 'hero_id': '501'},
             {'name': '女娲', 'url': 'https://pvp.qq.com/web201605/herodetail/179.shtml', 'hero_id': '179'},
             {'name': '梦奇', 'url': 'https://pvp.qq.com/web201605/herodetail/198.shtml', 'hero_id': '198'},
             {'name': '苏烈', 'url': 'https://pvp.qq.com/web201605/herodetail/194.shtml', 'hero_id': '194'},
             {'name': '百里玄策', 'url': 'https://pvp.qq.com/web201605/herodetail/195.shtml', 'hero_id': '195'},
             {'name': '百里守约', 'url': 'https://pvp.qq.com/web201605/herodetail/196.shtml', 'hero_id': '196'},
             {'name': '铠', 'url': 'https://pvp.qq.com/web201605/herodetail/193.shtml', 'hero_id': '193'},
             {'name': '鬼谷子', 'url': 'https://pvp.qq.com/web201605/herodetail/189.shtml', 'hero_id': '189'},
             {'name': '干将莫邪', 'url': 'https://pvp.qq.com/web201605/herodetail/182.shtml', 'hero_id': '182'},
             {'name': '东皇太一', 'url': 'https://pvp.qq.com/web201605/herodetail/187.shtml', 'hero_id': '187'},
             {'name': '大乔', 'url': 'https://pvp.qq.com/web201605/herodetail/191.shtml', 'hero_id': '191'},
             {'name': '黄忠', 'url': 'https://pvp.qq.com/web201605/herodetail/192.shtml', 'hero_id': '192'},
             {'name': '诸葛亮', 'url': 'https://pvp.qq.com/web201605/herodetail/190.shtml', 'hero_id': '190'},
             {'name': '哪吒', 'url': 'https://pvp.qq.com/web201605/herodetail/180.shtml', 'hero_id': '180'},
             {'name': '太乙真人', 'url': 'https://pvp.qq.com/web201605/herodetail/186.shtml', 'hero_id': '186'},
             {'name': '蔡文姬', 'url': 'https://pvp.qq.com/web201605/herodetail/184.shtml', 'hero_id': '184'},
             {'name': '雅典娜', 'url': 'https://pvp.qq.com/web201605/herodetail/183.shtml', 'hero_id': '183'},
             {'name': '杨戬', 'url': 'https://pvp.qq.com/web201605/herodetail/178.shtml', 'hero_id': '178'},
             {'name': '成吉思汗', 'url': 'https://pvp.qq.com/web201605/herodetail/177.shtml', 'hero_id': '177'},
             {'name': '钟馗', 'url': 'https://pvp.qq.com/web201605/herodetail/175.shtml', 'hero_id': '175'},
             {'name': '虞姬', 'url': 'https://pvp.qq.com/web201605/herodetail/174.shtml', 'hero_id': '174'},
             {'name': '李元芳', 'url': 'https://pvp.qq.com/web201605/herodetail/173.shtml', 'hero_id': '173'},
             {'name': '张飞', 'url': 'https://pvp.qq.com/web201605/herodetail/171.shtml', 'hero_id': '171'},
             {'name': '刘备', 'url': 'https://pvp.qq.com/web201605/herodetail/170.shtml', 'hero_id': '170'},
             {'name': '后羿', 'url': 'https://pvp.qq.com/web201605/herodetail/169.shtml', 'hero_id': '169'},
             {'name': '牛魔', 'url': 'https://pvp.qq.com/web201605/herodetail/168.shtml', 'hero_id': '168'},
             {'name': '孙悟空', 'url': 'https://pvp.qq.com/web201605/herodetail/167.shtml', 'hero_id': '167'},
             {'name': '亚瑟', 'url': 'https://pvp.qq.com/web201605/herodetail/166.shtml', 'hero_id': '166'},
             {'name': '橘右京', 'url': 'https://pvp.qq.com/web201605/herodetail/163.shtml', 'hero_id': '163'},
             {'name': '娜可露露', 'url': 'https://pvp.qq.com/web201605/herodetail/162.shtml', 'hero_id': '162'},
             {'name': '不知火舞', 'url': 'https://pvp.qq.com/web201605/herodetail/157.shtml', 'hero_id': '157'},
             {'name': '张良', 'url': 'https://pvp.qq.com/web201605/herodetail/156.shtml', 'hero_id': '156'},
             {'name': '花木兰', 'url': 'https://pvp.qq.com/web201605/herodetail/154.shtml', 'hero_id': '154'},
             {'name': '兰陵王', 'url': 'https://pvp.qq.com/web201605/herodetail/153.shtml', 'hero_id': '153'},
             {'name': '王昭君', 'url': 'https://pvp.qq.com/web201605/herodetail/152.shtml', 'hero_id': '152'},
             {'name': '韩信', 'url': 'https://pvp.qq.com/web201605/herodetail/150.shtml', 'hero_id': '150'},
             {'name': '刘邦', 'url': 'https://pvp.qq.com/web201605/herodetail/149.shtml', 'hero_id': '149'},
             {'name': '姜子牙', 'url': 'https://pvp.qq.com/web201605/herodetail/148.shtml', 'hero_id': '148'},
             {'name': '露娜', 'url': 'https://pvp.qq.com/web201605/herodetail/146.shtml', 'hero_id': '146'},
             {'name': '程咬金', 'url': 'https://pvp.qq.com/web201605/herodetail/144.shtml', 'hero_id': '144'},
             {'name': '安琪拉', 'url': 'https://pvp.qq.com/web201605/herodetail/142.shtml', 'hero_id': '142'},
             {'name': '貂蝉', 'url': 'https://pvp.qq.com/web201605/herodetail/141.shtml', 'hero_id': '141'},
             {'name': '关羽', 'url': 'https://pvp.qq.com/web201605/herodetail/140.shtml', 'hero_id': '140'},
             {'name': '老夫子', 'url': 'https://pvp.qq.com/web201605/herodetail/139.shtml', 'hero_id': '139'},
             {'name': '武则天', 'url': 'https://pvp.qq.com/web201605/herodetail/136.shtml', 'hero_id': '136'},
             {'name': '项羽', 'url': 'https://pvp.qq.com/web201605/herodetail/135.shtml', 'hero_id': '135'},
             {'name': '达摩', 'url': 'https://pvp.qq.com/web201605/herodetail/134.shtml', 'hero_id': '134'},
             {'name': '狄仁杰', 'url': 'https://pvp.qq.com/web201605/herodetail/133.shtml', 'hero_id': '133'},
             {'name': '马可波罗', 'url': 'https://pvp.qq.com/web201605/herodetail/132.shtml', 'hero_id': '132'},
             {'name': '李白', 'url': 'https://pvp.qq.com/web201605/herodetail/131.shtml', 'hero_id': '131'},
             {'name': '宫本武藏', 'url': 'https://pvp.qq.com/web201605/herodetail/130.shtml', 'hero_id': '130'},
             {'name': '典韦', 'url': 'https://pvp.qq.com/web201605/herodetail/129.shtml', 'hero_id': '129'},
             {'name': '曹操', 'url': 'https://pvp.qq.com/web201605/herodetail/128.shtml', 'hero_id': '128'},
             {'name': '甄姬', 'url': 'https://pvp.qq.com/web201605/herodetail/127.shtml', 'hero_id': '127'},
             {'name': '夏侯惇', 'url': 'https://pvp.qq.com/web201605/herodetail/126.shtml', 'hero_id': '126'},
             {'name': '周瑜', 'url': 'https://pvp.qq.com/web201605/herodetail/124.shtml', 'hero_id': '124'},
             {'name': '吕布', 'url': 'https://pvp.qq.com/web201605/herodetail/123.shtml', 'hero_id': '123'},
             {'name': '芈月', 'url': 'https://pvp.qq.com/web201605/herodetail/121.shtml', 'hero_id': '121'},
             {'name': '白起', 'url': 'https://pvp.qq.com/web201605/herodetail/120.shtml', 'hero_id': '120'},
             {'name': '扁鹊', 'url': 'https://pvp.qq.com/web201605/herodetail/119.shtml', 'hero_id': '119'},
             {'name': '孙膑', 'url': 'https://pvp.qq.com/web201605/herodetail/118.shtml', 'hero_id': '118'},
             {'name': '钟无艳', 'url': 'https://pvp.qq.com/web201605/herodetail/117.shtml', 'hero_id': '117'},
             {'name': '阿轲', 'url': 'https://pvp.qq.com/web201605/herodetail/116.shtml', 'hero_id': '116'},
             {'name': '高渐离', 'url': 'https://pvp.qq.com/web201605/herodetail/115.shtml', 'hero_id': '115'},
             {'name': '刘禅', 'url': 'https://pvp.qq.com/web201605/herodetail/114.shtml', 'hero_id': '114'},
             {'name': '庄周', 'url': 'https://pvp.qq.com/web201605/herodetail/113.shtml', 'hero_id': '113'},
             {'name': '鲁班七号', 'url': 'https://pvp.qq.com/web201605/herodetail/112.shtml', 'hero_id': '112'},
             {'name': '孙尚香', 'url': 'https://pvp.qq.com/web201605/herodetail/111.shtml', 'hero_id': '111'},
             {'name': '嬴政', 'url': 'https://pvp.qq.com/web201605/herodetail/110.shtml', 'hero_id': '110'},
             {'name': '妲己', 'url': 'https://pvp.qq.com/web201605/herodetail/109.shtml', 'hero_id': '109'},
             {'name': '墨子', 'url': 'https://pvp.qq.com/web201605/herodetail/108.shtml', 'hero_id': '108'},
             {'name': '赵云', 'url': 'https://pvp.qq.com/web201605/herodetail/107.shtml', 'hero_id': '107'},
             {'name': '小乔', 'url': 'https://pvp.qq.com/web201605/herodetail/106.shtml', 'hero_id': '106'},
             {'name': '廉颇', 'url': 'https://pvp.qq.com/web201605/herodetail/105.shtml', 'hero_id': '105'}]

# 代理头
list_useragent = [
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 "
    "Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36 Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36",
    "Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 Safari/537.14",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
    "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10",
    "Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko ) Version/5.1 Mobile/9B176 Safari/7534.48.3",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; da-dk) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; tr-TR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; ko-KR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; fr-FR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; cs-CZ) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; ja-JP) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; ja-jp) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; ja-jp) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; sv-se) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; ko-kr) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; ja-jp) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; it-it) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; fr-fr) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; es-es) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-us) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-gb) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; de-de) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; sv-SE) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; ja-JP) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; de-DE) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; hu-HU) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; de-DE) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; ja-JP) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; it-IT) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-us) AppleWebKit/534.16+ (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; fr-ch) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; de-de) AppleWebKit/534.15+ (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; ar) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
    "Mozilla/5.0 (Android 2.2; Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-HK) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; tr-TR) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; nb-NO) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; fr-FR) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-TW) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; zh-cn) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5"
]


def hero_is_exist(name):
    """
    检查英雄名称是否存在本地 如果本地不存在走网络请求
    :param name: 英雄名称
    :return: 英雄基本信息
    """
    # 检查 name 是否被禁止
    if name in must_not_exist:
        print(f"{name} 该名称不存在 请输入正确名称 ")
        return

    for hero in hero_info:
        if hero['name'] == name:
            return hero

    # 而且 hero_info_list
    if type(hero_info_list) == list and len(hero_info_list) == 0:
        # 如果本地找不到从网络中找
        get_hero_list(init_url)
        time_sleep(random_choice([1, 2, 3]))
    # 更新本地缓存
    for hero in hero_info_list:
        if hero['name'] == name:
            # 如果找到了更新 hero_info_list
            #  更新缓存
            hero_info.append(hero)
            return hero

    # 如果还是没找到说明该hero一定不存在 添加到缓存中
    must_not_exist.append(name)
    print(f"{name} 该名称不存在 请输入正确名称 ")
    return None


def get_fake_userAgent():
    """
    随机请求头
    :return:
    """
    return {
        'User-Agent': random_choice(list_useragent)
    }


def get_response(url):
    """
    对请求响应
    :param url: 地址
    :return: html
    """

    try:
        time_sleep(random_choice([1, 2, 3]))
        response = req_get(url=url, headers=get_fake_userAgent())
        if response and response.status_code == 200:
            return response.content
        else:
            return None
    except Exception as e:
        print(f"响应失败{url}", e)
        return None


def save_local_path():
    """
    保存路径
    :return:
    """
    return os_getcwd() + '\\img'


def parse_single_hero_data(url):
    """
    响应
    :param url: 响应地址
    :return:
    """
    response = get_response(url)
    if response is None:
        print(f"响应失败！可能是响应结果错误或者改地址不存在！{url}")
        return
    res = response.decode('gbk')
    # 获取英雄id
    hero_id = re_search(r'/\d+\.shtml', url)[0].replace('/', '').replace('.shtml', '')
    if res:
        soup = BeautifulSoup(res, 'lxml')
        # 英雄名称
        hero_name = soup.select_one('div.cover h2.cover-name').get_text()
        hero_skin_name_list = soup.select('ul.pic-pf-list.pic-pf-list3')[0]['data-imgname']
        hero_skin_name_list = re_sub(r'(&\d+)', '', hero_skin_name_list, re_M).split('|')
        # 皮肤遍历下载
        # 创建文件夹
        save_hero_skin(hero_id, hero_name, hero_skin_name_list)


def save_hero_skin(hero_id, hero_name, hero_skin_link_list):
    """
    保存皮肤
    :param hero_id: 英雄ID
    :param hero_name: 英雄名称
    :param hero_skin_link_list: 皮肤地址
    :return:
    """
    path = f'{save_local_path()}//{hero_name}'
    if not os_path.exists(path):
        os_makedirs(path)
    for i, skin_name in enumerate(hero_skin_link_list):
        try:
            link = skin_skin_link.format(hero_id, hero_id, i + 1)
            content = get_response(link)
            if content:
                with open(f'{path}//{skin_name}.jpg', mode='wb') as file:
                    file.write(content)
                    print(f'{hero_name} {skin_name}', '下载成功')
            else:
                print(f'{hero_name} {skin_name} 下载失败')
        except Exception as e:
            print(f'{hero_name} {skin_name} 下载失败！ =================> {e}')


def get_hero_list(url):
    """
    获取英雄信息
    :param url: 地址
    :return:
    """
    response = get_response(url)
    if response is None:
        print("响应失败！", url)
        return
    data = response.decode('gbk')
    if data:
        soup = BeautifulSoup(data, 'lxml')
        result_list = soup.select('ul.herolist.clearfix li a')
        if list == type(result_list):
            for index, hero_link in enumerate(result_list):
                try:
                    # 地址拼接替换
                    hero_url = f'{root_url}{hero_link["href"]}'
                    name = hero_link.text
                    result = re_search("\\d+", hero_link["href"])
                    hero_info_list.append({
                        'name': name,
                        'url': hero_url,
                        'hero_id': result.group()
                    })
                except:
                    pass
    else:
        return []


def input_name_download():
    """
    输入名称方式下载
    :return:
    """
    while True:
        hero_name = input("请输入要下载英雄名称: ")
        result = hero_is_exist(hero_name)
        if result:
            print(f"保存地址: {save_local_path()}\\{hero_name}")
            parse_single_hero_data(result['url'])
        else:
            pass
        ok = input("继续输入英雄下载壁纸操作？: y or n ")
        if ok == 'Y' or ok == 'y':
            continue
        else:
            break


def input_hero_url_download():
    """
     输入地址方式下载
    :return:
    """
    while True:
        hero_url = input("请输入要下载的地址: ")
        result = re_match(r'https://pvp.qq.com/web201605/herodetail/\d+.shtml', hero_url)
        if result:
            print(f"保存地址: {save_local_path()}")
            parse_single_hero_data(hero_url)
        else:
            print("地址匹配错误:请输入 https://pvp.qq.com/web201605/herodetail/xxxx.shtml 形式地址")
            print("示例地址:  https://pvp.qq.com/web201605/herodetail/162.shtml ")
            continue
        ok = input("继续输入英雄地址下载壁纸操作？: y or n ")
        if ok == 'Y' or ok == 'y':
            continue
        else:
            break


def all_hero_download():
    """
    全部下载
    :return:
    """
    # 从网络中获取全部信息
    get_hero_list(init_url)
    print(f"保存地址: {save_local_path()}")
    for hero in hero_info_list:
        parse_single_hero_data(hero['url'])


def start():
    """
    执行
    :return:
    """
    while True:
        download_type = input("请输入序号 1:输入英雄名称(默认) 2：输入地址 3：全部下载 ")
        if download_type == '1' or download_type == '':
            input_name_download()
        elif download_type == '2':
            input_hero_url_download()
        else:
            all_hero_download()
        ok = input("继续选择下载类型操作？: y or n ")
        if ok == 'Y' or ok == 'y':
            continue
        else:
            break


if __name__ == '__main__':
    must_not_exist = []
    hero_info_list = []
    root_url = 'https://pvp.qq.com/web201605/'
    init_url = 'https://pvp.qq.com/web201605/herolist.shtml'
    skin_skin_link = 'https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{}/{}-bigskin-{}.jpg'
    start()
