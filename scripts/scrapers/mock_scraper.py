"""
模拟数据源
用于演示和测试系统功能
"""

from typing import Dict, List
from datetime import datetime, timedelta


class MockScraper:
    """模拟数据爬虫 - 提供示例数据"""

    # 模拟的招聘公告数据
    MOCK_ANNOUNCEMENTS = [
        {
            "region": "深圳",
            "title": "深圳市盐田区教育局2026年面向应届毕业生公开招聘教师公告",
            "url": "https://www.yantian.gov.cn/ytjyj/gkmlpt/content/12/12459/post_12459198.html",
            "found_at": datetime.now().isoformat(),
            "description": "招聘62名编制教师,包含结构化面试环节"
        },
        {
            "region": "苏州",
            "title": "苏州市吴江区教育系统2026年公开招聘事业编制教师公告",
            "url": "https://hrss.suzhou.gov.cn/jsszhrss/gsgg/202512/0f825d50ecab47a28e55993181b946b3.shtml",
            "found_at": (datetime.now() - timedelta(days=2)).isoformat(),
            "description": "招聘100名教师,面试形式为结构化面试"
        },
        {
            "region": "大连",
            "title": "大连市西岗区2026年教育系统自主招聘应届毕业生公告",
            "url": "https://lsdjyw.lnnu.edu.cn/news/view/aid/297794/tag/zpxx",
            "found_at": (datetime.now() - timedelta(days=5)).isoformat(),
            "description": "招聘16名教师,含结构化面试和试讲"
        },
        {
            "region": "深圳",
            "title": "深圳市公办中小学2025年12月面向2026年应届毕业生公开招聘",
            "url": "https://szeb.sz.gov.cn/home/xxgk/flzy/rsxx2/ryzp/content/post_12564466.html",
            "found_at": (datetime.now() - timedelta(days=7)).isoformat(),
            "description": "招聘888名教师,结构化面试安排另行通知"
        },
        {
            "region": "玉环",
            "title": "玉环市公开招聘2026年事业编制教师公告（浙师大专场）",
            "url": "http://www.yuhuan.gov.cn/art/2025/10/29/art_1229304968_4079109.html",
            "found_at": (datetime.now() - timedelta(days=10)).isoformat(),
            "description": "招聘30名教师,面试包含结构化问答"
        }
    ]

    def __init__(self, config: Dict):
        """
        初始化模拟爬虫

        Args:
            config: 配置字典
        """
        self.config = config
        self.enabled = config.get('data_sources', {}).get('mock', {}).get('enabled', False)

    def scrape(self, region: str = None, max_days: int = 90, max_workers: int = 1) -> List[Dict]:
        """
        获取模拟数据

        Args:
            region: 地区名称（暂不使用）
            max_days: 最大天数（暂不使用）
            max_workers: 并发数（暂不使用）

        Returns:
            公告列表
        """
        if not self.enabled:
            print("  ⚠️  模拟数据源未启用")
            return []

        print("\n📋 使用模拟数据源")
        print(f"  ✅ 提供 {len(self.MOCK_ANNOUNCEMENTS)} 条示例公告")

        # 返回所有模拟数据
        return self.MOCK_ANNOUNCEMENTS.copy()
