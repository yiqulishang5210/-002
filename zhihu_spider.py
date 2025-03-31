import requests
from bs4 import BeautifulSoup
import json
import time

# 1. 配置请求头（已整合你的Cookie）
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Cookie': '_zap=4f6a07c0-2192-49d6-9e1e-1ec67c0c659c; d_c0=ELUTxu7WKBqPTtuEkmZu4fF5Wyd8thPkf2I=|1742197296; __snaker__id=hjredoXwRVuSBKXz; gdxidpyhxdE=Z%2BsBZvq%5C1dxeXTbVnOxIWRwqwGE6ohg%5CXfeqX%5CSxOJ7jVbidWyWmQr1b78Sczc3sryTTOnrJmmisWmCiG%5CX2bKExCtKpMt1%2FrTke8YmJRDH%2Bxiin7rt3%5C1tNsBm1airpCjHecEVctVVBBMC9WaENvH6APoHz6q7himmJkARG7T0KJTY1%3A1742198198927; q_c1=7ced1b8210d042379d4a66614dfc335c|1742197341000|1742197341000'
}

# 2. 获取知乎热榜
def get_zhihu_hot():
    hot_url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=10"
    try:
        response = requests.get(hot_url, headers=headers, timeout=10)
        response.raise_for_status()  # 检查请求是否成功
        return response.json()
    except Exception as e:
        print(f"请求热榜失败: {e}")
        return None

# 3. 获取问题的第一个高赞回答
def get_top_answer(question_id):
    answer_url = f"https://www.zhihu.com/api/v4/questions/{question_id}/answers?limit=1&sort_by=vote_num"
    try:
        response = requests.get(answer_url, headers=headers, timeout=10)
        answer_data = response.json()
        if answer_data.get('data'):
            content = answer_data['data'][0]['content']
            soup = BeautifulSoup(content, 'html.parser')
            return soup.get_text().strip()[:200] + "..."  # 截取前200字
        return "暂无回答"
    except Exception as e:
        print(f"获取回答失败（问题ID: {question_id}）: {e}")
        return "获取失败"

# 4. 保存结果
def save_results(results):
    with open('zhihu_hot_answers.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    print("开始爬取知乎热榜...")
    hot_data = get_zhihu_hot()
    if not hot_data:
        print("热榜数据获取失败，请检查Cookie或网络！")
        exit()

    results = []
    for item in hot_data['data'][:10]:  # 只处理前10条
        question_title = item['target'].get('title', '无标题')
        question_id = item['target']['id']
        print(f"正在处理: {question_title}...")
        
        answer = get_top_answer(question_id)
        results.append({
            '排名': hot_data['data'].index(item) + 1,
            '问题': question_title,
            '回答摘要': answer
        })
        time.sleep(2)  # 避免请求过快被封

    save_results(results)
    print("爬取完成！结果已保存到 zhihu_hot_answers.json")