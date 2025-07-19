import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

class ImageScraper:
    def __init__(self, save_dir="downloaded_images"):
        """初始化保存目录
        
        Args:
            save_dir: 图片保存的本地路径
        """
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)
    
    def fetch_images(self, url):
        """爬取指定URL页面中的图片
        
        Args:
            url: 需要爬取的网页地址
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            img_tags = soup.find_all('img')
            
            for img in img_tags:
                img_url = img.get('src')
                if not img_url:
                    continue
                
                # 处理相对路径
                full_url = urljoin(url, img_url)
                self._download_image(full_url)
                
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
    
    def _download_image(self, img_url):
        """下载单张图片到本地
        
        Args:
            img_url: 图片的完整URL
        """
        try:
            response = requests.get(img_url, timeout=10)
            response.raise_for_status()
            
            # 获取文件名
            filename = os.path.join(
                self.save_dir, 
                os.path.basename(img_url.split('?')[0])
            )
            
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"下载成功: {filename}")
            
        except requests.exceptions.RequestException as e:
            print(f"下载失败 {img_url}: {e}")

# 使用示例
import os
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    try:
        # 从环境变量获取URL，若未设置则使用默认值
        target_url = os.environ.get("TARGET_URL", "https://bing.ee123.net/")
        
        scraper = ImageScraper()
        logging.info(f"开始抓取图片，目标URL: {target_url}")
        scraper.fetch_images(target_url)
        logging.info("图片抓取完成")
    except Exception as e:
        logging.error(f"抓取过程中发生错误: {e}", exc_info=True)