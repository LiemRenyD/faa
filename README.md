# 信仰答题自动化工具

基于 Playwright 的自动化答题工具，支持填空题、判断题、多选题等多种题型。

## 功能特点

- ✅ 自动登录答题系统
- ✅ 支持多种题型（填空、判断、多选）
- ✅ 智能题库匹配
- ✅ 可配置答题间隔和轮数
- ✅ 模拟真实用户操作

## 环境要求

- Python 3.8+
- Playwright

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
playwright install
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env`：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填写你的账号信息和配置：

```ini
# 账号信息
PHONE_NUMBER=你的手机号
PASSWORD=你的密码

# 网站配置
WEBSITE_URL=登录页面URL
QUESTION_URL=答题页面URL

# 答题配置
QUESTIONLIMIT=10          # 每轮答题数量
MAX_ROUNDS=1              # 最大运行轮数
ANSWER_INTERVAL=500       # 答题间隔（毫秒）
HEADLESS=false            # 是否无头模式
```

### 3. 准备题库

将题库文件放置在 `data/question_bank.json`，格式如下：

```json
{
  "questions": [
    {
      "question_id": "3547276",
      "question_text": "题目内容",
      "question_type": "填空题",
      "answer": "答案内容",
      "options": {}
    }
  ]
}
```

### 4. 运行程序

```bash
python main.py
```

## 配置说明

### 必填配置

| 参数 | 说明 | 示例 |
|------|------|------|
| PHONE_NUMBER | 登录手机号 | 13800138000 |
| PASSWORD | 登录密码 | your_password |
| WEBSITE_URL | 登录页面URL | https://.../mlogin |
| QUESTION_URL | 答题页面URL | https://.../practice |

### 可选配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| QUESTIONLIMIT | 10 | 每轮答题数量限制 |
| MAX_ROUNDS | 1 | 最大运行轮数 |
| ANSWER_INTERVAL | 500 | 每题答题间隔（毫秒） |
| ANSWERTIMELIMIT | 20 | 答题时限（秒） |
| END_SCORE | 180 | 目标分数 |
| HEADLESS | false | 是否无头模式运行 |

## 项目结构

```
faith_auto_answer/
├── src/
│   ├── config/           # 配置管理
│   ├── core/             # 浏览器管理
│   ├── handlers/         # 题型处理器
│   ├── models/           # 数据模型
│   ├── services/         # 业务逻辑
│   └── storage/          # 数据存储
├── data/
│   └── question_bank.json  # 题库文件
├── output/               # 输出目录
├── tests/                # 测试文件
├── main.py               # 入口文件
├── .env                  # 环境配置（不提交到Git）
├── .env.example          # 配置模板
└── requirements.txt      # 依赖列表
```

## 注意事项

1. ⚠️ **不要将 `.env` 文件提交到 Git**（已加入 `.gitignore`）
2. 📝 确保题库文件格式正确
3. 🌐 首次运行建议设置 `HEADLESS=false` 观察运行情况
4. ⏱️ 适当调整 `ANSWER_INTERVAL` 避免被检测为机器人

## 常见问题

### Q: 登录失败怎么办？
A: 检查 `PHONE_NUMBER` 和 `PASSWORD` 是否正确，确认 `WEBSITE_URL` 是否可以正常访问。

### Q: 答题时卡住不动？
A: 检查网络连接，确认 `QUESTION_URL` 是否正确，查看控制台错误信息。

### Q: 答案没有填入？
A: 检查 `data/question_bank.json` 中是否有对应题目的答案，确认题目 ID 或内容是否匹配。

## License

MIT
