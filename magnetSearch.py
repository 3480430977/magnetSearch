from urllib.request import urlopen, Request  # urlopen：打开网页，Request：伪装请求头
from urllib.parse import quote  # 解析含有中文的URL
import re  # 正则模块
from threading import Thread  # 多线程
# 请求头信息，伪装成浏览器
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                         "63.0.3239.26 Safari/537.36 Core/1.63.6756.400 QQBrowser/10.3.2473.400"}


# 定义每个线程的target
def fun(page, k):
    """
    线程的target
    :param page: 页
    :param k: 关键字
    :return: 无返回值，直接输出结果
    """
    # 使用try...except...排除异常
    try:
        # 创建请求对象
        request = Request(f"https://www.btbook.tv/search/{k}/last-{page}.html", headers=headers)
        # 接受请求响应
        response = urlopen(request).read().decode()
        # url的正则
        url_pattern = re.compile(r'<a.*?href="(/wiki/.*?\.html)".*?>')
        # 将匹配的结果放到一个列表中
        url_list = url_pattern.findall(response)
        # 遍历列表
        for url in url_list:
            request = Request(f"https://www.btbook.tv{url}", headers=headers)
            response = urlopen(request).read().decode()
            # 名称正则
            name_pattern = re.compile(r'<h2>(.*?)</h2>')
            # 获取名称
            name = name_pattern.findall(response)[0]
            # 大小正则
            size_pattern = re.compile(r'<td>(.*?)\xa0(.*?)</td>')
            # 获取大小
            value, union = size_pattern.findall(response)[0]  # value：值，union：单位
            size = value + union  # 值和单位拼接起来就是大小
            # 磁力链接的正则
            magnet_pattern = re.compile(r'<a href="magnet:\?xt=urn:btih:.*?">(magnet:\?xt=urn:btih:.*?)</a>')
            # 获取磁力链接
            magnet = magnet_pattern.findall(response)[0]
            # 迅雷链接的正则
            thunder_pattern = re.compile(r'<a href="thunder://.*?==">(thunder://.*?==)</a>')
            # 获取迅雷链接
            thunder = thunder_pattern.findall(response)[0]
            # 输出信息
            print(f"名称：{name}\n大小：{size}\n磁力链接：{magnet}\n迅雷链接：{thunder}\n")
    except BaseException as e:
        str(e)  # 走个形式


key = quote(input("请输入关键字："))
# 创建一个线程列表，列表中的每一个元素是一个线程对象
thread_list = [Thread(target=fun, args=(i, key))for i in range(1, 101)]
# 遍历列表，启动线程
for thread in thread_list:
    thread.start()
# 将每个线程调用join方法，阻塞主线程（防止主线程先执行完）
for thread in thread_list:
    thread.join()
input("按回车键继续...")  # 防止打包之后执行exe程序一结束就闪退
