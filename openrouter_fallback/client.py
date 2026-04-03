"""
OpenRouter Fallback Client - 智能多模型降级
"""

import json
import logging
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    import openai
except ImportError:
    raise ImportError("请先安装 openai 包: pip install openai")

logger = logging.getLogger(__name__)


class OpenRouterFallbackClient:
    """OpenRouter智能降级客户端"""

    def __init__(
        self,
        api_key: str,
        models: List[Dict] = None,
        max_retries: int = 3,
        retry_delay: float = 2.0,
        base_url: str = "https://openrouter.ai/api/v1"
    ):
        """
        初始化客户端

        Args:
            api_key: OpenRouter API密钥
            models: 模型列表，每个元素包含 'id' 字段
            max_retries: 每个模型最大重试次数
            retry_delay: 初始重试延迟（秒），指数退避
            base_url: OpenRouter API端点
        """
        self.api_key = api_key
        self.base_url = base_url
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.models = models or []

        # 初始化 OpenAI 客户端
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url
        )

        logger.info(f"OpenRouterFallbackClient 初始化，支持 {len(self.models)} 个模型")

    def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = 4000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        智能聊天，自动尝试多个模型直到成功

        Args:
            messages: 消息列表 [{"role": "user", "content": "..."}]
            model: 首选模型ID（可选）
            temperature: 温度参数 (0-2)
            max_tokens: 最大生成token数
            **kwargs: 其他参数（top_p, stream等）

        Returns:
            包含 response, model, usage 的成功字典，或包含 error 的失败字典
        """
        # 确定模型尝试顺序
        if model:
            models_to_try = [model] + [m["id"] for m in self.models if m["id"] != model]
        else:
            models_to_try = [m["id"] for m in self.models]

        if not models_to_try:
            return {"success": False, "error": "没有配置任何模型"}

        logger.info(f"将尝试以下模型顺序: {models_to_try}")
        last_error = None

        for attempt, model_id in enumerate(models_to_try, 1):
            logger.info(f"尝试模型 {attempt}/{len(models_to_try)}: {model_id}")

            for retry in range(1, self.max_retries + 1):
                try:
                    response = self.client.chat.completions.create(
                        model=model_id,
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        **kwargs
                    )

                    usage = response.usage
                    logger.info(
                        f"✅ 模型 {model_id} 成功 | "
                        f"Tokens: {usage.prompt_tokens}+{usage.completion_tokens}={usage.total_tokens}"
                    )

                    return {
                        "success": True,
                        "model": model_id,
                        "response": response.choices[0].message.content,
                        "usage": {
                            "prompt_tokens": usage.prompt_tokens,
                            "completion_tokens": usage.completion_tokens,
                            "total_tokens": usage.total_tokens
                        },
                        "finish_reason": response.choices[0].finish_reason
                    }

                except Exception as e:
                    error_str = str(e).lower()
                    last_error = e

                    # 判断是否可重试
                    if any(code in error_str for code in ["429", "rate limit", "quota", "502", "503", "504"]):
                        logger.warning(f"⚠️ 模型 {model_id} 重试 {retry}/{self.max_retries}: {e}")
                        if retry < self.max_retries:
                            time.sleep(self.retry_delay * (2 ** (retry - 1)))  # 指数退避
                            continue
                    else:
                        # 不可重试错误，立即切换下一个模型
                        logger.warning(f"❌ 模型 {model_id} 不可用: {e}")
                        break

            # 当前模型失败，继续下一个
            if attempt < len(models_to_try):
                logger.info(f"模型 {model_id} 失败，尝试下一个...")

        # 全部失败
        return {
            "success": False,
            "error": str(last_error) if last_error else "所有模型都失败",
            "models_tried": models_to_try
        }

    def stream_chat(
        self,
        messages: List[Dict[str, str]],
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = 4000,
        **kwargs
    ):
        """
        流式聊天，自动fallback到可用模型

        Yields:
            流式响应块: {"success": True, "model": str, "content": str, "finish_reason": str}
            或错误块: {"success": False, "error": str}
        """
        if model:
            models_to_try = [model] + [m["id"] for m in self.models if m["id"] != model]
        else:
            models_to_try = [m["id"] for m in self.models]

        logger.info(f"流式聊天将尝试: {models_to_try}")
        last_error = None

        for model_id in models_to_try:
            try:
                logger.info(f"流式连接模型: {model_id}")
                stream = self.client.chat.completions.create(
                    model=model_id,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=True,
                    **kwargs
                )

                for chunk in stream:
                    if chunk.choices and chunk.choices[0].delta.content:
                        yield {
                            "success": True,
                            "model": model_id,
                            "content": chunk.choices[0].delta.content,
                            "finish_reason": chunk.choices[0].finish_reason
                        }

                return  # 成功完成

            except Exception as e:
                last_error = e
                logger.warning(f"流式模型 {model_id} 失败: {e}")
                continue

        # 全部失败
        yield {
            "success": False,
            "error": str(last_error) if last_error else "所有流式模型都失败",
            "models_tried": models_to_try
        }
