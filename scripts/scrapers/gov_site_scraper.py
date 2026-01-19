"""
教育局官网结构化面试公告爬虫
专门抓取各地教育局发布的结构化面试公告
"""

import os
import json
import hashlib
from typing import Dict, List
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper


class GovSiteScraper(BaseScraper):
    """教育局官网结构化面试公告爬虫"""

    # 结构化面试关键词
    INTERVIEW_KEYWORDS = [
        "结构化面试",
        "面试安排",
        "面试通知",
        "面试公告",
        "答辩",
        "面试时间"
    ]

    def __init__(self, config: Dict):
        super().__init__(config)
        self.filters = config.get('filters', {})
        self.sites_config = config.get('data_sources', {}).get('gov_websites', {}).get('sites', {})

    def scrape(self, region: str = None, max_days: int = 90) -> List[Dict]:
        """
        抓取指定地区的结构化面试公告

        Args:
            region: 地区名称（如"北京"），None 表示抓取所有地区
            max_days: 抓取最近多少天的公告

        Returns:
            公告列表
        """
        print(f"\n📍 开始抓取教育局官网公告...")
        results = []

        # 确定要抓取的地区
        regions = [region] if region else list(self.sites_config.keys())
        if not regions:
            print("  ⚠️  没有配置地区网站")
            return results

        for region_name in regions:
            if region_name not in self.sites_config:
                print(f"  ⚠️  跳过未配置的地区: {region_name}")
                continue

            site_url = self.sites_config[region_name]
            print(f"\n  📡 抓取 {region_name}: {site_url}")

            try:
                # 尝试抓取该地区的公告
                announcements = self._fetch_announcements(region_name, site_url, max_days)
                results.extend(announcements)
                print(f"  ✅ {region_name} 抓取到 {len(announcements)} 条公告")

            except Exception as e:
                print(f"  ❌ {region_name} 抓取失败: {e}")
                continue

        print(f"\n📊 总共抓取到 {len(results)} 条公告")
        return results

    def _fetch_announcements(self, region: str, site_url: str, max_days: int) -> List[Dict]:
        """
        抓取指定网站的公告列表

        Args:
            region: 地区名称
            site_url: 网站首页 URL
            max_days: 抓取最近多少天的公告

        Returns:
            公告列表
        """
        announcements = []

        try:
            # 抓取首页
            response = self.fetch(site_url)
            if not response:
                return announcements

            soup = BeautifulSoup(response.text, 'lxml')

            # 尝试查找公告列表
            # 这里需要根据不同网站的实际情况调整选择器
            # 目前使用通用的策略，实际使用时需要针对每个网站进行适配

            # 策略1: 查找包含"公告"、"通知"等关键词的链接
            news_links = soup.find_all('a', href=True)

            cutoff_date = datetime.now() - timedelta(days=max_days)

            for link in news_links:
                try:
                    title = link.get_text(strip=True)
                    href = link['href']

                    # 筛选包含面试关键词的公告
                    if not any(keyword in title for keyword in self.INTERVIEW_KEYWORDS):
                        continue

                    # 构建完整 URL
                    if href.startswith('/'):
                        base_url = '/'.join(site_url.split('/')[:3])
                        full_url = base_url + href
                    elif not href.startswith('http'):
                        full_url = site_url.rstrip('/') + '/' + href
                    else:
                        full_url = href

                    # 检查是否重复（使用 URL hash）
                    url_hash = hashlib.md5(full_url.encode()).hexdigest()

                    # 创建公告记录
                    announcement = {
                        'region': region,
                        'title': title,
                        'url': full_url,
                        'url_hash': url_hash,
                        'found_at': datetime.now().isoformat()
                    }

                    announcements.append(announcement)

                    # 限制数量，避免抓取过多
                    if len(announcements) >= 50:
                        break

                except Exception as e:
                    continue

        except Exception as e:
            print(f"  ❌ 抓取失败: {e}")

        return announcements

    def _fetch_announcement_detail(self, url: str) -> str:
        """
        抓取公告详情内容

        Args:
            url: 公告 URL

        Returns:
            公告文本内容
        """
        try:
            response = self.fetch(url)
            if not response:
                return ""

            soup = BeautifulSoup(response.text, 'lxml')

            # 尝试提取正文内容
            # 移除脚本和样式
            for script in soup(['script', 'style']):
                script.decompose()

            # 获取文本
            text = soup.get_text(separator='\n', strip=True)

            # 清理空行
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            cleaned_text = '\n'.join(lines)

            return cleaned_text[:10000]  # 限制长度

        except Exception as e:
            print(f"  ❌ 抓取详情失败: {e}")
            return ""
