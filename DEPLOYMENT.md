# GitHub Secrets 配置指南 🚀

## 📋 需要配置的 Secrets

请访问以下链接配置仓库 Secrets：

**🔗 配置页面**: https://github.com/ccj20181-lab/teacher-interview-digest/settings/secrets/actions

## 🔑 必需的 Secrets

### 1. ANTHROPIC_API_KEY

- **名称**: `ANTHROPIC_API_KEY`
- **描述**: Claude API 密钥
- **获取方式**:
  1. 访问 https://console.anthropic.com/
  2. 登录并创建 API Key
  3. 复制密钥并粘贴到 Secrets

### 2. PUSHPLUS_TOKEN

- **名称**: `PUSHPLUS_TOKEN`
- **描述**: 微信推送 Token
- **获取方式**:
  1. 访问 http://www.pushplus.plus/
  2. 微信扫码登录
  3. 在"发送消息"页面获取 Token
  4. 复制 Token 并粘贴到 Secrets

## ⚙️ 配置步骤

### 方法一：通过网页配置

1. 访问仓库设置页面：https://github.com/ccj20181-lab/teacher-interview-digest/settings/secrets/actions

2. 点击 "New repository secret"

3. 填写 Secret 信息：
   - **Name**: 输入 Secret 名称（如 `ANTHROPIC_API_KEY`）
   - **Value**: 粘贴密钥值
   - 点击 "Add secret"

4. 重复步骤 2-3 添加所有 Secrets

### 方法二：通过命令行配置（推荐）

```bash
# 设置 ANTHROPIC_API_KEY
gh secret set ANTHROPIC_API_KEY -b"your_api_key_here"

# 设置 PUSHPLUS_TOKEN
gh secret set PUSHPLUS_TOKEN -b"your_pushplus_token_here"
```

## ✅ 验证配置

配置完成后，可以通过以下方式验证：

### 1. 查看 Secrets 列表

```bash
gh secret list
```

### 2. 手动触发 Workflow 测试

1. 访问 Actions 页面：https://github.com/ccj20181-lab/teacher-interview-digest/actions
2. 选择 "教师考编结构化面试每日简报"
3. 点击 "Run workflow" 按钮
4. 选择分支并点击运行

## 📅 定时任务说明

配置完成后，workflow 将：

- **运行时间**: 每天北京时间 **07:00**（UTC 23:00）
- **自动执行**: 数据抓取 → AI 分析 → 简报生成 → 微信推送
- **手动触发**: 随时可以在 Actions 页面手动运行

## 🔧 故障排除

### 问题：Workflow 运行失败

**检查清单**：
1. ✅ Secrets 是否正确配置
2. ✅ API 密钥是否有效
3. ✅ Token 是否有足够权限
4. ✅ 查看 Workflow 日志确认具体错误

### 问题：微信推送失败

**检查清单**：
1. ✅ PushPlus Token 是否正确
2. ✅ PushPlus 服务是否正常
3. ✅ 是否关注了 PushPlus 公众号

### 问题：AI 生成失败

**检查清单**：
1. ✅ Anthropic API Key 是否有效
2. ✅ API 配额是否充足
3. ✅ 网络连接是否正常

## 📞 获取帮助

如果遇到问题：

1. 查看 Workflow 运行日志
2. 检查 [SKILL.md](./SKILL.md) 文档
3. 提交 Issue 到仓库

---

**配置完成后，系统将每天自动运行，为您推送教师考编结构化面试考情简报！** 🎓
