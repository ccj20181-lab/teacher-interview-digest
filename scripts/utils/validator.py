"""
数据验证工具
用于验证公告和真题数据的真实性
"""

import requests
from typing import Dict, List, Optional
from urllib.parse import urlparse
import re


class DataValidator:
    """数据验证器"""

    def __init__(self, timeout: int = 10):
        """
        初始化验证器

        Args:
            timeout: 请求超时时间（秒）
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })

    def validate_announcement(self, announcement: Dict) -> Dict:
        """
        验证单个公告数据

        Args:
            announcement: 公告数据字典

        Returns:
            验证结果字典:
            - is_valid: 是否有效
            - link_accessible: 链接是否可访问
            - errors: 错误列表
        """
        errors = []
        is_valid = True
        link_accessible = False

        # 1. 检查必需字段
        if 'title' not in announcement or not announcement['title']:
            errors.append("缺少标题")
            is_valid = False

        if 'url' not in announcement or not announcement['url']:
            errors.append("缺少链接")
            is_valid = False
        else:
            # 2. 验证链接格式
            try:
                result = urlparse(announcement['url'])
                if not all([result.scheme, result.netloc]):
                    errors.append(f"链接格式无效: {announcement['url']}")
                    is_valid = False
                else:
                    # 3. 尝试访问链接（可选，因为可能较慢）
                    link_accessible = self._check_link_accessibility(announcement['url'])
            except Exception as e:
                errors.append(f"链接解析失败: {e}")
                is_valid = False

        if 'region' not in announcement or not announcement['region']:
            errors.append("缺少地区信息")
            # 地区信息不是必需的，所以只警告

        return {
            "is_valid": is_valid,
            "link_accessible": link_accessible,
            "errors": errors
        }

    def validate_announcements(
        self,
        announcements: List[Dict],
        check_links: bool = False
    ) -> Dict:
        """
        批量验证公告数据

        Args:
            announcements: 公告列表
            check_links: 是否检查链接可访问性（较慢）

        Returns:
            验证统计结果
        """
        if not announcements:
            return {
                "total": 0,
                "valid": 0,
                "invalid": 0,
                "link_accessible_count": 0,
                "validation_rate": 0.0,
                "errors": []
            }

        valid_count = 0
        invalid_count = 0
        link_accessible_count = 0
        all_errors = []

        for i, ann in enumerate(announcements):
            result = self.validate_announcement(ann)

            if result["is_valid"]:
                valid_count += 1
            else:
                invalid_count += 1

            if result["link_accessible"]:
                link_accessible_count += 1

            if result["errors"]:
                all_errors.append({
                    "index": i,
                    "title": ann.get('title', '未知'),
                    "errors": result["errors"]
                })

        total = len(announcements)
        validation_rate = (valid_count / total * 100) if total > 0 else 0.0

        return {
            "total": total,
            "valid": valid_count,
            "invalid": invalid_count,
            "link_accessible_count": link_accessible_count,
            "validation_rate": validation_rate,
            "errors": all_errors[:10]  # 只返回前10个错误
        }

    def _check_link_accessibility(self, url: str) -> bool:
        """
        检查链接是否可访问

        Args:
            url: 链接地址

        Returns:
            是否可访问
        """
        try:
            response = self.session.head(
                url,
                timeout=self.timeout,
                allow_redirects=True
            )
            # 认为状态码 < 400 是可访问的
            return response.status_code < 400
        except Exception:
            # 如果 HEAD 请求失败，尝试 GET（有些服务器不支持 HEAD）
            try:
                response = self.session.get(
                    url,
                    timeout=self.timeout,
                    allow_redirects=True,
                    stream=True  # 不下载完整内容
                )
                # 只读取前1KB来判断
                next(iter(response.iter_content(1024)), None)
                return response.status_code < 400
            except Exception:
                return False

    def sanitize_content(self, content: str, max_length: int = 10000) -> str:
        """
        清理和截断内容

        Args:
            content: 原始内容
            max_length: 最大长度

        Returns:
            清理后的内容
        """
        if not content:
            return ""

        # 移除多余的空白字符
        content = re.sub(r'\s+', ' ', content)

        # 截断
        if len(content) > max_length:
            content = content[:max_length] + "..."

        return content.strip()

    def extract_date_from_text(self, text: str) -> Optional[str]:
        """
        从文本中提取日期

        Args:
            text: 文本内容

        Returns:
            提取到的日期字符串（YYYY-MM-DD格式），如果未找到则返回None
        """
        # 匹配常见日期格式
        date_patterns = [
            r'(\d{4})-(\d{1,2})-(\d{1,2})',  # 2024-01-15
            r'(\d{4})年(\d{1,2})月(\d{1,2})日',  # 2024年1月15日
            r'(\d{4})/(\d{1,2})/(\d{1,2})',  # 2024/01/15
        ]

        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                year, month, day = match.groups()
                # 格式化为 YYYY-MM-DD
                return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

        return None
