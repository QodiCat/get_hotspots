import requests
import json
from functools import wraps
from datetime import datetime
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def token_counter(func):
    """
    装饰器：统计token使用情况
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        start_time = datetime.now()
        
        # 调用原函数
        result = func(self, *args, **kwargs)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # 提取token使用信息
        if result and isinstance(result, dict) and 'usage' in result:
            usage = result['usage']
            prompt_tokens = usage.get('prompt_tokens', 0)
            completion_tokens = usage.get('completion_tokens', 0)
            total_tokens = usage.get('total_tokens', 0)
            
            # 记录到实例的统计信息中
            if not hasattr(self, 'token_stats'):
                self.token_stats = {
                    'total_calls': 0,
                    'total_prompt_tokens': 0,
                    'total_completion_tokens': 0,
                    'total_tokens': 0,
                    'total_duration': 0,
                    'call_history': []
                }
            
            # 更新统计信息
            self.token_stats['total_calls'] += 1
            self.token_stats['total_prompt_tokens'] += prompt_tokens
            self.token_stats['total_completion_tokens'] += completion_tokens
            self.token_stats['total_tokens'] += total_tokens
            self.token_stats['total_duration'] += duration
            
            # 记录本次调用信息
            call_info = {
                'timestamp': start_time.isoformat(),
                'function': func.__name__,
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': total_tokens,
                'duration': duration
            }
            self.token_stats['call_history'].append(call_info)
            
            # 日志输出
            logger.info(f"API调用统计 - 函数: {func.__name__}, "
                       f"输入tokens: {prompt_tokens}, 输出tokens: {completion_tokens}, "
                       f"总tokens: {total_tokens}, 耗时: {duration:.2f}秒")
        
        return result
    
    return wrapper

class DeepSeekAPI:
    def __init__(self, api_key, system_prompt="你是一个有帮助的助手"):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.system_prompt = system_prompt
        self.token_stats = {
            'total_calls': 0,
            'total_prompt_tokens': 0,
            'total_completion_tokens': 0,
            'total_tokens': 0,
            'total_duration': 0,
            'call_history': []
        }
    
    def ai_response(self, prompt, model="deepseek-chat", temperature=0.7, max_tokens=4000, system_prompt=None):
        """
        获取AI回复（只返回内容文本）
        
        Args:
            prompt (str): 用户输入的提示
            model (str): 模型名称
            temperature (float): 温度参数
            max_tokens (int): 最大生成token数
            system_prompt (str): 系统提示（可选）
            
        Returns:
            str: AI回复的文本内容
        """
        if system_prompt is None:
            system_prompt = self.system_prompt
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        response = self.chat_completion(messages, model, temperature, max_tokens)
        
        if response and 'choices' in response:
            return response["choices"][0]["message"]["content"]
        return None
    
    @token_counter
    def chat_completion(self, messages, model="deepseek-chat", temperature=0.7, max_tokens=4000):
        """
        调用DeepSeek聊天完成API（返回完整响应）
        
        Args:
            messages (list): 对话消息列表
            model (str): 模型名称
            temperature (float): 温度参数，控制输出的随机性
            max_tokens (int): 最大生成token数
            
        Returns:
            dict: API完整响应结果，包含token使用信息
        """
        endpoint = f"{self.base_url}/chat/completions"
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API调用出错: {str(e)}")
            return None
    
    def get_token_stats(self):
        """
        获取token使用统计信息
        
        Returns:
            dict: 包含详细统计信息的字典
        """
        stats = self.token_stats.copy()
        if stats['total_calls'] > 0:
            stats['avg_prompt_tokens'] = stats['total_prompt_tokens'] / stats['total_calls']
            stats['avg_completion_tokens'] = stats['total_completion_tokens'] / stats['total_calls']
            stats['avg_total_tokens'] = stats['total_tokens'] / stats['total_calls']
            stats['avg_duration'] = stats['total_duration'] / stats['total_calls']
        else:
            stats['avg_prompt_tokens'] = 0
            stats['avg_completion_tokens'] = 0
            stats['avg_total_tokens'] = 0
            stats['avg_duration'] = 0
        
        return stats
    
    def print_token_stats(self):
        """
        打印token使用统计信息
        """
        stats = self.get_token_stats()
        print(f"\n=== DeepSeek API Token 使用统计 ===")
        print(f"总调用次数: {stats['total_calls']}")
        print(f"总输入tokens: {stats['total_prompt_tokens']}")
        print(f"总输出tokens: {stats['total_completion_tokens']}")
        print(f"总tokens: {stats['total_tokens']}")
        print(f"总耗时: {stats['total_duration']:.2f}秒")
        if stats['total_calls'] > 0:
            print(f"平均输入tokens: {stats['avg_prompt_tokens']:.1f}")
            print(f"平均输出tokens: {stats['avg_completion_tokens']:.1f}")
            print(f"平均总tokens: {stats['avg_total_tokens']:.1f}")
            print(f"平均耗时: {stats['avg_duration']:.2f}秒")
        print("=" * 35)
    
    def reset_token_stats(self):
        """
        重置token统计信息
        """
        self.token_stats = {
            'total_calls': 0,
            'total_prompt_tokens': 0,
            'total_completion_tokens': 0,
            'total_tokens': 0,
            'total_duration': 0,
            'call_history': []
        }
        logger.info("Token统计信息已重置")

def main():
    # 示例用法
    api_key = "your_api_key_here"  
    deepseek = DeepSeekAPI(api_key)
    
    # 测试基本聊天
    response = deepseek.ai_response("你好，请介绍一下你自己。")
    if response:
        print(f"AI回复: {response}")
    
    # 测试完整API调用
    messages = [
        {"role": "system", "content": "你是一个有帮助的AI助手。"},
        {"role": "user", "content": "解释一下什么是机器学习。"}
    ]
    
    full_response = deepseek.chat_completion(messages)
    if full_response:
        print(f"\n完整响应: {json.dumps(full_response, ensure_ascii=False, indent=2)}")
    
    # 打印统计信息
    deepseek.print_token_stats()

if __name__ == "__main__":
    main() 