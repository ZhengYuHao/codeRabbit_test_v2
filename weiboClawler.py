# ... existing code ...
import requests
from bs4 import BeautifulSoup
import logging
import os
from datetime import datetime

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WeiboHotScraper:
    """微博热榜爬虫类"""
    
    # 常量配置
    URL = 'https://s.weibo.com/top/summary'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    TIMEOUT = 10  # 请求超时时间
    OUTPUT_DIR = 'data'  # 输出目录
    OUTPUT_FILE = 'weibo_hot_titles.txt'

    def __init__(self):
        """初始化输出目录"""
        if not os.path.exists(self.OUTPUT_DIR):
            os.makedirs(self.OUTPUT_DIR)

    def fetch_hot_titles(self):
        """获取热榜标题"""
        try:
            response = requests.get(
                self.URL, 
                headers=self.HEADERS,
                timeout=self.TIMEOUT
            )
            response.raise_for_status()  # 检查HTTP错误
           
            return self._parse_html(response.text)
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {str(e)}")
            return []
        except Exception as e:
            print(f"未知错误: {str(e)}")
            return []

    def _parse_html(self, html_content):
        """解析HTML内容"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            print(soup)
            rows = soup.select('table tbody tr')
            titles = []
            
            for row in rows:
                title_element = row.select_one('td:nth-child(2) a')
                if title_element:
                    titles.append(title_element.text.strip())
            
            return titles
        except Exception as e:
            logger.error(f"HTML解析失败: {str(e)}")
            return []

    def save_to_file(self, titles):
        """保存数据到本地文件"""
        try:
            output_path = os.path.join(self.OUTPUT_DIR, self.OUTPUT_FILE)
            with open(output_path, 'w', encoding='utf-8') as file:
                for title in titles:
                    file.write(f"{title}\n")
            logger.info(f"成功保存 {len(titles)} 个标题到 {output_path}")
            return True
        except IOError as e:
            logger.error(f"文件写入失败: {str(e)}")
            return False

if __name__ == '__main__':
    scraper = WeiboHotScraper()
    hot_titles = scraper.fetch_hot_titles()
    print(hot_titles)
    if hot_titles:
        scraper.save_to_file(hot_titles)
    else:
        logger.warning("未获取到有效数据")
# ... existing code ...