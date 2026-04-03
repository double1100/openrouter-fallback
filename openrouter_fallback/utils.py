"""
工具函数：配置加载、缓存读取、API密钥管理
"""

import json
import logging
import os
from pathlib import Path
from typing import List, Dict, Optional

# 缓存文件位置
DEFAULT_CACHE_PATH = Path.home() / ".openclaw" / ".freeride-cache.json"
# OpenRouter fallback 配置文件
CONFIG_PATH = Path.home() / ".openrouter_fallback_config.json"


def get_api_key() -> Optional[str]:
    """
    获取 OpenRouter API 密钥

    顺序：
    1. 环境变量 OPENROUTER_API_KEY
    2. ~/文档/AI工具/openrouter.txt
    3. ~/.openrouterrc (KEY=...)
    """
    # 1. 环境变量
    api_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if api_key:
        return api_key

    # 2. 用户 openrouter.txt
    key_file = Path.home() / "文档" / "AI工具" / "openrouter.txt"
    if key_file.exists():
        return key_file.read_text().strip()

    # 3. ~/.openrouterrc
    rc_file = Path.home() / ".openrouterrc"
    if rc_file.exists():
        for line in rc_file.read_text().splitlines():
            if line.strip().startswith("OPENROUTER_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")

    return None


def load_models_from_cache(
    cache_path: Path = None,
    limit: int = 10,
    min_score: float = 0.0
) -> List[Dict]:
    """
    从 FreeRide 缓存加载优质免费模型列表

    Args:
        cache_path: 缓存文件路径
        limit: 最多返回多少个模型
        min_score: 最低分数（如果有_score字段）

    Returns:
        格式化后的模型列表，每个包含 'id' 键
    """
    if cache_path is None:
        cache_path = DEFAULT_CACHE_PATH

    if not cache_path.exists():
        logger = logging.getLogger(__name__)
        logger.warning(f"缓存文件不存在: {cache_path}")
        return []

    try:
        with open(cache_path, 'r', encoding='utf-8') as f:
            cache = json.load(f)

        models = cache.get("models", [])

        # 筛选和格式化
        formatted = []
        for m in models[:limit]:
            model_id = m.get("id", "")
            if not model_id:
                continue

            # 检查是否免费
            is_free = False
            pricing = m.get("pricing", {})
            prompt_cost = pricing.get("prompt")
            if prompt_cost is not None:
                try:
                    if float(prompt_cost) == 0:
                        is_free = True
                except (ValueError, TypeError):
                    pass
            if ":free" in model_id:
                is_free = True

            if not is_free:
                continue

            # 分数筛选（如果有）
            score = m.get("_score", 0)
            if score < min_score:
                continue

            formatted.append({
                "id": model_id,
                "name": m.get("name", model_id),
                "context_length": m.get("context_length", 0),
                "description": m.get("description", "")[:100],
                "score": score
            })

        logger = logging.getLogger(__name__)
        logger.info(f"从缓存加载了 {len(formatted)} 个模型")
        return formatted

    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"读取缓存失败: {e}")
        return []


def save_config(config: Dict, path: Path = CONFIG_PATH) -> None:
    """保存配置到 JSON 文件"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def load_config(path: Path = CONFIG_PATH) -> Optional[Dict]:
    """从 JSON 文件加载配置"""
    if not path.exists():
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None
