"""
微信公众号文章爬虫
通过搜狗微信搜索抓取公众号文章
"""

import hashlib
import requests
from typing import Dict, List
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper


class WechatScraper(BaseScraper):
    """微信公众号文章爬虫"""

    # 搜狗微信搜索 URL
    SOGOU_WEIXIN_SEARCH = "https://weixin.sogou.com/weixin"

    # 搜索关键词
    SEARCH_KEYWORDS = [
        "教师招聘",
        "结构化面试",
        "教师编制",
        "面试通知",
        "招聘公告"
    ]

    def __init__(self, config: Dict):
        """
        初始化微信爬虫

        Args:
            config: 配置字典
        """
        self.config = config
        self.enabled = config.get('data_sources', {}).get('wechat', {}).get('enabled', False)
        self.max_results = config.get('data_sources', {}).get('wechat', {}).get('max_results', 20)

    def scrape(self, region: str = None, max_days: int = 90, max_workers: int = 1) -> List[Dict]:
        """
        通过搜狗微信搜索抓取文章

        Args:
            region: 地区名称（可用于限定搜索范围）
            max_days: 最大天数（暂不使用）
            max_workers: 并发数（暂不使用）

        Returns:
            文章列表
        """
        if not self.enabled:
            print("  ⚠️  微信数据源未启用")
            return []

        print("\n📱 使用搜狗微信搜索")
        all_articles = []

        try:
            # 对每个关键词进行搜索
            for keyword in self.SEARCH_KEYWORDS:
                articles = self._search_weixin(keyword, region)
                all_articles.extend(articles)

                # 限制总数量
                if len(all_articles) >= self.max_results:
                    break

            print(f"  ✅ 找到 {len(all_articles)} 篇相关文章")

        except Exception as e:
            print(f"  ❌ 微信搜索失败: {e}")

        return all_articles

    def _search_weixin(self, keyword: str, region: str = None) -> List[Dict]:
        """
        搜狗微信搜索

        Args:
            keyword: 搜索关键词
            region: 地区限定

        Returns:
            文章列表
        """
        articles = []

        try:
            # 构建搜索查询
            if region:
                query = f"{region} {keyword}"
            else:
                query = keyword

            params = {
                'type': 2,  # 2 表示搜索文章
                'query': query,
                'ie': 'utf8'
            }

            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }

            response = requests.get(
                self.SOGOU_WEIXIN_SEARCH,
                params=params,
                headers=headers,
                timeout=10
            )

            if response.status_code != 200:
                return articles

            soup = BeautifulSoup(response.text, 'html.parser')

            # 查找文章结果
            results = soup.find_all('div', class_='news-box')

            for item in results:
                try:
                    # 提取标题
                    title_elem = item.find('h3')
                    if not title_elem:
                        continue

                    title = title_elem.get_text(strip=True)

                    # 提取链接
                    link_elem = item.find('a')
                    if not link_elem:
                        continue

                    # 搜狗的链接是微信文章的跳转链接
                    sogou_url = link_elem.get('href', '')

                    # 提取公众号名称
                    account_elem = item.find('a', class_='account')
                    account = account_elem.get_text(strip=True) if account_elem else "未知公众号"

                    # 提取摘要
                    summary_elem = item.find('p', class_='txt-info')
                    summary = summary_elem.get_text(strip=True) if summary_elem else ""

                    # 提取时间
                    time_elem = item.find('span', class_='s2')
                    publish_time = time_elem.get_text(strip=True) if time_elem else ""

                    # 生成唯一 ID
                    url_hash = hashlib.md5(sogou_url.encode()).hexdigest()

                    article = {
                        'region': region or '全国',
                        'title': title,
                        'url': sogou_url,  # 使用搜狗链接
                        'url_hash': url_hash,
                        'account': account,
                        'summary': summary[:200],  # 限制摘要长度
                        'publish_time': publish_time,
                        'found_at': datetime.now().isoformat(),
                        'source': 'wechat'
                    }

                    articles.append(article)

                except Exception as e:
                    continue

        except Exception as e:
            print(f"  ❌ 搜索失败: {e}")

        return articles
