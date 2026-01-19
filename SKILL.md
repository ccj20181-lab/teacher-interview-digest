# 教师考编结构化面试考情收集 Skill

> 每天自动收集各地教师招聘结构化面试信息，AI 生成考情简报，微信推送提醒

## 🎯 功能特点

### 核心功能

- **精准数据收集**: 专门抓取结构化面试相关的招聘公告
- **智能时间提取**: AI 自动识别和提取结构化面试时间
- **考情分析**: 使用 Claude AI 生成专业的结构化面试考情简报
- **自动推送**: 每天早上 7:00 推送到微信，紧急面试顶部突出显示
- **真题资源**: 收集整理结构化面试真题和答题思路

### 简报内容（8大板块）

1. **🎯 即将到来的结构化面试** - 按紧急程度分类（7天/30天）
2. **📊 近期考情汇总** - 地区分布、时间集中期、形式趋势
3. **💎 真题精选** - 5-8道最具代表性的真题 + 答题思路
4. **📈 考情趋势分析** - 难度变化、题型趋势、地区特色
5. **🎓 高频考点速查** - 表格形式快速查阅
6. **💡 备考策略建议** - 按时间倒推的备考计划
7. **🔗 重要资源链接** - 公告、真题、备考资料
8. **⏰ 下一步行动提醒** - 明确的时间线提醒

## 📦 安装和使用

### 1. 安装依赖

```bash
cd ~/.claude/skills/teacher-interview-digest
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件或设置环境变量：

```bash
# 必需
export ANTHROPIC_API_KEY=sk-ant-xxx
export PUSHPLUS_TOKEN=xxx

# 可选（使用自定义 API 端点）
export ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/anthropic
```

### 3. 运行简报生成

```bash
python scripts/interview_digest.py
```

生成的简报将保存在 `digests/` 目录下。

### 4. 测试微信推送

```bash
python scripts/send_pushplus.py
```

## ⚙️ 配置说明

配置文件位于 `scripts/config.json`：

```json
{
  "target_regions": [
    "北京", "上海", "广东", "江苏", "浙江",
    "山东", "河南", "四川", "湖北", "湖南"
  ],
  "data_sources": {
    "gov_websites": {
      "enabled": true,
      "priority": 1,
      "sites": {
        "教育部": "http://www.moe.gov.cn/",
        "北京": "http://jw.beijing.gov.cn/",
        ...
      }
    }
  },
  "filters": {
    "interview_keywords": [
      "结构化面试", "面试安排", "面试通知",
      "面试公告", "答辩", "面试时间"
    ],
    "max_age_days": 90
  }
}
```

### 配置项说明

- **target_regions**: 目标抓取地区列表
- **data_sources**: 数据源配置
  - `enabled`: 是否启用该数据源
  - `priority`: 优先级（数字越小优先级越高）
  - `sites`: 具体网站配置
- **filters**: 过滤规则
  - `interview_keywords`: 结构化面试关键词（用于筛选公告）
  - `max_age_days`: 抓取最近多少天的公告

## 🚀 GitHub Actions 自动化

### 配置 Secrets

在 GitHub 仓库设置中添加以下 Secrets：

- `ANTHROPIC_API_KEY`: Claude API 密钥
- `ANTHROPIC_BASE_URL`: API 端点（可选）
- `PUSHPLUS_TOKEN`: 微信推送 Token

### 定时任务

默认配置：每天北京时间 **07:00** 自动运行

可在 `.github/workflows/daily-interview-digest.yml` 中修改：

```yaml
schedule:
  - cron: '0 23 * * *'  # UTC 23:00 = 北京时间 07:00
```

### 手动触发

在 GitHub Actions 页面点击 "Run workflow" 按钮手动触发。

## 📂 目录结构

```
teacher-interview-digest/
├── SKILL.md                      # 本文档
├── requirements.txt              # Python 依赖
├── scripts/
│   ├── interview_digest.py       # 主执行脚本
│   ├── send_pushplus.py          # 微信推送脚本
│   ├── config.json               # 配置文件
│   ├── scrapers/                 # 爬虫模块
│   │   ├── __init__.py
│   │   ├── base_scraper.py       # 基础爬虫类
│   │   └── gov_site_scraper.py   # 官网爬虫
│   └── analyzers/                # AI 分析模块
│       ├── __init__.py
│       └── interview_analyzer.py # AI 分析器
├── digests/                      # 简报输出目录
├── data/
│   ├── exam_schedule.json        # 面试时间表
│   └── logs/                     # 日志目录
└── .github/workflows/
    └── daily-interview-digest.yml # GitHub Actions 配置
```

## 🔧 技术栈

- **Python 3.9+**
- **Anthropic Claude AI** (GLM-4-Plus)
- **BeautifulSoup4** (网页解析)
- **GitHub Actions** (自动化)
- **PushPlus** (微信推送)

## 💡 使用技巧

### 自定义地区

编辑 `config.json`，在 `target_regions` 中添加或删除地区：

```json
{
  "target_regions": ["北京", "上海", "广东"]
}
```

### 调整抓取时间范围

修改 `filters.max_age_days`：

```json
{
  "filters": {
    "max_age_days": 30  // 只抓取最近30天
  }
}
```

### 本地测试

```bash
# 设置测试环境变量
export ANTHROPIC_API_KEY=your_key
export PUSHPLUS_TOKEN=your_token

# 运行脚本
python scripts/interview_digest.py
```

## 🐛 故障排除

### 问题：抓取不到数据

**解决方案**：
1. 检查网络连接
2. 确认目标网站是否可访问
3. 查看日志输出的错误信息
4. 尝试减少 `max_age_days` 值

### 问题：AI 生成失败

**解决方案**：
1. 检查 `ANTHROPIC_API_KEY` 是否正确
2. 确认 API 端点是否可访问
3. 检查 API 配额是否用尽
4. 查看错误日志

### 问题：微信推送失败

**解决方案**：
1. 确认 `PUSHPLUS_TOKEN` 是否正确
2. 检查 PushPlus 服务状态
3. 确认简报文件是否生成

## 📊 输出文件

### 1. 简报文件

位置: `digests/interview-digest-YYYY-MM-DD.md`

格式: Markdown

示例:
```markdown
# 教师考编结构化面试考情简报 (2026-01-19)

## 🎯 即将到来的结构化面试

**[紧急] 7天内面试**
...
```

### 2. 面试时间表

位置: `data/exam_schedule.json`

格式: JSON

用途: 程序化访问面试时间数据

## 🎓 与普通招聘信息收集的区别

| 维度 | 普通招聘信息收集 | 本 Skill |
|------|-----------------|---------|
| **聚焦点** | 招聘岗位、报名信息 | **结构化面试时间**、真题、备考策略 |
| **时间精度** | 报名时间范围 | **精确到小时的面试时间** |
| **内容深度** | 基本信息 | AI 分析的考情趋势和答题思路 |
| **推送策略** | 按时推送 | **紧急面试顶部突出显示** |
| **用户价值** | 信息获取 | **备考决策支持** |

## 🚧 未来扩展

- [ ] 支持小红书 MCP 工具抓取真题
- [ ] 智能订阅特定地区/学科
- [ ] 历史考情数据分析
- [ ] AI 模拟结构化面试
- [ ] 建立真题数据库
- [ ] 个性化备考日历

## 📝 License

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**作者**: Claude (猫娘幽浮喵) ฅ'ω'ฅ

**最后更新**: 2026-01-19
