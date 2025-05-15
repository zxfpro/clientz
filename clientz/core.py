import re
from typing import Dict, Any
from querypipz import Queryr
from llmada import BianXieAdapter

def format_node_for_chat(node_data: Dict[str, Any]) -> str:
    """
    解析节点数据，生成适合聊天窗口显示的格式化字符串。

    Args:
        node_data: 包含节点信息的字典结构。

    Returns:
        一个格式化的字符串，包含分数和节点文本内容。
        如果结构异常，返回错误提示。
    """
    node = node_data.get('node')
    score = node_data.get('score')

    if not node:
        return "Error: Could not find 'node' information."

    text_content = node.get('text')
    if not text_content:
        return "Error: 'text' content not found in node."

    # 移除 text 开头的 "topic:  content: \n\n\n" 或类似的元数据前缀
    # 根据你提供的样本，可能是固定的前缀，或者需要更灵活的处理
    # 这里简单移除已知的开头
    prefix_to_remove = "topic:  content: \n\n\n"
    if text_content.startswith(prefix_to_remove):
        text_content = text_content[len(prefix_to_remove):].strip()
    else:
         text_content = text_content.strip() # 或者只移除首尾空白

    # 构建输出字符串
    output = ""
    if score is not None:
        # 格式化分数，例如保留两位小数
        output += f"**Relevant Information (Score: {score:.2f})**:\n\n"
    else:
        output += "**Relevant Information:**\n\n"

    # 直接添加处理后的文本内容
    # 假设聊天窗口支持 Markdown，会渲染 #, ##, **, -, []() 等
    output += text_content

    # 你可以进一步处理 links，例如将它们提取出来单独列在末尾
    # link_pattern = re.compile(r'\[([^\]]+)\]\(([^\)]+)\)')
    # links_found = link_pattern.findall(text_content)
    # if links_found:
    #     output += "\n\n---\n*Links mentioned:*\n"
    #     for link_text, link_url in links_found:
    #         output += f"- [{link_text}]({link_url})\n" # 或其他格式

    return output


def show(xx):
    return xx.response +"\n\n"+ xx.get_formatted_sources()


ModelCards = ["gpt-4.1",
             "gemini-2.5-flash-preview-04-17-nothinking",
             "gemini-2.5-flash-preview-04-17-thinking",
             "query_origin",
             "query1"]

class ChatBox():
    def __init__(self) -> None:
        self.bx = BianXieAdapter()
        self.qur = Queryr(persist_dir='/Users/zhaoxuefeng/GitHub/test1/obsidian_kb/my_obsidian_notes')
        self.model_pool = ModelCards

    def product(self,prompt: str, model: str) -> str:
        if model in self.model_pool:
            self.bx.set_model(model)
            return self.bx.product(prompt)
        elif model == 'rag':
            result = self.qur.query(prompt)
            return show(result)
        elif model == 'work':
            formatted_output_string = ""
            for source in self.qur.retrieve(prompt):
                data = source.to_dict()
                formatted_output_string += format_node_for_chat(data)
                formatted_output_string += "\n########## --- ###########\n"
            result = formatted_output_string
            return result
        else:
            return 'pass'
    def stream_product(self,prompt: str, model: str) -> str:
        if model in self.model_pool:
            self.bx.set_model(model)
            for word in self.bx.product_stream(prompt):
                yield word
        elif model == 'work':
            formatted_output_string = ""
            for source in self.qur.retrieve(prompt):
                data = source.to_dict()
                formatted_output_string += format_node_for_chat(data)
                formatted_output_string += "\n########## --- ###########\n"
            result = formatted_output_string
            yield result
        else:
            yield 'pass'