import json

def read_json_file(file_path,version=None):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # 获取system_prompt中"0"键对应的值
            if version is None:
                value = data['system_prompt']['0']
            else:
                value = data['system_prompt'][version]
            return value
    except FileNotFoundError:
        print(f"错误：找不到文件 {file_path}")
    except json.JSONDecodeError:
        print("错误：JSON文件格式不正确")
    except KeyError:
        print("错误：找不到指定的键")

if __name__ == "__main__":
    # 使用相对路径读取JSON文件
    file_path = "agent_prompt/big_character_poster/plan_style_agent.json"
    read_json_file(file_path) 