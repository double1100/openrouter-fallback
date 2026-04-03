# 自动更新免费模型（超详细教程）

> 让模型列表永远保持最新，新出的免费模型自动用上

---

## ❓ 为什么要自动更新？

OpenRouter 的免费模型列表就像"流动的河"：
- ✨ 新的好模型会出现（比如刚出的 Qwen 3.6 Plus）
- ❌ 差的模型会被下架或限流
- 🔄 每天的免费额度会重置

**如果不更新：** 你可能还在用旧模型，不知道有更好的。

**自动更新后：** 系统自动检测、自动下载最新推荐列表，你永远用当前最好的。

---

## 📅 两种自动更新方式

| 方式 | 优点 | 缺点 | 适合谁 |
|------|------|------|--------|
| **Cron** (Linux 自带) | 100%可靠，系统级，重启也生效 | 需要命令行操作 | 所有人 |
| **OpenClaw 心跳** | 和 OpenClaw 深度集成 | OpenClaw 不一定支持 | 开发者 |

**推荐：** 用 Cron，简单可靠。

---

## 🔧 方式一：Cron（推荐，3分钟搞定）

Cron 是 Linux 自带的定时任务，相当于你的私人秘书，每天帮你点一下"刷新"按钮。

### 第1步：找到 or-auto 命令的位置

```bash
which or-auto
```

可能输出：
- `/home/lbd/.local/bin/or-auto`
- 或 `/usr/local/bin/or-auto`
- 或找不到（说明 PATH 没配好）

**如果找不到：**
```bash
# 试试这个
python -c "import openrouter_fallback; print(openrouter_fallback.__file__)"
# 输出类似：/home/lbd/.venv/lib/python3.10/site-packages/openrouter_fallback/__init__.py
# 那么 or-auto 在那个目录的 ../bin/or-auto

# 直接创建软链接到 ~/.local/bin
ln -s /完整路径/or-auto ~/.local/bin/or-auto
```

### 第2步：测试手动刷新

```bash
or-auto --refresh
```

如果看到 `✅ 刷新完成`，说明功能正常。

**提示：** `--refresh` 会：
1. 调用 freeride 技能更新 `~/.openclaw/.freeride-cache.json`
2. 下载最新的免费模型列表
3. 更新推荐排序

### 第3步：添加 cron 任务

```bash
crontab -e
```

如果是第一次，会问用什么编辑器，选 **nano**（最简单，序号1）。

然后会出现一个空文件，在最后加一行：

```bash
0 3 * * * /home/你的用户名/.local/bin/or-auto --refresh >> /home/你的用户名/.copaw/logs/freeride-auto-refresh.log 2>&1
```

**修改这里的"你的用户名"：**
```bash
whoami
# 比如输出 lbd，那路径就是 /home/lbd
```

完整例子（用户 lbd）：
```bash
0 3 * * * /home/lbd/.local/bin/or-auto --refresh >> /home/lbd/.copaw/logs/freeride-auto-refresh.log 2>&1
```

**这一行是什么意思？**
- `0 3 * * *` → 每天凌晨3点整执行
- `/home/lbd/.local/bin/or-auto` → 要执行的命令
- `--refresh` → 参数：刷新模型
- `>> /home/lbd/.copaw/logs/freeride-auto-refresh.log` → 日志存这里
- `2>&1` → 错误也记到同一个日志

保存：`Ctrl+X` → `Y` → `Enter`

### 第4步：验证 crontab 是否生效

```bash
crontab -l
```

应该看到你刚加的那行。

### 第5步：测试立即执行一次（不等3点）

```bash
# 假设你的命令是 /home/lbd/.local/bin/or-auto --refresh
/home/lbd/.local/bin/or-auto --refresh
```

看输出：`✅ 刷新完成`

看日志：
```bash
tail -f /home/lbd/.copaw/logs/freeride-auto-refresh.log
```

### 第6步：检查明早是否自动运行

第二天早上3点后：
```bash
tail -20 /home/lbd/.copaw/logs/freeride-auto-refresh.log
```

应该看到类似：
```
[2025-04-04 03:00:00] 🔄 开始自动刷新...
[2025-04-04 03:00:05] ✅ 刷新完成，更新了 5 个模型
```

---

## 🔄 方式二：OpenClaw 心跳（如果支持的话）

OpenClaw 可能有类似 `HEARTBEAT.md` 的机制，定期检查并执行里面的命令。

### 1. 编辑 OpenClaw 的心跳文件

```bash
nano ~/.copaw/workspaces/default/HEARTBEAT.md
```

在 `## Tasks` 下面加：

```markdown
### 🔄 OpenRouter 模型自动刷新

- [ ] 检查缓存：如果 `~/.openclaw/.freeride-cache.json` 存在且修改时间 <6小时 → 跳过
- [ ] 否则执行：`export OPENROUTER_API_KEY="你的密钥" && or-auto --refresh`
- [ ] 记录日志到 `~/.copaw/logs/freeride-refresh.log`
```

### 2. 确保 OpenClaw daemon 在运行

```bash
systemctl --user status copaw
# 应该看到 active (running)
```

如果没运行：
```bash
systemctl --user enable --now copaw
```

### 3. 手动触发一次心跳测试

```bash
# 方法A：重启 daemon
systemctl --user restart copaw

# 方法B：等待下一次心跳（默认30分钟）
```

查看日志：
```bash
journalctl --user -u copaw -f
```

---

**注意：** OpenClaw 的心跳机制可能和 CoPaw 不同，如果 `HEARTBEAT.md` 无效，请改用 Cron 方式。

---

## ⚙️ 高级：调整刷新频率

### 更频繁（每6小时）

```bash
crontab -e
# 加这一行：
0 */6 * * * /home/lbd/.local/bin/or-auto --refresh >> /home/lbd/.copaw/logs/freeride-auto-refresh.log 2>&1
```

### 只在工作日刷新

```bash
crontab -e
# 加这一行（周一到周五，凌晨3点）：
0 3 * * 1-5 /home/lbd/.local/bin/or-auto --refresh >> /home/lbd/.copaw/logs/freeride-auto-refresh.log 2>&1
```

 Cron 时间解释：
```
* * * * *
│ │ │ │ │
│ │ │ │ └── 星期几 (0-7, 0和7都代表周日)
│ │ │ └──── 月份 (1-12)
│ │ └────── 日期 (1-31)
│ └──────── 小时 (0-23)
└────────── 分钟 (0-59)
```

---

## 🐛 故障排除

### 问题1: `or-auto: command not found` in cron

原因：cron 的 PATH 和你的 shell 不一样。

解决：
```bash
# 在 crontab 里用绝对路径
crontab -e
# 改成：
0 3 * * * /bin/bash -c '/home/lbd/.local/bin/or-auto --refresh >> /home/lbd/.copaw/logs/freeride-auto-refresh.log 2>&1'
```

### 问题2: cron 不执行，日志是空的

检查 cron 服务是否运行：
```bash
systemctl --user status cron
# 如果显示 inactive，启动：
systemctl --user enable --now cron
```

### 问题3: 刷新失败，网络超时

原因：OpenRouter API 有时慢。

解决：增加 `--timeout` 参数（当前版本可能不支持，等待更新）

### 问题4: 日志文件越来越大

需要用 logrotate 管理，或手动清空：
```bash
# 清空但不删除文件
> /home/lbd/.copaw/logs/freeride-auto-refresh.log
```

---

## 📊 监控与提醒

### 设置失败提醒（可选）

如果刷新失败，给自己发一封邮件：
```bash
crontab -e
0 3 * * * /home/lbd/.local/bin/or-auto --refresh >> /home/lbd/.copaw/logs/freeride-auto-refresh.log 2>&1 || echo "or-auto refresh failed at $(date)" | mail -s "OpenRouter Fallback Alert" 你的邮箱@example.com
```

需要先配置 mail 命令（略复杂，小白跳过）。

---

## ✅ 最佳实践

1. **日志位置：** 固定记到 `~/.copaw/logs/`，方便统一管理
2. **权限：** 确保日志目录可写：`chmod 755 ~/.copaw/logs`
3. **频率：** 每天一次足够，OpenRouter 模型不会一天一变
4. **测试：** 每周末手动跑一次 `or-auto --refresh` 检查是否正常
5. **备份：** 把 crontab 内容备份到 `~/copaw工作室/配置文件备份/crontab-backup.txt`

---

## 🔚 总结

**最简配置（复制即用）：**
```bash
# 1. 设置环境变量（一次）
echo 'export OPENROUTER_API_KEY="你的密钥"' >> ~/.bashrc && source ~/.bashrc

# 2. 安装（一次）
pip install openrouter-fallback

# 3. 添加 cron（一次）
(crontab -l 2>/dev/null; echo "0 3 * * * /home/$(whoami)/.local/bin/or-auto --refresh >> /home/$(whoami)/.copaw/logs/freeride-auto-refresh.log 2>&1") | crontab -
```

**done！** 以后每年 365 天，每天凌晨 3 点自动更新，你什么都不用管。

---

**有问题？** 看 `troubleshooting.md` 或提 Issue。
