import requests
from bs4 import BeautifulSoup
import csv

# 1. 设置请求头（模拟浏览器访问）
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 2. 抓取数据
def scrape_douban_top250():
    base_url = "https://movie.douban.com/top250"
    movies = []
    
    for page in range(0, 250, 25):  # 每页25条，共10页
        url = f"{base_url}?start={page}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 解析电影信息
        for item in soup.find_all('div', class_='item'):
            title = item.find('span', class_='title').text
            rating = item.find('span', class_='rating_num').text
            movies.append({'title': title, 'rating': rating})
    
    return movies

# 3. 保存为CSV文件
def save_to_csv(movies, filename='douban_top250.csv'):
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'rating'])
        writer.writeheader()
        writer.writerows(movies)

if __name__ == '__main__':
    movies = scrape_douban_top250()
    save_to_csv(movies)
    print(f"成功抓取 {len(movies)} 条数据，已保存到 douban_top250.csv")