from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import random

# 配置参数
USERNAME = "18811700012"  # 替换为你的知乎账号
PASSWORD = "Luowang970128!"  # 替换为你的知乎密码
TOPIC_URL = httpswww.zhihu.comtopic19550901hot  # 示例：互联网话题热门
MIN_LIKES = 100  # 最小点赞数阈值，只给超过这个赞数的回答点赞
MAX_ACTIONS = 10  # 最大操作次数，防止过度操作

def setup_driver()
    设置浏览器驱动
    chrome_options = Options()
    # 以下选项可以根据需要取消注释
    # chrome_options.add_argument('--headless')  # 无头模式
    # chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # 添加用户代理，模拟真实浏览器
    chrome_options.add_argument('--user-agent=Mozilla5.0 (Windows NT 10.0; Win64; x64) AppleWebKit537.36 (KHTML, like Gecko) Chrome96.0.4664.110 Safari537.36')
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def login_zhihu(driver)
    登录知乎
    driver.get(httpswww.zhihu.comsignin)
    print(正在打开知乎登录页面...)
    
    try
        # 等待登录选项加载
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, .SignFlow-accountInput))
        )
        
        # 切换到密码登录
        password_login = driver.find_element(By.CSS_SELECTOR, .SignFlow-tab)
        password_login.click()
        
        # 输入用户名和密码
        username_input = driver.find_element(By.CSS_SELECTOR, .SignFlow-account input)
        password_input = driver.find_element(By.CSS_SELECTOR, .SignFlow-password input)
        
        username_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)
        
        # 点击登录按钮
        login_button = driver.find_element(By.CSS_SELECTOR, .SignFlow-submitButton)
        login_button.click()
        
        # 等待登录成功
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, .AppHeader-profile))
        )
        print(登录成功！)
        
    except Exception as e
        print(f登录过程出错 {e})
        # 可能需要处理验证码或其他登录问题
        input(请手动完成登录，然后按Enter继续...)

def like_top_answers(driver, topic_url)
    浏览话题并给高赞回答点赞
    driver.get(topic_url)
    print(f正在打开话题页面 {topic_url})
    
    # 等待页面加载
    time.sleep(3)
    
    # 滚动页面以加载更多内容
    for _ in range(5)
        driver.execute_script(window.scrollTo(0, document.body.scrollHeight);)
        time.sleep(2)
    
    # 获取所有回答卡片
    answer_cards = driver.find_elements(By.CSS_SELECTOR, .ContentItem.AnswerItem)
    print(f找到 {len(answer_cards)} 个回答)
    
    like_count = 0
    
    for card in answer_cards
        if like_count = MAX_ACTIONS
            print(f已达到最大操作次数 {MAX_ACTIONS}，停止点赞)
            break
            
        try
            # 获取点赞数
            vote_button = card.find_element(By.CSS_SELECTOR, button.VoteButton--up)
            vote_text = vote_button.text.strip()
            
            # 解析点赞数
            if 'K' in vote_text
                likes = int(float(vote_text.replace('K', ''))  1000)
            else
                likes = int(vote_text) if vote_text else 0
                
            # 检查是否已经点过赞
            is_voted = 'is-active' in vote_button.get_attribute('class')
            
            if likes = MIN_LIKES and not is_voted
                print(f发现高赞回答，点赞数 {likes})
                
                # 滚动到按钮可见
                driver.execute_script(arguments[0].scrollIntoView();, vote_button)
                time.sleep(1)
                
                # 点赞
                vote_button.click()
                print(已点赞)
                like_count += 1
                
                # 随机等待，模拟人类行为
                time.sleep(random.uniform(2, 5))
                
        except Exception as e
            print(f处理回答时出错 {e})
            continue

def main()
    driver = setup_driver()
    try
        login_zhihu(driver)
        like_top_answers(driver, TOPIC_URL)
        print(任务完成！)
    except Exception as e
        print(f程序执行出错 {e})
    finally
        # 等待一会再关闭浏览器
        time.sleep(5)
        driver.quit()

if __name__ == __main__
    main()