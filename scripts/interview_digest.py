#!/usr/bin/env python3
"""
教师考编结构化面试考情收集主脚本
每天自动收集各地教师招聘结构化面试信息，生成AI分析简报
"""

import os
import sys
import json
import pytz
from datetime import datetime
from pathlib import Path

# 添加脚本目录到 Python 路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from scrapers import GovSiteScraper
from analyzers import InterviewAnalyzer


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
    print("=" * 60)
    print("🎓 教师考编结构化面试考情收集")
    print("=" * 60)

    # 1. 加载配置
    config_path = SCRIPT_DIR / 'config.json'
    print(f"\n📄 加载配置文件: {config_path}")
    config = load_config(str(config_path))
    print(f"✅ 配置加载成功")
    print(f"  - 目标地区: {', '.join(config['target_regions'])}")
    print(f"  - AI 模型: {config['ai_config']['model']}")

    # 2. 初始化爬虫
    print(f"\n📡 初始化数据收集模块...")
    gov_scraper = GovSiteScraper(config)

    # 3. 抓取数据
    print(f"\n" + "=" * 60)
    print("开始抓取数据")
    print("=" * 60)

    all_announcements = []

    # 抓取教育局官网
    for region in config['target_regions']:
        try:
            announcements = gov_scraper.scrape(
                region=region,
                max_days=config['filters']['max_age_days']
            )
            all_announcements.extend(announcements)
        except Exception as e:
            print(f"❌ 抓取 {region} 失败: {e}")
            continue

    print(f"\n📊 数据抓取完成:")
    print(f"  - 总计: {len(all_announcements)} 条公告")

    # 4. 初始化 AI 分析器
    print(f"\n🤖 初始化 AI 分析器...")
    analyzer = InterviewAnalyzer(
        api_key=os.environ['ANTHROPIC_API_KEY'],
        base_url=os.environ.get('ANTHROPIC_BASE_URL')
    )

    # 5. 生成简报
    print(f"\n" + "=" * 60)
    print("生成 AI 简报")
    print("=" * 60)

    today = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d')
    questions = []  # 暂时没有真题来源，后续可扩展

    digest = analyzer.generate_interview_digest(
        announcements=all_announcements,
        questions=questions,
        today=today
    )

    # 6. 保存简报
    print(f"\n" + "=" * 60)
    print("保存简报文件")
    print("=" * 60)

    digests_dir = SCRIPT_DIR / config['output']['digests_dir']
    digests_dir.mkdir(exist_ok=True)

    digest_file = digests_dir / f"interview-digest-{today}.md"

    with open(digest_file, 'w', encoding='utf-8') as f:
        f.write(digest)

    print(f"✅ 简报已保存: {digest_file}")
    print(f"   文件大小: {len(digest)} 字符")

    # 7. 保存面试时间表
    schedule_file = SCRIPT_DIR.parent / 'data' / 'exam_schedule.json'
    save_interview_schedule(all_announcements, str(schedule_file))
    print(f"✅ 面试时间表已保存: {schedule_file}")

    # 8. 输出结果到 GitHub Actions
    if 'GITHUB_OUTPUT' in os.environ:
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            f.write(f"digest_file={digest_file}\n")
            f.write(f"total_announcements={len(all_announcements)}\n")

    # 9. 设置环境变量供推送脚本使用
    digest_file_env = SCRIPT_DIR.parent / 'digest_file.txt'
    with open(digest_file_env, 'w') as f:
        f.write(str(digest_file))

    print(f"\n" + "=" * 60)
    print("✅ 执行完成！")
    print("=" * 60)
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
