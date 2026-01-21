import re
import requests
import pandas as pd

results = []
# 获得HTML
def toscrape_api(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0"
    }
    response = requests.get(url,headers = headers)
    if response.status_code == 200:
        return response.text
    else:
        print("请求未成功")
    return 0

# 构造列表页，并获得列表页的HTML
def toscrape_index(page):
    url = f'https://books.toscrape.com/catalogue/page-{page}.html'
    return toscrape_api(url)

# 获取详情页网址后缀
def toscrape_index_href(html):
    # 创建正则捕获对象，方便复用
    index_pattern = re.compile('<a href="(.*?)" title=".*?"')
    detail = re.findall(index_pattern,html)
    for item in detail:
        index_href = f'https://books.toscrape.com/catalogue/{item}'
        yield index_href

# 获取详情页的HTML
def toscrape_detail(href):
    return toscrape_api(href)

# 构造详情页的正则(书名、价格、库存、评级、产品描述)
def toscrape_compile(html):

    detail_pattern = re.compile(r'<h1>(.*?)</h1>\s+'  # 书名
                                '<p class="price_color">(.*?)</p>.*?'  # 价格
                                '<p class="star-rating (.*?)">.*?'  # 评级
                                '<p>(.*?)</p>.*?'  # 产品描述
                                '<td>In stock \(\s*(\d+)\s*available\)</td>'  # 库存
                                ,re.S)
    detail_results = re.findall(detail_pattern,html)  # 进行正则匹配
    for result in detail_results:
        name = result[0] if result[0] else None
        preice = result[1] if result[0] else None
        stock = result[4] if result[0] else None
        evaluate = result[2] if result[0] else None
        describe = result[3] if result[0] else None
        detail_result = {
            '书名':name,
            '价格':preice,
            '库存':stock,
            '评级':evaluate,
            '产品描述':describe
        }
        results.append(detail_result)
    return 0

# 写入csv文件
def save_to_csv(results):
    df = pd.DataFrame(results)
    df.to_csv('toscrape详情页内容.csv', index=False, encoding='utf-8-sig')  # 使用 utf-8 编码

# 主程序
def main():
    for page in range(1,3):
        html = toscrape_index(page)
        index_href = toscrape_index_href(html)
        for href in index_href:
            print(href)
            html = toscrape_detail(href)
            toscrape_compile(html)
            print(results)
    save_to_csv(results)

if __name__ == '__main__':
    main()
