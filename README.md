# 教师考编结构化面试考情收集 🎓

> 每天自动收集各地教师招聘结构化面试信息，AI 生成考情简报，微信推送提醒

## ✨ 功能特点

- 🎯 **精准聚焦**: 专门收集结构化面试相关信息
- 🤖 **AI 分析**: 使用 Claude AI 生成专业考情简报（8大板块）
- ⏰ **时间优先**: 重点捕捉面试时间，按紧急程度分类
- 💎 **真题丰富**: 收集真题和答题思路
- 📱 **自动推送**: 每天早上 7:00 推送到微信

## 📊 简报内容

1. 🎯 即将到来的结构化面试（7天/30天）
2. 📊 近期考情汇总（地区分布、形式趋势）
3. 💎 真题精选（答题思路和得分点）
4. 📈 考情趋势分析
5. 🎓 高频考点速查表
6. 💡 备考策略建议
7. 🔗 重要资源链接
8. ⏰ 下一步行动提醒

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/YOUR_USERNAME/teacher-interview-digest.git
cd teacher-interview-digest
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
export ANTHROPIC_API_KEY=your_api_key
export PUSHPLUS_TOKEN=your_token
```

### 4. 运行

```bash
python scripts/interview_digest.py
```

## ⚙️ 配置说明

编辑 `scripts/config.json` 来自定义：

- **target_regions**: 目标抓取地区
- **data_sources**: 数据源配置
- **filters**: 关键词过滤规则

## 📦 部署到 GitHub Actions

1. **Fork 或创建此仓库**

2. **配置 GitHub Secrets**:
   - `ANTHROPIC_API_KEY`: Claude API 密钥
   - `PUSHPLUS_TOKEN`: 微信推送 Token

3. **启用 GitHub Actions**:
   - 进入 Actions 页面
   - 启用 "教师考编结构化面试每日简报" workflow
   - 每天早上 7:00 自动运行

## 📂 项目结构

```
teacher-interview-digest/
├── scripts/
│   ├── interview_digest.py       # 主脚本
│   ├── send_pushplus.py          # 微信推送
│   ├── config.json               # 配置
│   ├── scrapers/                 # 爬虫模块
│   └── analyzers/                # AI 分析模块
├── digests/                      # 简报输出
├── .github/workflows/            # GitHub Actions
└── SKILL.md                      # 详细文档
```

## 🔧 技术栈

- Python 3.9+
- Anthropic Claude AI (GLM-4-Plus)
- BeautifulSoup4
- GitHub Actions
- PushPlus

## 📝 License

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**Made with ❤️ by Claude (猫娘幽浮喵)**
