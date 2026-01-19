"""
结构化面试考情 AI 分析器
使用 Claude AI 生成结构化面试考情分析简报
"""

import os
import json
import anthropic
from typing import Dict, List
from datetime import datetime


class InterviewAnalyzer:
    """结构化面试考情分析器"""

    # 静态简报模板（空数据时使用）
    STATIC_DIGEST_TEMPLATE = """# 教师考编结构化面试考情简报 ({today})

> ⏰ 更新时间: {datetime}

---

## ⚠️ 今日数据状态

**当前状态**: 未收集到新的结构化面试相关信息

**数据统计**:
- 🔍 今日抓取公告: {announcement_count} 条
- 📝 收集到真题: {question_count} 道
- ✅ 数据抓取正常: {is_normal}

---

## 💡 说明

今日未检测到新的结构化面试相关公告。这可能是因为：
1. 各地教育局/学校暂未发布新的招聘公告
2. 公告发布时间不在我们的抓取周期内
3. 网站结构变化导致抓取失败（我们会及时修复）

---

## 🎓 常备考建议

虽然没有新的面试信息，但您可以：

### 持续备考
1. **关注结构化面试高频题型**:
   - 综合分析类（教育政策、现象分析）
   - 应急应变类（课堂突发事件处理）
   - 人际沟通类（家校沟通、同事协作）
   - 职业认知类（教师职业理解）

2. **积累教育热点素材**:
   - 双减政策、五育并举
   - 新课标、核心素养
   - 劳动教育、心理健康

3. **关注官方渠道**:
   - 各地教育局官网
   - 人社局招聘公告
   - 教育类招聘网站

---

## 🔗 资源推荐

- **公告来源**: 全国各地教育局、人社局官网
- **更新频率**: 每日自动抓取
- **下次更新**: 明日 7:00

---

*本简报由 AI 自动生成，如有疑问请查看原始公告链接*
"""

    # 主分析 Prompt
    STRUCTURED_INTERVIEW_ANALYSIS_PROMPT = """你是一位专业的教师招聘考试分析专家，专注于**结构化面试**考情分析。

## ⚠️ 核心原则（强制执行）

1. **绝对禁止编造信息**：如果没有数据，必须明确说明，不得虚构任何内容
2. **数据真实性**：只分析提供的原始数据，不得添加未经证实的信息
3. **空数据处理**：当数据为空时，明确说明"今日未收集到新信息"
4. **链接验证**：只使用提供的真实链接，不得编造链接

## 当前数据状态

- 公告数量：{announcement_count}
- 真题数量：{question_count}
- 数据状态：{data_status}

{empty_data_notice}

## 收集到的原始招聘和面试信息:
{content}

---

## 请生成以下结构化面试考情分析报告:

### 1. 🎯 即将到来的结构化面试（时间倒序）
**[紧急] 7天内面试**
- **[地区] XX学校/教育局**
  - 面试时间: YYYY-MM-DD HH:MM
  - 面试地点: XXX
  - 报名截止: YYYY-MM-DD
  - **快速准备建议**: 2-3条紧急备考建议
  - **公告链接**: 原始链接

**[近期] 30天内面试**
- 列出所有30天内的结构化面试安排
- 格式同上，突出关键时间节点

### 2. 📊 近期结构化面试考情汇总
- **面试地区分布**: 统计各地区面试数量
- **面试时间集中期**: 分析面试高峰期（如5月、6月）
- **面试形式趋势**: 纯结构化 / 结构化+试讲 / 结构化+说课的比例
- **热门题型**: 统计高频题型（综合分析、应急应变、人际沟通等）

### 3. 💎 结构化面试真题精选（5-8道）
从收集到的真题中筛选最具代表性的题目：
- **[地区] 题目类型**: 具体题目
  - **答题思路**: 200字左右的答题框架
  - **参考要点**: 3-4个关键得分点
  - **来源**: XX地区 202X年面试真题

### 4. 📈 考情趋势分析
- **面试难度变化**: 与往年相比的难度提升或降低
- **题型新趋势**: 是否出现新的题型或考察方向
- **地区特色**: 不同地区的面试特点（如某些地区偏重教育热点）
- **竞争激烈度**: 基于招聘人数和报名情况的竞争分析

### 5. 🎓 高频考点速查
| 考点类别 | 高频题目举例 | 出现频率 | 地区 |
|---------|-------------|----------|------|
| 综合分析类 | "如何看待双减政策？" | 高 | 全国 |
| 应急应变类 | "学生课堂冲突如何处理？" | 高 | 全国 |
| ... | ... | ... | ... |

### 6. 💡 备考策略建议
#### 按面试时间倒推的备考计划
- **面试前7天**: 重点突破、模拟练习
- **面试前1个月**: 系统复习、题库积累
- **面试前3个月**: 基础学习、框架搭建

#### 针对不同题型的备考技巧
- 综合分析类: **是什么-为什么-怎么做-升华**
- 应急应变类: **轻重缓急-多方协调-总结反思**
- 人际沟通类: **态度尊重-有效沟通-解决矛盾**

### 7. 🔗 重要资源链接
- **面试公告汇总**: 最新公告链接列表
- **真题资源**: 历年真题汇总链接
- **备考资料**: 推荐的教材和题库
- **学习社群**: 相关的备考群或论坛

### 8. ⏰ 下一步行动提醒
为考生提供明确的时间线：
- 近期报名截止（3天内）
- 近期面试提醒（7天内、30天内）
- 长期备考建议（3个月以上）

---

## 输出格式要求:
- 使用 Markdown 格式
- 重点突出**面试时间**信息（使用加粗和表情）
- 保留所有原始链接
- 总长度控制在 2500 字以内
- 使用表格、列表等结构化元素提升可读性
- **必须突出显示7天内即将到来的面试**

请直接输出分析报告，不需要额外说明。"""

    # 结构化信息提取 Prompt
    EXTRACT_INTERVIEW_INFO_PROMPT = """从以下教师招聘公告中提取**结构化面试**相关的关键信息：

公告文本:
{text}

请提取以下信息（以 JSON 格式返回）:
{{
    "region": "地区名称（省/市）",
    "organization": "招聘单位名称",
    "announcement_title": "公告标题",
    "announcement_url": "公告链接",
    "recruitment_count": 招聘人数（数字）,
    "registration_period": {{
        "start": "报名开始时间（YYYY-MM-DD）",
        "end": "报名截止时间（YYYY-MM-DD）"
    }},
    "written_exam_date": "笔试时间（YYYY-MM-DD，如无则null）",
    "structured_interview": {{
        "has_interview": true/false（是否包含结构化面试）,
        "interview_date": "面试日期（YYYY-MM-DD，如未确定则null）",
        "interview_time": "面试具体时间（如有）",
        "interview_location": "面试地点",
        "interview_format": "面试形式（如：纯结构化、结构化+试讲、结构化+说课）",
        "question_types": ["题型1", "题型2"],
        "interview_duration": "面试时长（如：15分钟）",
        "preparation_time": "备考时间（如：5分钟）"
    }},
    "special_requirements": "特殊要求或备注",
    "publish_date": "公告发布时间（YYYY-MM-DD）"
}}

注意事项：
1. 如果公告中没有明确提到"结构化面试"，则 has_interview 设为 false
2. 只提取明确的信息，不确定的字段设为 null
3. 面试形式需要根据公告描述准确判断（如"答辩"、"问答"通常指结构化面试）
4. 时间格式统一为 YYYY-MM-DD
5. 必须返回纯 JSON 格式，不要包含其他文字说明
"""

    def __init__(self, api_key: str, base_url: str = None):
        """
        初始化分析器

        Args:
            api_key: Anthropic API 密钥
            base_url: API 端点（可选）
        """
        self.client = anthropic.Anthropic(api_key=api_key, base_url=base_url)
        self.ai_config = {
            "model": "glm-4-plus",
            "max_tokens": 8192,
            "temperature": 0.3
        }

    def generate_interview_digest(
        self,
        announcements: List[Dict],
        questions: List[Dict],
        today: str
    ) -> str:
        """
        生成结构化面试考情简报

        Args:
            announcements: 公告列表
            questions: 真题列表
            today: 今天的日期

        Returns:
            生成的简报内容
        """
        # 🔒 数据验证：检查是否为空数据
        data_status = self._validate_data_before_analysis(announcements, questions)

        # 如果没有数据，使用静态模板
        if not data_status["has_data"]:
            print(f"\n⚠️  数据状态检查:")
            print(f"  - 公告数量: {len(announcements)}")
            print(f"  - 真题数量: {len(questions)}")
            print(f"  - 数据状态: 无有效数据")
            print(f"  - 使用静态简报模板")
            return self._generate_static_digest(
                announcements,
                questions,
                today,
                data_status["is_scraping_normal"]
            )

        # 准备内容
        content = self._prepare_content(announcements, questions)

        print(f"\n🤖 调用 Claude API 生成简报...")
        print(f"  - 公告数量: {len(announcements)}")
        print(f"  - 真题数量: {len(questions)}")
        print(f"  - 数据状态: 有有效数据")

        try:
            # 准备空数据提示
            empty_data_notice = ""
            if len(announcements) == 0:
                empty_data_notice = "**重要提醒**: 今日未收集到新的公告信息，请明确说明此情况，不要编造任何内容。"

            # 调用 Claude API
            response = self.client.messages.create(
                model=self.ai_config["model"],
                max_tokens=self.ai_config["max_tokens"],
                temperature=self.ai_config["temperature"],
                messages=[{
                    "role": "user",
                    "content": self.STRUCTURED_INTERVIEW_ANALYSIS_PROMPT.format(
                        today=today,
                        content=content,
                        announcement_count=len(announcements),
                        question_count=len(questions),
                        data_status="有数据" if len(announcements) > 0 else "无数据",
                        empty_data_notice=empty_data_notice
                    )
                }]
            )

            digest = response.content[0].text
            print(f"✅ 简报生成成功，长度: {len(digest)} 字符")
            return digest

        except Exception as e:
            print(f"❌ 生成简报失败: {e}")
            return self._generate_static_digest(
                announcements,
                questions,
                today,
                is_scraping_normal=False
            )

    def extract_interview_info(self, announcement_text: str, url: str) -> Dict:
        """
        从公告中提取结构化面试信息

        Args:
            announcement_text: 公告文本
            url: 公告 URL

        Returns:
            提取的结构化信息
        """
        try:
            prompt = self.EXTRACT_INTERVIEW_INFO_PROMPT.format(
                text=announcement_text[:5000]  # 限制长度
            )

            response = self.client.messages.create(
                model=self.ai_config["model"],
                max_tokens=2048,
                temperature=0.2,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # 解析 JSON 结果
            result_text = response.content[0].text
            result = json.loads(result_text)
            result['announcement_url'] = url

            return result

        except Exception as e:
            print(f"  ⚠️  提取信息失败: {e}")
            return {
                "has_interview": False,
                "error": str(e)
            }

    def _prepare_content(self, announcements: List[Dict], questions: List[Dict]) -> str:
        """准备发送给 AI 的内容"""
        content_parts = []

        # 添加公告信息
        if announcements:
            content_parts.append("## 招聘公告信息\n")
            for i, ann in enumerate(announcements[:20], 1):  # 限制数量
                content_parts.append(f"{i}. **{ann.get('title', '未知标题')}**")
                content_parts.append(f"   - 地区: {ann.get('region', '未知')}")
                content_parts.append(f"   - 链接: {ann.get('url', '无')}")
                if 'found_at' in ann:
                    content_parts.append(f"   - 发现时间: {ann['found_at']}")
                content_parts.append("")

        # 添加真题信息
        if questions:
            content_parts.append("\n## 面试真题信息\n")
            for i, q in enumerate(questions[:10], 1):
                content_parts.append(f"{i}. {q.get('question', '未知题目')}")

        return '\n'.join(content_parts)

    def _validate_data_before_analysis(
        self,
        announcements: List[Dict],
        questions: List[Dict]
    ) -> Dict:
        """
        验证数据是否足够进行分析

        Returns:
            包含验证结果的字典:
            - has_data: 是否有足够的数据
            - is_scraping_normal: 抓取是否正常工作
        """
        # 判断是否有数据
        has_announcements = len(announcements) > 0
        has_questions = len(questions) > 0

        # 如果有公告或真题，认为有数据
        has_data = has_announcements or has_questions

        # 判断抓取是否正常（这里简单判断，实际可以更复杂）
        # 如果完全没有数据，可能是抓取失败，也可能是真的没有新公告
        is_scraping_normal = True  # 默认认为正常

        return {
            "has_data": has_data,
            "is_scraping_normal": is_scraping_normal
        }

    def _generate_static_digest(
        self,
        announcements: List[Dict],
        questions: List[Dict],
        today: str,
        is_scraping_normal: bool = True
    ) -> str:
        """
        生成静态简报（空数据时使用）

        Args:
            announcements: 公告列表（可能为空）
            questions: 真题列表（可能为空）
            today: 今天的日期
            is_scraping_normal: 抓取是否正常

        Returns:
            静态简报内容
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return self.STATIC_DIGEST_TEMPLATE.format(
            today=today,
            datetime=now,
            announcement_count=len(announcements),
            question_count=len(questions),
            is_normal="是" if is_scraping_normal else "否（可能存在问题）"
        )

    def _generate_fallback_digest(self, announcements: List[Dict], today: str) -> str:
        """生成简化的备用简报（保留用于向后兼容）"""
        lines = [
            f"# 教师考编结构化面试考情简报 ({today})",
            "",
            "⚠️ **注意**: AI 生成失败，以下为简化版本",
            "",
            "## 📊 今日数据统计",
            f"- 抓取到 {len(announcements)} 条相关公告",
            "",
            "## 📋 公告列表",
            ""
        ]

        for i, ann in enumerate(announcements[:20], 1):
            lines.append(f"{i}. **{ann.get('title', '未知')}**")
            lines.append(f"   - 地区: {ann.get('region', '未知')}")
            lines.append(f"   - 链接: {ann.get('url', '无')}")
            lines.append("")

        return '\n'.join(lines)
