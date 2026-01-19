#!/usr/bin/env python3
"""
教师考编结构化面试考情收集主脚本
每天自动收集各地教师招聘结构化面试信息，生成AI分析简报
优化版本：添加时间统计和进度显示
"""

import os
import sys
import json
import pytz
import time
from datetime import datetime
from pathlib import Path

# 添加脚本目录到 Python 路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from scrapers import GovSiteScraper, MockScraper, WechatScraper
from analyzers import InterviewAnalyzer
from utils import DataValidator


class Timer:
    """简单的计时器"""
    def __init__(self):
        self.start_time = None
        self.stage_start = None

    def start(self):
        """开始计时"""
        self.start_time = time.time()
        self.stage_start = time.time()

    def stage(self, stage_name: str):
        """记录阶段时间"""
        if self.stage_start:
            elapsed = time.time() - self.stage_start
            print(f"  ⏱️  {stage_name} 耗时: {elapsed:.1f} 秒")
        self.stage_start = time.time()

    def total(self) -> float:
        """总耗时"""
        if self.start_time:
            return time.time() - self.start_time
        return 0


def load_config(config_path: str) -> dict:
    """加载配置文件"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_interview_schedule(announcements: list, output_file: str):
    """保存面试时间表到 JSON 文件"""
    schedule_data = {
        'updated_at': datetime.now(pytz.timezone('Asia/Shanghai')).isoformat(),
        'total_count': len(announcements),
        'announcements': announcements
    }

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(schedule_data, f, ensure_ascii=False, indent=2)


def main():
    """主执行流程"""
    timer = Timer()
    timer.start()

    print("=" * 60)
    print("🎓 教师考编结构化面试考情收集")
    print("=" * 60)

    # 1. 加载配置
    print(f"\n📄 加载配置...")
    config_path = SCRIPT_DIR / 'config.json'
    config = load_config(str(config_path))
    print(f"✅ 配置加载成功")
    print(f"  - 目标地区: {', '.join(config['target_regions'])}")
    print(f"  - AI 模型: {config['ai_config']['model']}")

    # 2. 初始化爬虫
    print(f"\n📡 初始化数据收集模块...")

    # 按优先级选择数据源
    wechat_enabled = config.get('data_sources', {}).get('wechat', {}).get('enabled', False)
    mock_enabled = config.get('data_sources', {}).get('mock', {}).get('enabled', False)

    scraper = None
    scraper_type = ""

    if wechat_enabled:
        print("  ✅ 微信数据源已启用（搜狗微信搜索）")
        scraper = WechatScraper(config)
        scraper_type = "wechat"
    elif mock_enabled:
        print("  ✅ 模拟数据源已启用")
        scraper = MockScraper(config)
        scraper_type = "mock"
    else:
        print("  ✅ 使用政府网站数据源")
        scraper = GovSiteScraper(config)
        scraper_type = "gov"

    timer.stage("初始化")

    # 3. 抓取数据
    print(f"\n" + "=" * 60)
    if scraper_type == "wechat":
        print("🚀 使用搜狗微信搜索")
    elif scraper_type == "mock":
        print("🚀 使用模拟数据源")
    else:
        print("🚀 开始抓取数据（并发模式）")
    print("=" * 60)

    all_announcements = []

    try:
        announcements = scraper.scrape(
            max_days=config['filters']['max_age_days'],
            max_workers=5  # 5个并发线程
        )
        all_announcements.extend(announcements)
    except Exception as e:
        print(f"❌ 数据抓取失败: {e}")

    timer.stage("数据抓取")

    print(f"\n📊 数据抓取完成:")
    print(f"  - 总计: {len(all_announcements)} 条公告")

    # 4.1 数据验证（新增）
    print(f"\n" + "=" * 60)
    print("🔍 数据验证")
    print("=" * 60)

    validator = DataValidator(timeout=5)
    validation_result = validator.validate_announcements(
        all_announcements,
        check_links=False  # 不检查链接可访问性（加快速度）
    )

    print(f"✅ 数据验证完成:")
    print(f"  - 总计: {validation_result['total']} 条")
    print(f"  - 有效: {validation_result['valid']} 条")
    print(f"  - 无效: {validation_result['invalid']} 条")
    print(f"  - 验证率: {validation_result['validation_rate']:.1f}%")

    if validation_result['errors']:
        print(f"\n⚠️  发现 {len(validation_result['errors'])} 个数据问题:")
        for error in validation_result['errors'][:5]:  # 只显示前5个
            print(f"  - [{error['index']}] {error['title']}: {', '.join(error['errors'])}")

    timer.stage("数据验证")

    # 4. 初始化 AI 分析器
    print(f"\n🤖 初始化 AI 分析器...")
    analyzer = InterviewAnalyzer(
        api_key=os.environ['ANTHROPIC_API_KEY'],
        base_url=os.environ.get('ANTHROPIC_BASE_URL')
    )

    # 5. 生成简报
    print(f"\n" + "=" * 60)
    print("📝 生成 AI 简报")
    print("=" * 60)

    today = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d')
    questions = []  # 暂时没有真题来源，后续可扩展

    digest = analyzer.generate_interview_digest(
        announcements=all_announcements,
        questions=questions,
        today=today
    )

    timer.stage("AI 分析")

    # 6. 保存简报
    print(f"\n" + "=" * 60)
    print("💾 保存简报文件")
    print("=" * 60)

    # 使用项目根目录的 digests 文件夹
    project_root = SCRIPT_DIR.parent
    digests_dir = project_root / config['output']['digests_dir']
    digests_dir.mkdir(exist_ok=True)

    digest_file = digests_dir / f"interview-digest-{today}.md"

    with open(digest_file, 'w', encoding='utf-8') as f:
        f.write(digest)

    print(f"✅ 简报已保存: {digest_file}")
    print(f"   文件大小: {len(digest)} 字符")

    # 7. 保存面试时间表
    schedule_file = project_root / 'data' / 'exam_schedule.json'
    save_interview_schedule(all_announcements, str(schedule_file))
    print(f"✅ 面试时间表已保存: {schedule_file}")

    # 8. 输出结果到 GitHub Actions
    if 'GITHUB_OUTPUT' in os.environ:
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            f.write(f"digest_file={digest_file}\n")
            f.write(f"total_announcements={len(all_announcements)}\n")

    # 9. 设置环境变量供推送脚本使用
    digest_file_env = project_root / 'digest_file.txt'
    with open(digest_file_env, 'w') as f:
        f.write(str(digest_file))

    timer.stage("保存文件")

    print(f"\n" + "=" * 60)
    print("✅ 执行完成！")
    print("=" * 60)
    print(f"\n⏱️  总耗时: {timer.total():.1f} 秒")
    print(f"\n📄 简报文件: {digest_file}")
    print(f"📅 时间表文件: {schedule_file}")

    return str(digest_file)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 执行失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
