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

    def fetch(self, url: str, timeout: int = 30, delay: bool = True) -> Optional[requests.Response]:
        """
        通用请求方法，带重试机制（优化版本）

        Args:
            url: 请求的 URL
            timeout: 超时时间（秒）
            delay: 是否添加请求延迟（并发模式下可关闭）

        Returns:
            Response 对象，失败返回 None
        """
        max_retries = 2  # 减少重试次数，从3改为2
        backoff_factor = 1.5  # 减少退避因子，从2改为1.5

        for attempt in range(max_retries):
            try:
                # 只在重试时添加延迟
                if attempt > 0 and delay:
                    wait_time = backoff_factor ** attempt
                    time.sleep(wait_time)

                response = self.session.get(url, timeout=timeout)
                response.raise_for_status()

                # 成功后根据是否并发模式决定延迟时间
                if delay:
                    time.sleep(random.uniform(0.5, 1.5))  # 从2-5秒减少到0.5-1.5秒

                return response

            except requests.exceptions.Timeout:
                # 超时错误不打印，避免刷屏
                if attempt == max_retries - 1:
                    return None

            except requests.exceptions.HTTPError as e:
                # 只在特定错误时打印
                if e.response.status_code in [403, 429]:
                    time.sleep(backoff_factor ** attempt * 3)
                if attempt == max_retries - 1:
                    return None

            except Exception:
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
