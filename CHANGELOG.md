# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-04-03

### Added ✨
- 多模型智能降级系统（最多10个fallback）
- 自动从 FreeRide 缓存加载推荐模型列表
- 指数退避重试机制（429/502/503/504）
- 流式输出支持（stream_chat）
- 命令行工具 `or-auto`
- 详细日志记录
- 配置文件热重载（通过缓存）
- Docker 容器化支持
- MIT 许可证

### Documentation 📖
- 新增小白版 README，3分钟快速上手
- 新增 docs/quickstart.md - 极简安装指南
- 新增 docs/autoupdate.md - 自动更新模型完整教程（cron + OpenClaw 心跳）
- 新增 docs/troubleshooting.md - 常见问题排查
- 新增 docs/SUPPORTED_MODELS.md - 推荐模型列表与说明
- 文档统一使用 OpenRouter 术语，区分 OpenClaw 集成场景

### Technical 🔧
- Python 3.10+ 支持
- 依赖：openai>=2.30.0, requests>=2.31.0
- setuptools/pyproject.toml 打包
- GitHub Actions CI/CD
- 自动发布到 PyPI

### Notes 📝
- 本项目专为 OpenClaw 设计，可与 OpenRouter 免费模型完美配合
- 自动更新机制通过 cron 或 OpenClaw HEARTBEAT.md 触发
- 缓存文件路径: `~/.openclaw/.freeride-cache.json`
- 默认模型优先级按国内可用性 + 质量 + 速度综合排序
