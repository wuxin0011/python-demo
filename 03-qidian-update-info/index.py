# 系统内置模块
import json
import math
import os.path
from ast import literal_eval
from datetime import datetime
from json import loads as json_loads
from re import match as re_match, search as re_search, compile as re_compile

# 第三方模块
from bs4 import BeautifulSoup
from openpyxl.workbook import Workbook
from requests import get as req_get


def is_leap_year(year):
    """
    判断给定的年份是否为闰年。
    如果是闰年，返回 True；否则返回 False。
    """
    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
        return True
    else:
        return False


def get_month_day(year, month):
    '''
    根据年份和月份获取当前月份天数
    '''
    year = int(year)
    month = int(month)
    if month == 2:
        if is_leap_year(year):
            return 29
        else:
            return 28
    month_day_dict = {
        '1': 31,
        '3': 31,
        '4': 30,
        '5': 31,
        '6': 30,
        '7': 31,
        '8': 31,
        '9': 30,
        '10': 31,
        '11': 30,
        '12': 31,
    }
    return month_day_dict[f'{month}']


def download_page(url):
    '''
    请求 url 内容
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/47.0.2526.80 Safari/537.36'
    }
    try:
        data = req_get(url, headers=headers)
        if data.status_code == 200:
            return data.content
        else:
            raise Exception("响应失败!")
    except Exception as e:
        print(f"请求失败:{e}")
        return None


def check_version_file_is_exist():
    '''
    检查版本文件是否存在
    '''
    if check_file("json", bookId):
        # 获取文件名
        file = open(f'{get_full_path("json", bookId)}', mode='r', encoding='utf-8')
        info = json_loads(file.read())
        if type(info) == dict:
            title = info['title']
            if title is not None:
                res = response_html(title)
                return {
                    'title': title,
                    'urls': res['urls']
                }

    res = response_html()

    with open(f'{get_full_path("json", bookId)}', mode="w", encoding="utf-8") as file:
        file.write(str(json.dumps({
            'title': res['title'],
            "bookId": bookId
        })))
        print(f'版本信息文件: {save_location}{bookId}.json 格式保存成功！')
        file.close()

    return {
        'title': res['title'],
        'urls': res['urls']
    }


def check_url_is_ok():
    '''
    检查链接是否符合规范
    '''
    global save_file_name
    this_input_url = input_url

    # 检查地址是否规范
    save_file_name = re_compile("\\d+").findall(this_input_url)[0]
    global req_url
    req_url = f"https://book.qidian.com/info/{save_file_name}/#Catalog"

    global bookId
    bookId = save_file_name
    res = check_version_file_is_exist()
    title = res['title']
    urls = res['urls']
    print('书名ID:', save_file_name, "书名:", title)
    save_all_chapter_info_to_json(title, urls)
    return True


def find_first_index(urls):
    '''
    查找第一章出现位置
    '''
    index = 0
    for data in urls:
        str1 = data.get('title')
        if re_match(".*第一章.*", str1):
            return index
        index = index + 1
    return 1


def write_xlsx(xlsx_list, name, header_map=None, override=False):
    '''
    写入文件格式为 xlsx_list
    '''
    try:
        if header_map is None:
            header_map = {'link': '链接', 'chapterName': '章节名', 'publishDate': '发布日期', "size": '大小'}
            # 定义列表型字典
        new_data_list = [{header_map[col]: row_data[col] for col in row_data} for row_data in xlsx_list]
        # 检查文件是否存在
        # 写入格式为 xlsx
        wb = Workbook()
        # 获取当前活跃的工作表（第一个工作表）
        ws = wb.active
        # 写入表头
        header = list(header_map.values())
        ws.append(header)
        # 写入数据
        for row_data in new_data_list:
            data = [row_data[col] for col in header]
            ws.append(data)
        wb.save(get_full_path("xlsx", name))
        print(f'{get_full_path("xlsx", name)} 保存成功')

        return True
    except Exception as e:
        print(f'xlsx 格式保存失败 {e}！')
        return False


def write_json(data_list, name, override=False):
    '''
    吸入格式为json格式
    '''
    try:
        if not check_file("json", name) or override == True:
            with open(f'{get_full_path("json", name)}', mode="w", encoding="utf-8") as file:
                file.write(str(json.dumps(data_list)))
                print(f'{get_full_path("json", name)} 保存成功！')
                file.close()
        return True
    except Exception as e:
        print(f'json 格式保存失败{e}！')
        return False


def write_html(html_content, name):
    '''
    写入html文档
    html_content html 内容
    name 默认名称 默认为 bookName
    '''
    try:
        if html_content is None:
            html_content = response_html()['html_content']
        with open(get_full_path("html", name), encoding='utf-8', mode='w') as file:
            file.write(html_content)
            print(f'{get_full_path("html", name)}.html 保存成功！')
            file.close()
        return True
    except Exception as e:
        print(f"html文档保存失败{e}！")
        return False


def response_html(name=None, override=False):
    # 使用bx解析 html格式内容
    html_content = None
    if check_file("html", name) and name is not None:
        read_file = open(get_full_path("html", name), mode="r", encoding="utf-8")
        html_content = read_file.read()
        read_file.close()
    if html_content is None:
        html_content = download_page(req_url).decode("utf-8")
        override = True
    soup = BeautifulSoup(markup=html_content, features='html.parser')
    # 书名
    name = soup.select_one("div.book-detail-wrap div.book-information div.book-info em").text
    # 地址信息
    urls = soup.select("div.volume-wrap .volume ul.cf li a")
    # 确认覆盖源文件
    if html_content is None or name is None or urls is None or override:
        write_html(html_content, name)
    return {
        "title": name,
        "urls": urls,
        "html_content": html_content
    }


def save_all_chapter_info_to_json(name, urls=None):
    '''
    将内容保存为json格式
    '''
    '''全部章节内容转换为json信息'''
    if name is not None and check_file("json", name):
        format_json_file(name)
        return;
    if urls is None or len(urls) == 0:
        urls = response_html(name, True)["urls"]
    if urls is None or len(urls) == 0:
        print(f"请求失败 请检查书籍地址 {req_url} 是否可访问！")
        return
        # 变量
    try:
        # 获取全部章节内容:
        ALL_LINK_INFO = []
        # 文件内容读取
        xlsx_list = []
        index = find_first_index(urls)
        for content in urls[index:]:
            link = "https:" + content.get('href')
            new_content = parse_re_urls_content(content.get('title'), link, name)
            ALL_LINK_INFO.append(str(new_content))
            xlsx_list.append(new_content)

        write_xlsx(xlsx_list, name, None, True)
        # 开始解析文件
        write_json(ALL_LINK_INFO, name)
        format_json_file(name)
    except Exception as E:
        print(f'json 格式保存异常:{E}')


def parse_re_urls_content(content, link, bookName):
    publishDate = None
    size = None
    # 匹配日期
    se = re_search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", content)
    if se:
        publishDate = se.group(1)
    #     匹配章节字数
    se1 = re_search(r"(\d+$)", content)
    if se1:
        size = se1.group(1)
    chapterName = content \
        .replace("首发时间", "") \
        .replace("：", "") \
        .replace("章节字数", "") \
        .replace(f"{publishDate}", "") \
        .replace(f"{size}", "") \
        .replace(f"{bookName}", "") \
        .replace(" ", "")
    return {
        "link": link,
        "chapterName": chapterName,
        "publishDate": publishDate,
        "size": size,
    }


def check_file(ext='json', fileName=None):
    '''
    检查文件是否存在
    @params ext 文件后缀
    '''
    if fileName is None:
        fileName = save_file_name
    if not os.path.exists(get_dir_file()):
        os.makedirs(get_dir_file())
    return os.path.exists(f'{get_full_path(ext, fileName)}')


def check_data_is_exist(new_data, d):
    '''
    检查日期是否存在
    '''
    if new_data is None:
        return False
    return f'{d}' in new_data


def format_json_file(name):
    """
    解析json中文件内容
    """
    if not check_file("json", name):
        print(f"文件 {get_full_path('json', name)}.json 不存在")
        res = check_version_file_is_exist(bookId)
        save_all_chapter_info_to_json(res['title'], res["urls"])

    new_data = {}
    try:
        file = open(f'{get_full_path("json", name)}', mode="r", encoding="utf-8")
        data = json_loads(file.read())
        file.close()
        format_str1 = '%Y-%m-%d %H:%M:%S'
        for str1 in data:
            str1 = literal_eval(str1)
            # 过滤不规范数据
            if re_match(".*\d+", str1['chapterName']):
                pass
            else:
                try:
                    datetime_obj = datetime.strptime(str1['publishDate'], format_str1)
                    date = datetime_obj.time()
                    content = {
                        'year': datetime_obj.year,
                        'month': datetime_obj.month,
                        'day': datetime_obj.day,
                        'time': f'{get_format_date(date.hour)}:{get_format_date(date.minute)}:{get_format_date(date.second)}',
                        'date': str1['publishDate'],
                        'chapterName': str1['chapterName'],
                        'size': str1['size']
                    }
                    Y = content["year"]
                    M = content["month"]
                    # 检查年份是否存在
                    y_ok = check_data_is_exist(new_data, Y)

                    if y_ok:
                        # 检查月份是否存在
                        m_ok = check_data_is_exist(new_data[f'{Y}'], M)
                        if m_ok:
                            new_data[f'{Y}'][f'{M}'].append(content)
                        else:
                            new_data[f'{Y}'][f'{M}'] = [content]
                    else:
                        new_data[f'{Y}'] = {
                            f'{M}': [content]
                        }
                except Exception as e:
                    # print("e", e, "data = ", str1)
                    pass

    except Exception as e:
        print(f"格式化异常信息：{e}")
    data_info = {}
    for key, value in new_data.items():
        if check_data_is_exist(data_info, key):
            pass
        else:
            data_info[f'{key}'] = {
                'year': parse_int_size(key),
                'total_update_num': 0,
                'no_update_day': 0,
                'update_day': 0,
                'total_size': 0,
                'average_size': 0,
                'update_num_max_month': None,
                'update_num_min_month': None,
                'update_info': []
            }
        for key1, value1 in value.items():
            d = parse_data(key, key1, value1)
            if type(d) == dict:
                data_info[f'{key}']['update_info'].append(d)
                data_info[f'{key}']['total_update_num'] = data_info[f'{key}']['total_update_num'] + d[
                    'total_update_num']
                data_info[f'{key}']['update_day'] = data_info[f'{key}']['update_day'] + d['update_day']
                data_info[f'{key}']['no_update_day'] = data_info[f'{key}']['no_update_day'] + d['no_update_day']
                data_info[f'{key}']['total_size'] = data_info[f'{key}']['total_size'] + d['total_size']
                data_info[f'{key}']['average_size'] = math.floor(data_info[f'{key}']['total_size'] / (
                        data_info[f'{key}']['update_day'] + data_info[f'{key}']['no_update_day']))

                # max
                if data_info[f'{key}']['update_num_max_month'] is not None:
                    before = data_info[f'{key}']['update_num_max_month']
                    if before['total_update_num'] < d['total_update_num']:
                        data_info[f'{key}']['update_num_max_month'] = d
                else:
                    data_info[f'{key}']['update_num_max_month'] = d

                # min
                if data_info[f'{key}']['update_num_min_month'] is not None:
                    before = data_info[f'{key}']['update_num_max_month']
                    if before['total_update_num'] > d['total_update_num']:
                        data_info[f'{key}']['update_num_min_month'] = d
                else:
                    data_info[f'{key}']['update_num_min_month'] = d

    # print(data_info)
    month_xlsx_info_list = []
    year_xlsx_info_list = []

    for key, value in data_info.items():
        print_info(key, value, name, month_xlsx_info_list)
        if type(value) == dict:
            del value["update_info"]
            del value["update_num_max_month"]
            del value["update_num_min_month"]
            year_xlsx_info_list.append(value)
    header_map_month = {'month': '年月', 'total_size': '更新总字数', 'average_size': '当月平均字数',
                        "total_update_num": "更新章节数", "update_day": '更新天数', 'no_update_day': "断更天数"}

    write_xlsx(month_xlsx_info_list, f'{name}-全部年月份更新总结', header_map_month, False)

    header_map_year = {'year': '年', 'total_size': '更新总字数', 'average_size': '当月平均字数',
                       "total_update_num": "更新章节数", "update_day": '更新天数', 'no_update_day': "断更天数",
                       }

    # print(year_xlsx_info_list)
    write_xlsx(year_xlsx_info_list, f'{name}-年度更新总结', header_map_year, False)


def get_dir_file():
    return f'{save_location}{bookId}'


def get_full_path(ext, filename):
    return f'{get_dir_file()}//{filename}.{ext}'


def print_info(year, data, name, xlsx_info_list):
    # print(f'====================={year}====================')
    # print("data", data)
    header_map = {'month': '年月', 'total_size': '更新总字数', 'average_size': '当月平均字数',
                  "total_update_num": "更新章节数", "update_day": '更新天数', 'no_update_day': "断更天数"}

    for i in data['update_info']:
        i['month'] = f'{year}-{i["month"]}'
        if type(xlsx_info_list) == list:
            xlsx_info_list.append(i)
    # write_xlsx(data['update_info'], f'{name}-{year}-年度更新总结', header_map, False)


def parse_data(year, month, value):
    # print(year, month, value)
    l = len(value)
    d = {'month': parse_int_size(month), 'total_size': parse_int_size(value[0]['size']), 'average_size': 0,
         'update_day': get_month_day(year, month),
         'no_update_day': 0, 'total_update_num': l}
    for i in range(1, l):
        # print('是否断更:', is_no_update(value[i - 1]['date'], value[i]['date']))
        if not is_no_update(value[i - 1]['date'], value[i]['date']):
            d['no_update_day'] = d['no_update_day'] + 1
            d['update_day'] = d['update_day'] - 1
        d['total_size'] = d['total_size'] + parse_int_size(value[i]['size'])

    d['average_size'] = math.floor(d['total_size'] / l)

    return d


def parse_int_size(str_num):
    '''
    格式化字符串
    '''
    try:
        return math.floor(int(str_num))
    except:
        return 0


def is_no_update(time1, time2):
    '''
    检查是否断更
    '''
    # 将两个字符串解析成 datetime 对象
    try:
        time1 = datetime.strptime(time1, "%Y-%m-%d %H:%M:%S")
        time2 = datetime.strptime(time2, "%Y-%m-%d %H:%M:%S")

        # 计算时间差，并打印出小时数
        delta = time2 - time1
        hours = delta.total_seconds() / 3600

        # 如果时间小于24小时或者间隔天数小于1或等于1 ，则认为是没有断更
        return hours < 24 or (time2.day - time1.day) <= 1
    except:
        return False


def get_format_date(t):
    if t < 10:
        return f'0{t}'
    else:
        return f'{t}'


def run():
    global input_url
    while True:
        print("示例地址1: https://book.qidian.com/info/1032778366/#Catalog")
        print("示例地址2: https://book.qidian.com/info/1031940621/\n")

        url = input("请输入地址 输入 1 或者 2 或者不输入 使用示例地址: ")

        if url != '1' or url != '2' or url != '':
            input_url = url
        if url == '1' or url == '':
            input_url = 'https://book.qidian.com/info/1032778366'
        if url == '2':
            input_url = 'https://book.qidian.com/info/1031940621'

        print(f"\n你输入地址为:{input_url}\n")
        if re_match(r"https://book.qidian.com/info/\d+", input_url) is None:
            print("匹配失败:请输入{}形式地址 xxx 为书籍ID序号 ".format("https://book.qidian.com/info/xxxx"))
            continue

        check_url_is_ok()
        answer = input("\n继续？ Y or y : ")
        if answer == 'y' or answer == 'Y' or answer == 'Yes' or answer == 'yes':
            continue
        else:
            print("\n拜拜！")
            break


if __name__ == '__main__':
    global save_location
    save_location = "D://desktop//qidian_novel//"

    run()
