#!/usr/bin/env python3
"""
PushPlus 微信推送通知 - 教师考编结构化面试版
将结构化面试考情简报推送到微信
"""

import os
import sys
import requests
from datetime import datetime
from pathlib import Path
import pytz
import re


def format_markdown_to_html(markdown_text: str) -> str:
    """
    将Markdown格式转换为美观的HTML格式

    Args:
        markdown_text: Markdown格式的文本

    Returns:
        HTML格式的文本
    """
    lines = markdown_text.split('\n')
    html_lines = []
    in_list = False

    for line in lines:
        # 跳过空行
        if not line.strip():
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append('<br>')
            continue

        # 处理标题（# ## ### 等）
        if line.startswith('#'):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            level = len(re.match(r'^#+', line).group())
            text = line.lstrip('#').strip()
            if level == 1:
                html_lines.append(f'<h1 style="color: #7c3aed; font-size: 24px; font-weight: bold; margin: 20px 0 10px;">{text}</h1>')
            elif level == 2:
                html_lines.append(f'<h2 style="color: #5b21b6; font-size: 20px; font-weight: bold; margin: 18px 0 8px;">{text}</h2>')
            elif level == 3:
                html_lines.append(f'<h3 style="color: #4c1d95; font-size: 18px; font-weight: bold; margin: 15px 0 6px;">{text}</h3>')
            else:
                html_lines.append(f'<h4 style="font-size: 16px; font-weight: bold; margin: 12px 0 5px;">{text}</h4>')

        # 处理表格
        elif '|' in line and line.strip().startswith('|'):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            # 简单处理表格（保留 Markdown 格式）
            html_lines.append(f'<p style="font-family: monospace; font-size: 12px; margin: 5px 0;">{line}</p>')

        # 处理列表项（- 或 * 开头）
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            if not in_list:
                html_lines.append('<ul style="margin: 10px 0; padding-left: 20px;">')
                in_list = True
            text = line.strip().lstrip('-*').strip()
            # 处理加粗
            text = re.sub(r'\*\*(.*?)\*\*', r'<b style="color: #7c3aed;">\1</b>', text)
            # 简化处理：移除链接，保留文本
            text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
            html_lines.append(f'<li style="margin: 8px 0; line-height: 1.6;">{text}</li>')

        # 处理普通段落
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False

            text = line.strip()
            # 处理加粗
            text = re.sub(r'\*\*(.*?)\*\*', r'<b style="color: #7c3aed;">\1</b>', text)
            # 简化处理：移除链接，保留文本
            text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
            # 处理分隔线
            if text.strip() == '---':
                html_lines.append('<hr style="border: none; border-top: 1px solid #e0e0e0; margin: 20px 0;">')
            else:
                html_lines.append(f'<p style="margin: 10px 0; line-height: 1.8;">{text}</p>')

    if in_list:
        html_lines.append('</ul>')

    return '\n'.join(html_lines)


def send_pushplus_notification(token: str, title: str, content: str):
    """
    发送 PushPlus 通知（完整内容版）

    Args:
        token: PushPlus Token
        title: 消息标题
        content: 完整的简报内容（Markdown格式）
    """
    # 将Markdown转换为美观的HTML
    html_content = format_markdown_to_html(content)

    # 构建完整消息（精美排版）
    full_content = f"""
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; line-height: 1.8; color: #333;">
{html_content}

<hr style="border: none; border-top: 1px solid #e0e0e0; margin: 30px 0;">

<p style="text-align: center; color: #999; font-size: 12px; line-height: 1.6;">
  🎓 教师考编结构化面试考情简报<br>
  🤖 由 Claude AI + 智谱 GLM-4 自动生成<br>
  ⏰ 生成时间: {datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')}
</p>
</div>
"""

    # PushPlus API
    url = f"http://www.pushplus.plus/send/{token}"

    payload = {
        "title": title,
        "content": full_content,
        "template": "html"  # 使用 HTML 模板支持链接
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()

        if result.get("code") == 200:
            print(f"✅ 微信推送已发送")
            return True
        else:
            print(f"❌ 推送失败: {result.get('msg', '未知错误')}")
            return False

    except Exception as e:
        print(f"❌ 推送错误: {e}")
        return False


def main():
    """主函数"""
    # 从环境变量获取配置
    token = os.environ.get("PUSHPLUS_TOKEN")
    if not token:
        print("❌ 请设置 PUSHPLUS_TOKEN 环境变量")
        sys.exit(1)

    # 读取最新的简报内容
    script_dir = Path(__file__).parent.parent
    digest_file_path = script_dir / 'digest_file.txt'

    try:
        with open(digest_file_path, 'r') as f:
            digest_file = f.read().strip()

        with open(digest_file, "r", encoding="utf-8") as f:
            content = f.read()

        # 构建标题
        tz = pytz.timezone("Asia/Shanghai")
        today = datetime.now(tz).strftime("%Y-%m-%d")
        title = f"🎓 教师考编结构化面试简报 {today}"

        print(f"📤 准备发送微信推送...")
        print(f"   标题: {title}")
        print(f"   简报长度: {len(content)} 字符")

        # 发送简报通知
        success = send_pushplus_notification(
            token=token,
            title=title,
            content=content
        )

        sys.exit(0 if success else 1)

    except FileNotFoundError as e:
        print(f"❌ 找不到简报文件: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 推送失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
