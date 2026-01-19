"""
基础爬虫类 - 教师考编结构化面试考情收集
提供通用的爬虫功能：请求发送、错误处理、重试机制
"""

import requests
import time
import random
from typing import Optional, Dict, List
from abc import ABC, abstractmethod


class BaseScraper(ABC):
    """爬虫基类"""

    # User-Agent 池
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    ]

    def __init__(self, config: Dict):
        """
        初始化爬虫

        Args:
            config: 配置字典
        """
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self._get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })

    def _get_random_user_agent(self) -> str:
        """获取随机 User-Agent"""
        return random.choice(self.USER_AGENTS)

    def fetch(self, url: str, timeout: int = 30) -> Optional[requests.Response]:
        """
        通用请求方法，带重试机制

        Args:
            url: 请求的 URL
            timeout: 超时时间（秒）

        Returns:
            Response 对象，失败返回 None
        """
        max_retries = 3
        backoff_factor = 2

        for attempt in range(max_retries):
            try:
                # 随机延迟 2-5 秒，避免请求过快被封
                if attempt > 0:
                    delay = random.uniform(2, 5)
                    print(f"  [重试 {attempt}/{max_retries}] 等待 {delay:.1f} 秒...")
                    time.sleep(delay)

                response = self.session.get(url, timeout=timeout)
                response.raise_for_status()

                # 成功后随机延迟，避免连续请求
                time.sleep(random.uniform(2, 5))

                return response

            except requests.exceptions.Timeout:
                print(f"  ⚠️  请求超时: {url}")
                if attempt == max_retries - 1:
                    return None

            except requests.exceptions.HTTPError as e:
                print(f"  ⚠️  HTTP 错误 {e.response.status_code}: {url}")
                if e.response.status_code in [403, 429]:
                    # 被封禁或请求过多，增加延迟
                    time.sleep(backoff_factor ** attempt * 5)
                if attempt == max_retries - 1:
                    return None

            except Exception as e:
                print(f"  ⚠️  请求失败: {e}")
                if attempt == max_retries - 1:
                    return None

        return None

    @abstractmethod
    def scrape(self, **kwargs) -> List[Dict]:
        """
        抓取数据的抽象方法，子类必须实现

        Returns:
            数据列表
        """
        pass
