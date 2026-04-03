"""
命令行接口：or-auto
"""

import argparse
import json
import logging
import sys
from pathlib import Path

from .client import OpenRouterFallbackClient
from .utils import get_api_key, load_models_from_cache

# 默认模型列表（当缓存不可用时使用）
DEFAULT_MODELS = [
    {"id": "qwen/qwen3.6-plus:free", "priority": 1},
    {"id": "nvidia/nemotron-3-super-120b-a12b:free", "priority": 2},
    {"id": "nvidia/nemotron-3-nano-30b-a3b:free", "priority": 3},
    {"id": "stepfun/step-3.5-flash:free", "priority": 4},
    {"id": "qwen/qwen3-coder:free", "priority": 5},
    {"id": "nvidia/nemotron-nano-9b-v2:free", "priority": 6},
    {"id": "nvidia/nemotron-nano-12b-v2-vl:free", "priority": 7},
    {"id": "qwen/qwen3-next-80b-a3b-instruct:free", "priority": 8},
    {"id": "arcee-ai/trinity-mini:free", "priority": 9},
    {"id": "meta-llama/llama-3.2-3b-instruct:free", "priority": 10},
]

def main():
    parser = argparse.ArgumentParser(
        prog="or-auto",
        description="OpenRouter Fallback - 智能多模型降级客户端"
    )
    parser.add_argument("prompt", nargs="*", help="要问的问题（如果不提供则进入交互模式）")
    parser.add_argument("--model", help="首选模型ID")
    parser.add_argument("--temp", type=float, default=0.7, help="温度参数 (0-2)")
    parser.add_argument("--tokens", type=int, default=4000, help="最大token数")
    parser.add_argument("--list-models", action="store_true", help="列出推荐模型")
    parser.add_argument("--test", action="store_true", help="测试连接")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细日志")

    args = parser.parse_args()

    # 配置日志
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # 获取API密钥
    api_key = get_api_key()
    if not api_key and not args.list_models:
        print("❌ 未找到OPENROUTER_API_KEY")
        print("请设置环境变量或创建 ~/文档/AI工具/openrouter.txt")
        sys.exit(1)

    # 加载模型列表
    models = load_models_from_cache()
    if not models:
        models = DEFAULT_MODELS
        print("⚠️ 使用内置默认模型列表（缓存不可用）")

    # --list-models
    if args.list_models:
        print("\n📋 推荐模型列表（按优先级，共10个）:")
        print("-" * 80)
        for i, m in enumerate(models[:10], 1):
            ctx = m.get('context_length', '?')
            desc = m.get('description', '')[:50]
            print(f"{i:2d}. {m['id']}")
            print(f"    上下文: {ctx} tokens")
            if desc:
                print(f"    描述: {desc}...")
        sys.exit(0)

    # --test
    if args.test:
        print("🧪 测试OpenRouter连接...")
        try:
            client = OpenRouterFallbackClient(api_key, models)
            result = client.chat(
                messages=[{"role": "user", "content": "测试成功，请回复OK"}],
                max_tokens=50
            )
            if result["success"]:
                print(f"\n✅ 测试成功！模型: {result['model']}")
                print(f"响应: {result['response'][:50]}")
                print(f"Token: {result['usage']}")
                sys.exit(0)
            else:
                print(f"\n❌ 测试失败: {result['error']}")
                sys.exit(1)
        except Exception as e:
            print(f"❌ 客户端错误: {e}")
            sys.exit(1)

    # 处理prompt
    if not args.prompt:
        print("💡 交互模式（输入 'quit' 或 'exit' 退出）")
        while True:
            try:
                prompt = input("\n❓ 你: ").strip()
                if prompt.lower() in ('quit', 'exit', 'q'):
                    break
                if not prompt:
                    continue
                run_query(prompt, api_key, models, args)
            except (KeyboardInterrupt, EOFError):
                break
    else:
        prompt = " ".join(args.prompt)
        result = run_query(prompt, api_key, models, args)
        sys.exit(0 if result["success"] else 1)


def run_query(prompt: str, api_key: str, models: list, args):
    """执行单次查询"""
    client = OpenRouterFallbackClient(api_key, models)

    print(f"\n🤖 思考中... (首选: {args.model or models[0]['id']})")
    print(f"📝 {prompt[:80]}...\n")

    result = client.chat(
        messages=[{"role": "user", "content": prompt}],
        model=args.model,
        temperature=args.temp,
        max_tokens=args.tokens
    )

    if result["success"]:
        print(f"✅ 模型: {result['model']}")
        print(f"📊 Token: {result['usage']['total_tokens']}")
        print("\n" + "=" * 80 + "\n")
        print(result["response"])
        return result
    else:
        print(f"❌ 失败: {result['error']}")
        print(f"尝试过的: {result.get('models_tried', [])}")
        return result


if __name__ == "__main__":
    main()
