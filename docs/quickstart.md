# 快速开始（小白版）

**目标：** 3分钟安装成功，立刻用上免费 AI

---

## ⏱️ 真的只要3分钟？

是的！整个过程就 4 步：

1. 复制命令
2. 粘贴回车
3. 填你的 API 密钥
4. 测试

---

## 📋 准备工作

### 你需要：

- ✅ 已经安装了 OpenClaw（或其他任何用 OpenRouter 的程序）
- ✅ 能访问外网（需要访问 openrouter.ai）
- ✅ 有 `pip` 命令（Python 包管理器）

### 获取免费 API 密钥（30秒）

1. 打开 https://openrouter.ai/keys
2. 点右上角 "Sign Up" → 用邮箱注册
3. 登录 → 点 "Create Key"
4. 复制那一长串字符（以 `sk-or-v1-` 开头）

**记住：** 这个密钥以后就是你的"身份证"，不要告诉别人。

---

## 🚀 安装

### 选项A：一键安装（推荐）

```bash
# 复制整行，粘贴到终端，回车
pip install openrouter-fallback
```

如果提示 `pip: command not found`，说明 Python 没装对，先装 Python 3.10+。

### 选项B：手动安装（如果选项A失败）

```bash
# 1. 下载代码（我已经保存在工作室了）
cd ~/copaw工作室/项目/开源作品/openrouter-fallback

# 2. 安装
pip install -e .

# 3. 验证
or-auto --version
# 应该看到：or-auto 1.0.0
```

---

## 🔐 设置你的 API 密钥

**重要：** 必须设置，否则无法连接 OpenRouter。

### 方法1：环境变量（最干净）

```bash
# 编辑配置文件
nano ~/.bashrc
```

按方向键到底，加一行：

```
export OPENROUTER_API_KEY="sk-or-v1-你刚才复制的密钥"
```

**注意：** 双引号要保留，里面的内容换成你的真实密钥。

保存：`Ctrl+X` → `Y` → `Enter`

然后让配置生效：
```bash
source ~/.bashrc
```

测试：
```bash
echo $OPENROUTER_API_KEY
# 应该显示你的密钥
```

### 方法2：创建文件（如果你不想碰配置文件）

```bash
mkdir -p ~/文档/AI工具
echo "sk-or-v1-你的密钥" > ~/文档/AI工具/openrouter.txt
```

or-auto 会自动读取这个文件。

---

## 🧪 测试连接

```bash
or-auto --test
```

**预期输出1（成功）：**
```
🧪 测试OpenRouter连接...
✅ 测试成功！
模型: qwen/qwen3.6-plus:free
响应: 你好！我是...
```

**预期输出2（网络问题）：**
```
❌ 连接失败：HTTP 429
```
这时检查：密钥是否正确、网络是否通、模型是否用超（等几小时再试）

---

## 🎉 开始用！

### 最简单的用法

```bash
or-auto "今天天气怎么样？"
```

就这么简单！它会自动选最好的免费模型回答你。

### 列出所有可用的免费模型

```bash
or-auto --list-models
```

你会看到类似：
```
1. qwen/qwen3.6-plus:free      (100万上下文)
2. nvidia/nemotron-3-super...  (NVIDIA顶级)
3. stepfun/step-3.5-flash:free (国内可用)
...
```

### 指定模型（可选）

```bash
or-auto "用最简单的话解释黑洞" --model stepfun/step-3.5-flash:free
```

即使指定了，如果这个模型挂掉，会自动换别的，你的问题不会丢。

---

## 🔄 让模型列表自动更新（可选但推荐）

OpenRouter 的模型列表会变（新的上架、旧的下架），我们需要定期更新。

### 最简单：设置每天自动刷新

```bash
crontab -e
```

第一次会选编辑器，选 `nano`（第一个选项）

然后在文件末尾加一行：

```bash
0 3 * * * /home/你的用户名/.local/bin/or-auto --refresh >> /tmp/or-refresh.log 2>&1
```

**注意：** 把 `/home/你的用户名/` 换成你的真实路径（比如 `/home/lbd/`）

如何知道你的用户名？
```bash
whoami
# 打印你的用户名
```

保存：`Ctrl+X` → `Y` → `Enter`

完成！以后每天凌晨3点会自动更新模型列表。

**手动测试：**
```bash
or-auto --refresh
# 应该看到：✅ 刷新完成，更新了 X 个模型
```

---

## ❓ 遇到问题？

### 问题1: `or-auto: command not found`

原因：安装目录不在 PATH 里。

解决：
```bash
# 方法A：直接调用
python -m openrouter_fallback "问题"

# 方法B：把 ~/.local/bin 加入 PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 问题2: 报错 429 (Too Many Requests)

原因：免费模型用超了，正常现象。

解决：
- 等几小时再试
- or-auto 会自动降级，如果所有模型都429，说明今天额度确实用完了

### 问题3: 某个模型一直挂掉？

原因：地区限制或模型下架。

解决：or-auto 会自动跳过，等自动刷新更新列表即可。

### 问题4: 不会用 nano 编辑器？

用 `vim` 代替：
```bash
crontab -e
# 按 i 进入插入模式
# 粘贴内容
# 按 Esc 退出插入
# 输入 :wq 保存退出
```

或者不碰 crontab：
```bash
# 直接把命令写入 cron
(crontab -l 2>/dev/null; echo "0 3 * * * /home/你的用户名/.local/bin/or-auto --refresh >> /tmp/or-refresh.log 2>&1") | crontab -
```

---

## ✅ 检查清单

完成这些，你就算成功了：

- [ ] API 密钥已设置（`echo $OPENROUTER_API_KEY` 能看到）
- [ ] `or-auto --test` 显示 ✅
- [ ] `or-auto "测试问题"` 有答案
- [ ] (可选) `crontab -l` 能看到自动刷新任务

---

## 🎯 下一步

- 把 `or-auto` 加入你的日常工具链
- 如果用在 OpenClaw，记得设置 fallback 模型列表为 `~/.openclaw/.freeride-cache.json` 里的模型
- 遇到问题先看 `docs/troubleshooting.md`

---

**恭喜！你已经拥有一个永不中断的免费 AI 助手！** 🎉
