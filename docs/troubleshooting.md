# 故障排除（小白版）

**遇到问题别慌，这里都有答案**

---

## 🚨 错误信息对照表

### 1️⃣ 429 错误（最常见）

**错误样子：**
```
❌ 请求失败：HTTP 429 Too Many Requests
```

**原因：** 免费模型用超了，就像免费流量用完了，得等下个周期。

**解决方法（3选1）：**

**A. 等一等（最简单）**
- 等待 1 小时或明天再用
- 免费额度通常按小时或按天重置

**B. 用 or-auto 自动换模型（推荐）**
```bash
or-auto "你的问题"
```
它会自动尝试下一个模型，直到有可用的。

**C. 检查你的模型列表**
```bash
or-auto --list-models
```
如果所有模型都挂掉，说明今天的免费额度真的用完了，等明天。

---

### 2️⃣ 403 错误（地区限制）

**错误样子：**
```
❌ 请求失败：HTTP 403 Forbidden
```

**原因：** 某些模型（如 Google、Meta 的部分模型）在中国大陆不能用。

**解决方法：**
or-auto 会自动跳过这些模型，你不需要做任何事。

如果某个模型总是 403，说明它不适合你的地区，等自动刷新时会被替换成可用的。

---

### 3️⃣ 400 错误（模型出错了）

**错误样子：**
```
❌ 请求失败：HTTP 400 Bad Request
```

**原因：** 这个模型本身有问题（比如 API 格式不对），不是你的错。

**解决方法：**
or-auto 会立即尝试下一个模型，通常你能收到答案，只是会慢一点。

如果频繁出现，可以手动禁用这个模型（需要改配置文件，进阶功能）。

---

### 4️⃣ 找不到 API Key

**错误样子：**
```
❌ 未找到 OPENROUTER_API_KEY
```

**原因：** 你没告诉 or-auto 你的 OpenRouter 密钥。

**解决方法：**

**方案A：设置环境变量（推荐）**
```bash
# 编辑配置文件
nano ~/.bashrc
```
在文件最后加一行（换成你的真实密钥）：
```
export OPENROUTER_API_KEY="sk-or-v1-xxxxxxxx"
```
保存（Ctrl+X → Y → Enter）后，运行：
```bash
source ~/.bashrc
```

**方案B：创建文件**
```bash
echo "sk-or-v1-xxxxxxxx" > ~/文档/AI工具/openrouter.txt
```

**验证是否成功：**
```bash
echo $OPENROUTER_API_KEY
# 应该看到你的密钥
```

---

### 5️⃣ 缓存文件不存在

**错误样子：**
```
缓存文件不存在: ~/.openclaw/.freeride-cache.json
```

**原因：** 这是第一次使用，还没有模型列表缓存。

**这不是错误！** or-auto 会使用内置的默认模型列表工作。

**如果你想生成优化后的列表：**
```bash
# 使用 freeride 技能刷新（需要 OpenClaw 已安装）
python ~/.copaw/workspaces/default/skills/freeride/main.py refresh
```

或者等自动刷新任务运行。

---

### 6️⃣ or-auto 命令找不到

**错误样子：**
```
bash: or-auto: command not found
```

**原因：** 安装目录不在系统的 PATH 里。

**解决方法：**

**A. 找 or-auto 到底在哪里**
```bash
find ~ -name "or-auto" 2>/dev/null
```
可能输出：
- `/home/lbd/.local/bin/or-auto`
- `/home/lbd/.venv/bin/or-auto`

**B. 方法1 - 用绝对路径**
```bash
# 如果找到是 /home/lbd/.local/bin/or-auto
/home/lbd/.local/bin/or-auto "测试"
```

**B. 方法2 - 加到 PATH**
```bash
# 编辑配置文件
nano ~/.bashrc
```
在末尾加（路径换成你的实际路径）：
```bash
export PATH="$HOME/.local/bin:$PATH"
```
保存后：
```bash
source ~/.bashrc
```
现在 `or-auto` 应该就能用了。

---

### 7️⃣ 某个模型一直不动/很慢

**现象：** `or-auto "问题"` 等很久才出结果，或者一直卡住。

**原因：**
- 当前选中的模型质量高，但推理慢（比如 100B 参数的大模型）
- 网络慢
- 模型临时过载

**解决：**

**A. 强制换快一点的模型**
```bash
or-auto "问题" --model nvidia/nemotron-3-nano-30b-a3b:free
```
这个模型小而快。

**B. 调整模型优先级（需要改配置）**
编辑 `~/.openrouter_fallback_config.json`，把快模型放前面。

---

### 8️⃣ cron 任务不执行

**现象：** 设置了自动刷新，但日志文件没更新。

**排查步骤：**

**1. 检查 cron 服务是否在跑**
```bash
systemctl --user status cron
```
如果显示 `inactive (dead)`，启动它：
```bash
systemctl --user enable --now cron
```

**2. 检查 crontab 列表**
```bash
crontab -l
```
确保你能看到那一行 `0 3 * * * ...`

**3. 检查日志文件权限**
```bash
ls -la ~/.copaw/logs/
# 确保你的用户有写权限
```

**4. 手动测试命令**
```bash
/home/lbd/.local/bin/or-auto --refresh
```
如果这里能成功，cron 也应该能。

**5. 查看 cron 自己的日志**
```bash
journalctl --user -u cron -f
```
看看有没有执行记录或错误。

---

### 9️⃣ 刷新后模型列表没变化

**现象：** 运行 `or-auto --refresh`，然后 `or-auto --list-models`，列表没变。

**可能原因：**

**A. OpenRouter 接口变动**
-free 模型的 endpoint 可能已变更，需要更新技能。

**解决：** 检查 `skills/freeride` 是否最新，或手动运行更新脚本：
```bash
python ~/.copaw/workspaces/default/skills/freeride/main.py refresh --force
```

**B. 缓存没被读取**
确保 `~/.openclaw/.freeride-cache.json` 有内容：
```bash
ls -lh ~/.openclaw/.freeride-cache.json
cat ~/.openclaw/.freeride-cache.json | jq '.models | length'
```

---

### 🔟 流式输出（打字机效果）不支持

**问题：** 能不能像 ChatGPT 那样逐字显示？

**回答：** 当前版本（1.0.0）不支持流式输出，所有答案一次性返回。

下个版本计划支持，敬请期待。

---

## 🆘 仍然有问题？

### 提供这些信息，更容易解决：

1. **操作系统**：`uname -a`
2. **or-auto 版本**：`or-auto --version`
3. **完整错误信息**：截图或复制粘贴
4. **你做了什么**：一步步操作
5. **日志内容**：`cat ~/.copaw/logs/freeride-auto-refresh.log`

### 哪里提问：

- 📝 提 Issue（待定 GitHub 地址）
- 💬 在 OpenClaw 社区问
- 📧 发邮件（待定）

---

## ✅ 快速自查清单

| 问题 | 检查点 | 解决 |
|------|--------|------|
| command not found | 是否安装成功？`pip show openrouter-fallback` | 重装或加 PATH |
| 429 错误 | 额度用超？等1小时 | or-auto自动降级 |
| 403 错误 | 模型地区限制？ | 自动跳过，等刷新 |
| API key 未找到 | `echo $OPENROUTER_API_KEY` 有值吗？ | 设置环境变量 |
| cron 不运行 | `systemctl --user status cron` 是 active 吗？ | 启动 cron 服务 |
| 刷新无效 | 缓存文件有内容吗？`jq '.models | length' ~/.openclaw/.freeride-cache.json` | 手动强制刷新 |

---

**记住：** or-auto 就是用来处理这些错误的，大部分情况下你不需要做任何事，它会自己搞定。

如果问题持续，我们来升级代码！🚀
