# OpenRouter Fallback - 小白版

> 让 OpenClaw 永远有免费的 AI 用，自动切换，永不中断

---

## 🎯 这是什么？

简单说：**一个帮你省钱的聪明助手**

- OpenClaw 是一个 AI 助手软件
- OpenRouter 是 AI 模型的"超市"
- 有些模型免费，但有使用限制（就像免费试用，用超了就限流）
- 这个工具让 OpenClaw **自动换模型**，一个用不了了马上换下一个，你永远不停机

**效果：** 你以为在用 Qwen，其实它偷偷换了 Nemotron，你完全无感。

---

## 🆓 真的免费吗？

是的！这些模型在 OpenRouter 上真的免费（不用信用卡）：

| 模型 | 特点 | 国内速度 |
|------|------|----------|
| Qwen 3.6 Plus | 最强，100万上下文 | ✅ 快 |
| Nemotron 3 Super | NVIDIA出品，质量高 | ✅ 快 |
| StepFun 3.5 Flash | 速度快，人话好 | ✅ 快 |
| Qwen Coder | 写代码专用 | ✅ 快 |
| Nemotron Nano | 轻量，备胎 | ✅ 快 |

---

## 📦 安装（3分钟）

### 第一步：准备 OpenClaw

确保你已经安装了 OpenClaw（还没？去 openclaw.github.io 下载）

### 第二步：获取免费 API 密钥

1. 打开 https://openrouter.ai/keys
2. 点 "Sign Up" 注册（用邮箱，不用信用卡）
3. 登录后点 "Create Key"
4. 复制那一长串字符（以 `sk-or-v1-` 开头）

### 第三步：把密钥告诉电脑

**方法A（推荐）：环境变量**
```bash
# 编辑你的配置文件
nano ~/.bashrc
# 在文件末尾加这一行（替换成你的密钥）
export OPENROUTER_API_KEY="sk-or-v1-你复制的密钥"
# 保存退出（Ctrl+X, Y, Enter）

# 重新加载配置
source ~/.bashrc

# 测试是否成功
echo $OPENROUTER_API_KEY
# 应该看到你的密钥
```

**方法B：建个文件**
```bash
mkdir -p ~/文档/AI工具
echo "sk-or-v1-你复制的密钥" > ~/文档/AI工具/openrouter.txt
```

### 第四步：安装 openrouter-fallback

```bash
# 如果你有 pip
pip install openrouter-fallback

# 或者从源码（我已放在工作室）
cd ~/copaw工作室/项目/开源作品/openrouter-fallback
pip install -e .
```

### 第五步：测试

```bash
or-auto --test
```

预期输出：
```
🧪 测试OpenRouter连接...
✅ 测试成功！模型: qwen/qwen3.6-plus:free
响应: 你好！...
```

如果看到 ✅，说明安装成功！

---

## 🔧 怎么用？

### 最简用法

```bash
or-auto "今天北京天气怎么样？"
```

它会：
1. 用最好的模型（Qwen）问答
2. 如果 Qwen 用超了，自动换下一个（Nemotron）
3. 如果 Nemotron 也不行，再换...
4. 直到有一个能用的

**你什么都不用管，答案直接出来。**

### 列出所有可用的免费模型

```bash
or-auto --list-models
```

你会看到 10 个推荐的模型，按优先级排序。

### 指定用某个模型

```bash
or-auto "写一个Python爬虫" --model stepfun/step-3.5-flash:free
```

即使指定了，如果这个模型挂了，还是会自动降级。

---

## ⚙️ 高级设置

### 1. 让模型列表自动更新（重要！）

OpenRouter 会随时上下架模型，我们需要定期更新推荐列表。

**最简单：用 cron（每天自动刷新）**

```bash
# 输入这个命令
crontab -e
```

会打开一个编辑器， Add下面一行：

```bash
0 3 * * * /home/你的用户名/.venv/bin/or-auto --refresh 2>&1 >> /tmp/or-refresh.log
```

保存退出（如果是 nano：Ctrl+X, Y, Enter）

**作用是：** 每天早上3点自动更新模型列表，有新上的好模型会加进去，下架的会删掉。

**验证是否成功：**
```bash
crontab -l  # 应该看到你刚加的那行
```

第二天早上检查日志：
```bash
cat /tmp/or-refresh.log
```

**注意：** `or-auto --refresh` 功能还在开发中，目前可以每天手动运行一次：
```bash
or-auto --refresh
```

### 2. 调整模型优先级（可选）

如果你想自己控制「哪个模型优先用」，可以编辑配置文件：

```bash
# 创建配置文件
nano ~/.openrouter_fallback_config.json
```

内容示例：
```json
{
  "models": [
    {"id": "stepfun/step-3.5-flash:free", "priority": 1},
    {"id": "qwen/qwen3.6-plus:free", "priority": 2},
    {"id": "nvidia/nemotron-3-super-120b-a12b:free", "priority": 3}
  ]
}
```

保存后，下次 `or-auto` 就会按你这个顺序试。

### 3. 与 OpenClaw 配合使用

**方式A：最简单 - 只让 or-auto 帮你管理模型列表**

你继续用 OpenClaw 原来的设置，但定期运行 `or-auto --refresh` 更新 `~/.openclaw/.freeride-cache.json`，然后手动更新 OpenClaw 的 fallback 列表。

**方式B：全自动 - 让 OpenClaw 直接用 or-auto 的逻辑**（需要写 skill）

这个比较复杂，需要开发技能。如果你不是开发者，跳过。

---

## ❓ 常见问题

### Q1: 报错 "429 Too Many Requests" 怎么办？

答：免费模型用超了，正常。or-auto 会自动换模型。如果所有模型都429，说明今天额度用完了，明天再试。

### Q2: 某个模型一直挂掉？

答：可能地区限制（如 Google 模型国内用不了）。or-auto 会自动跳过，不用你操心。

### Q3: 怎么知道现在用的是哪个模型？

答：加 `--verbose` 参数：
```bash
or-auto "问题" --verbose
```
会打印详细日志，包括尝试了哪些模型。

### Q4: 能流式输出吗（打字机效果）？

答：当前版本不支持流式，后续版本会增加。

### Q5: 怎么停止所有自动任务？

答：
- 停止 cron：`crontab -r`（慎用，会删所有 cron）
- 只删某条：`crontab -e` 删对应行

### Q6: 密钥安全吗？

答：密钥只存在你电脑里，or-auto 不会上传到任何地方（除了 OpenRouter API）。

### Q7: 支持其他 AI 平台吗（如 OpenAI、Claude）？

答：不支持。这个工具专为 OpenRouter 的免费模型设计。

---

## 🗂️ 我该把文件放哪里？

安装后，重要文件位置：

| 文件 | 位置 | 说明 |
|------|------|------|
| 配置文件 | `~/.openrouter_fallback_config.json` | 自定义模型顺序 |
| 缓存文件 | `~/.openclaw/.freeride-cache.json` | 自动生成，别删 |
| 日志 | `~/.copaw/logs/freeride-refresh.log` | cron 刷新的日志 |
| 安装包 | `~/.venv/bin/or-auto` | 命令行工具 |

---

## 📞 需要帮助？

1. 先看本文件（README）
2. 再看 `docs/troubleshooting.md`
3. 还不行？提 Issue（地址待定）

---

## 🎉 总结

三步搞定：
1. **装**：`pip install openrouter-fallback`
2. **设密钥**：`export OPENROUTER_API_KEY=xxx`
3. **用**：`or-auto "你的问题"`

然后 **设置 cron 每天刷新**，以后就不用管了。

---

**版本：** 1.0.0
**许可：** MIT（随便用）
**作者：** [lbd8912](https://github.com/lbd8912)

---

> 💡 **一句话记住：** or-auto 就是 OpenClaw 的「免费模型保底系统」，装好设密钥，从此 AI 用不停。
