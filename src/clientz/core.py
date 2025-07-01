""" core 需要修改"""
import re
import os
import time
from contextlib import contextmanager
import importlib.resources
from typing import Dict, Any
import yaml
from llmada import BianXieAdapter
from querypipz import BuilderFactory,BuilderType,Director
from agentflowz.main import AgentFactory,AgentType,EasyAgentz
from toolsz.dev import AutoAPIMD

from .log import Log
logger = Log.logger
logger_path = 'logs/querypipz.log'

""" config.yaml
query_persist_dir: /Users/zhaoxuefeng/GitHub/test1/obsidian_kb/my_obsidian_notes
WORK_CANVAS_PATH:
- /工程系统级设计/能力级别/人体训练设计/人体训练设计.canvas
ModelCards:
- gpt-4.1
- cus-gemini-2.5-flash-preview-04-17-nothinking
- cus-gemini-2.5-flash-preview-04-17-thinking
Custom:
- config_info
- chat_with_long_memory_v2
- long_memory_v2_retriver
- chat_with_Agent_notes
- Custom_Agent_Latest
- Experts_V1
"""



LLM_INFO = {
"query_persist_dir": "/Users/zhaoxuefeng/GitHub/test1/obsidian_kb/my_obsidian_notes",
"WORK_CANVAS_PATH": [
"/工程系统级设计/能力级别/人体训练设计/人体训练设计.canvas"
],
"ModelCards": [
    "gpt-4.1",
    "cus-gemini-2.5-flash-preview-04-17-nothinking",
    "cus-gemini-2.5-flash-preview-04-17-thinking"
],
"Custom": [
            "config_info",
            "logger_info",
            "chat_with_long_memory_v2",
            "long_memory_v2_retriver",
            "chat_with_Agent_notes",
            "Custom_Agent_Latest",
            "Experts_V1",
            "llmada_expert",
            "canvaz_expert",
            "kanbanz_expert",
            "appscriptz_expert",
            "toolsz_expert",
            "mermaidz_expert",
            "promptlibz_expert",
        ]
}



def load_config():
    """ load config """
    with importlib.resources.open_text('clientz', 'config.yaml') as f:
        return yaml.safe_load(f)

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

def extract_last_user_input(dialogue_text):
    """
    从多轮对话文本中提取最后一个 user 的输入内容。

    Args:
        dialogue_text: 包含多轮对话的字符串。

    Returns:
        最后一个 user 的输入内容字符串，如果未找到则返回 None。
    """
    # 修正后的正则表达式
    # (?s) 标志：使 . 匹配换行符
    # .* 匹配任意字符，直到最后一个 user:
    # user:\s* 匹配 "user:" 后面的零个或多个空白字符
    # (.*?) 非贪婪匹配任意字符，直到下一个 user: 或字符串末尾
    # (?=user:|$) 正向先行断言：断言后面是 "user:" 或者字符串末尾
    pattern = r"(?s).*user:\s*(.*?)(?=user:|$)"

    match = re.search(pattern, dialogue_text)

    if match:
        # group(1) 捕获的是最后一个 user: 到下一个 user: 或字符串末尾的内容
        return match.group(1).strip()
    else:
        return None




@contextmanager
def check_time(title:str,logger):
    """ try catch"""
    time1 = time.time()
    yield
    time2 = time.time()
    logger.debug(f"{title}: {time2-time1}")

    

def extra_docs(inputs:str)->dict:
    """ docs """
    pattern1 = r'<context>(.*?)<\/context>'
    pattern2 = r'<source id="(\d+)">(.*?)<\/source>'

    match = re.search(pattern1, inputs,re.DOTALL)

    if match:
        sources = match.group(1).strip()
        matches = re.findall(pattern2, sources)

    result = {int(id): content for id, content in matches}
    return result


class ChatBox():
    """ chatbox """
    def __init__(self) -> None:
        self.bx = BianXieAdapter()
        # self.dicts = load_config()
        self.dicts = LLM_INFO
        self.query_persist_dir = self.dicts.get('query_persist_dir')
        self.model_pool = self.dicts.get("ModelCards")
        self.file_path = 'clientz/config.yaml'
        self._last_modified_time = None
        self._update_last_modified_time()
        self.init_lazy_parameter()
        self.query = None

    def _update_last_modified_time(self):
        """更新存储的最后修改时间"""
        try:
            self._last_modified_time = os.path.getmtime(self.file_path)
        except FileNotFoundError:
            self._last_modified_time = None # 文件不存在时设为None

    def check_and_trigger(self):
        """检查文件是否变化，如果变化则触发动作"""
        try:
            current_modified_time = os.path.getmtime(self.file_path)
            if current_modified_time != self._last_modified_time:
                print(f"文件 '{self.file_path}' 已发生变化。")
                self._trigger_action()
                self._last_modified_time = current_modified_time # 更新存储的时间
            else:
                print(f"文件 '{self.file_path}' 未发生变化。")
        except FileNotFoundError:
            print(f"文件 '{self.file_path}' 不存在。")
            self._last_modified_time = None # 文件不存在时重置状态
        except Exception as e:
            print(f"检查文件时发生错误: {e}")

    def _trigger_action(self):
        """当文件发生变化时触发的动作"""
        # 可以修改
        # 这里可以放置你想要执行的具体动作，例如：
        # - 读取文件内容
        # - 处理文件数据
        # - 调用其他函数
        print("触发预定动作...")
        # 示例：读取文件内容并打印
        try:
            self.dicts = load_config()

        except FileNotFoundError:
            print(f"触发动作时文件 '{self.file_path}' 不存在。")
        except Exception as e:
            print(f"读取文件时发生错误: {e}")

    def product(self,prompt_with_history: str, model: str) -> str:
        """ x """
        prompt_with_history, model
        return ''

    def init_lazy_parameter(self):
        """ 一个懒加载的初始化头部 """
        self.chat_with_agent_notes_object = None


    async def astream_product(self,prompt_with_history: str, model: str) -> Any:
        """
        # 只需要修改这里
        """
        self.check_and_trigger()
        prompt_no_history = extract_last_user_input(prompt_with_history)
        logger.debug(f"# prompt_no_history : {prompt_no_history}")
        logger.debug(f"# prompt_with_history : {prompt_with_history}")
        ## __init__ ##

        if model[4:] in self.model_pool:
            self.bx.set_model(model[4:])
            for word in self.bx.product_stream(prompt_with_history):
                yield word

        elif model == "config_info":
            logger.info(f"running {model}")
            yield f"query_dir: {self.query_persist_dir}, dicts {str(self.dicts)}"

            if self.chat_with_agent_notes_object:
                yield self.chat_with_agent_notes_object.tool_calls()

        elif model == "logger_info":
            logger.info(f"running {model}")
            with open(logger_path,'r') as f:
                text = f.read()
            yield text[-10000:]


        elif model == "llmada_expert":
            input_file = '/Users/zhaoxuefeng/GitHub/llmada/src/llmada/core.py'  # 替换为你的 Python 文件路径
            output_file = 'api_documentation_llmada.md'
            api_doc = AutoAPIMD().generate_api_docs(input_file, output_file)
            logger.debug(f'api_doc:{api_doc}')
            # api_doc = "# API Documentation\n\n## Classes\n\n### ResourceExhaustedError\nRaised when a resource's quota has been exceeded.\n\n#### Methods\n```python\ndef __init__(self, message):\n```\nNo docstring provided.\n\n### ModelAdapter\n语言大模型的抽象类\n\n    \n\n#### Methods\n```python\ndef __init__(self):\n```\nNo docstring provided.\n\n```python\ndef set_model(self, model_name: str):\n```\n实例化以后用以修改调用的模型, 要求该模型存在于 model_pool 中\n\nArgs:\n    model_name (str): _description_\n\n```python\ndef set_temperature(self, temperature: float):\n```\n用于设置模型的temperature\n\nArgs:\n    temperature (float): model temperature\n\n```python\ndef get_model(self) -> list[str]:\n```\n获得当前的 model_pool\n\nReturns:\n    list[str]: models\n\n```python\ndef product(self, prompt: str) -> str:\n```\n子类必须实现的类, 用于和大模型做非流式交互\n\nArgs:\n    prompt (str): 提示词\n\nRaises:\n    NotImplementedError: pass\n\nReturns:\n    str: 大模型返回的结果\n\n```python\ndef chat(self, messages: list) -> str:\n```\n子类必须实现的类, 用于和大模型做聊天交互\n\nReturns:\n    str: 大模型返回的结果\n\n### ModelModalAdapter\nNo docstring provided.\n\n#### Methods\n```python\ndef get_modal_model(self):\n```\n获取支持多模态的模型列表\n\nRaises:\n    NotImplementedError: _description_\n\n```python\ndef product_modal(self, prompt: RichPromptTemplate) -> str:\n```\n提供多模态的非流式交流\n\nArgs:\n    prompt (RichPromptTemplate): llama-index 的富文本格式\n\nReturns:\n    str: _description_\n\n### BianXieAdapter\nBianXie格式的适配器\n    \n\n#### Methods\n```python\ndef __init__(self, api_key: str, api_base: str):\n```\n初始化\n正常情况下, 这两个参数都不需要传入, 而是会自动寻找环境变量,除非要临时改变api_key.\n    api_base 不需要特别指定\nArgs:\n    api_key (str): API key for authentication.\n    api_base (str): Base URL for the API endpoint.\n\n```python\ndef get_modal_model(self) -> list[str]:\n```\n返回多模态模型池\n\nReturns:\n    list[str]: 大量模型的字符串名称列表\n\n```python\ndef product_modal(self, prompt: RichPromptTemplate) -> str:\n```\nNo docstring provided.\n\n```python\ndef _deal_response(self, response):\n```\n处理事件的相应\n\n```python\ndef product(self, prompt: str) -> str:\n```\nGenerate a response from the model based on a single prompt.\n\nArgs:\n    prompt (str): The input text prompt to generate a response for.\n\nReturns:\n    str: The response generated by the model.\n\n```python\ndef _assert_prompt(self, prompt):\n```\nNo docstring provided.\n\n```python\ndef product_stream(self, prompt: str) -> str:\n```\nGenerate a response from the model based on a single prompt.\n\nArgs:\n    prompt (str): The input text prompt to generate a response for.\n\nReturns:\n    str: The response generated by the model.\n\n```python\ndef chat(self, messages: list) -> str:\n```\nEngage in a conversation with the model using a list of messages.\n\nArgs:\n    messages (list): A list of message dictionaries, each containing a role and content.\n\nReturns:\n    str: The response generated by the model for the conversation.\n\n```python\ndef chat_stream(self, messages: list) -> str:\n```\nEngage in a conversation with the model using a list of messages.\n\nArgs:\n    messages (list): A list of message dictionaries, each containing a role and content.\n\nReturns:\n    str: The response generated by the model for the conversation.\n\n```python\ndef chat_stream_history(self, prompt: str, system: str) -> str:\n```\nEngage in a conversation with the model using a list of messages.\n\nArgs:\n    messages (list): A list of message dictionaries, each containing a role and content.\n\nReturns:\n    str: The response generated by the model for the conversation.\n\n### ArkAdapter\nNo docstring provided.\n\n#### Methods\n```python\ndef __init__(self, api_key: str, api_base: str):\n```\n初始化\n\nArgs:\n    api_key (str): API key for authentication.\n    api_base (str): Base URL for the API endpoint.\n\n```python\ndef product(self, prompt: str) -> str:\n```\nGenerate a response from the model based on a single prompt.\n\nArgs:\n    prompt (str): The input text prompt to generate a response for.\n\nReturns:\n    str: The response generated by the model.\n\n```python\ndef chat(self, messages: list) -> str:\n```\nEngage in a conversation with the model using a list of messages.\n\nArgs:\n    messages (list): A list of message dictionaries, each containing a role and content.\n\nReturns:\n    str: The response generated by the model for the conversation.\n\n### GoogleAdapter\nNo docstring provided.\n\n#### Methods\n```python\ndef __init__(self, api_key: str):\n```\n初始化\n\nArgs:\n    api_key (str): API key for authentication.\n\n```python\ndef product(self, prompt: str) -> str:\n```\nGenerate a response from the model based on a single prompt.\n\nArgs:\n    prompt (str): The input text prompt to generate a response for.\n\nReturns:\n    str: The response generated by the model.\n\n```python\ndef chat(self, messages: list) -> str:\n```\nEngage in a conversation with the model using a list of messages.\n\nArgs:\n    messages (list): A list of message dictionaries, each containing a role and content.\n\nReturns:\n    str: The response generated by the model for the conversation.\n\n### KimiAdapter\nKimi格式的适配器\n\n    \n\n#### Methods\n```python\ndef __init__(self, api_key: str, api_base: str):\n```\n初始化\n\nArgs:\n    api_key (str): API key for authentication.\n    api_base (str): Base URL for the API endpoint.\n\n```python\ndef product(self, prompt: str) -> str:\n```\nGenerate a response from the model based on a single prompt.\n\nArgs:\n    prompt (str): The input text prompt to generate a response for.\n\nReturns:\n    str: The response generated by the model.\n\n```python\ndef chat(self, messages: list) -> str:\n```\nEngage in a conversation with the model using a list of messages.\n\nArgs:\n    messages (list): A list of message dictionaries, each containing a role and content.\n\nReturns:\n    str: The response generated by the model for the conversation.\n\n"
            system_prompt = f"""
            以下是软件包llmada 的api文档, 请有限使用该包完成用户的问题
            API_DOCUMENT:

            {api_doc}
            ---

            """
            prompt = system_prompt + prompt_with_history
            for word in self.bx.product_stream(prompt):
                yield word

        elif model == "canvaz_expert":
            input_file = '/Users/zhaoxuefeng/GitHub/canvaz/src/canvaz/core.py'  # 替换为你的 Python 文件路径
            output_file = 'api_documentation_canvaz.md'
            api_doc = AutoAPIMD().generate_api_docs(input_file, output_file)
            logger.debug(f'api_doc:{api_doc}')
            assert api_doc is not None
            system_prompt = f"""
            以下是软件包canvaz 的api文档, 请有限使用该包完成用户的问题
            API_DOCUMENT:

            {api_doc}
            ---

            """
            prompt = system_prompt + prompt_with_history
            for word in self.bx.product_stream(prompt):
                yield word

        elif model == "kanbanz_expert":
            input_file = '/Users/zhaoxuefeng/GitHub/kanbanz/src/kanbanz/core.py'  # 替换为你的 Python 文件路径
            output_file = 'api_documentation_kanbanz.md'
            api_doc = AutoAPIMD().generate_api_docs(input_file, output_file)
            assert api_doc is not None
            logger.debug(f'api_doc:{api_doc}')
            system_prompt = f"""
            以下是软件包kanbanz 的api文档, 请有限使用该包完成用户的问题
            API_DOCUMENT:

            {api_doc}
            ---

            """
            prompt = system_prompt + prompt_with_history
            for word in self.bx.product_stream(prompt):
                yield word

        elif model == "appscriptz_expert":
            input_file = '/Users/zhaoxuefeng/GitHub/appscriptz/src/appscriptz/core.py'  
            output_file = 'api_documentation_appscriptz.md'
            api_doc = AutoAPIMD().generate_api_docs(input_file, output_file)
            assert api_doc is not None
            logger.debug(f'api_doc:{api_doc}')
            system_prompt = f"""
            以下是软件包appscriptz 的api文档, 请有限使用该包完成用户的问题
            API_DOCUMENT:

            {api_doc}
            ---

            """
            prompt = system_prompt + prompt_with_history
            for word in self.bx.product_stream(prompt):
                yield word

        elif model == "toolsz_expert":
            input_file = '/Users/zhaoxuefeng/GitHub/toolsz/src/toolsz/dev.py'  # 替换为你的 Python 文件路径
            output_file = 'api_documentation_toolsz.md'
            input_file2 = '/Users/zhaoxuefeng/GitHub/toolsz/src/toolsz/freedom_function.py'  # 替换为你的 Python 文件路径
            output_file2 = 'api_documentation_toolsz2.md'
            api_doc = AutoAPIMD().generate_api_docs(input_file, output_file)
            api_doc2 = AutoAPIMD().generate_api_docs(input_file2, output_file2)

            assert api_doc is not None
            assert api_doc2 is not None
            logger.debug(f'api_doc:{api_doc}')
            logger.debug(f'api_doc2:{api_doc2}')
            system_prompt = f"""
            以下是软件包toolsz 的api文档, 请有限使用该包完成用户的问题
            API_DOCUMENT:

            {api_doc}

            {api_doc2}
            ---

            """
            prompt = system_prompt + prompt_with_history
            for word in self.bx.product_stream(prompt):
                yield word

        elif model == "mermaidz_expert":
            input_file = '/Users/zhaoxuefeng/GitHub/mermaidz/src/mermaidz/core.py'  # 替换为你的 Python 文件路径
            output_file = 'api_documentation_mermaidz.md'
            api_doc = AutoAPIMD().generate_api_docs(input_file, output_file)
            assert api_doc is not None
            logger.debug(f'api_doc:{api_doc}')
            system_prompt = f"""
            以下是软件包mermaidz 的api文档, 请有限使用该包完成用户的问题
            API_DOCUMENT:

            {api_doc}
            ---

            """
            prompt = system_prompt + prompt_with_history
            for word in self.bx.product_stream(prompt):
                yield word


        elif model == "promptlibz_expert":
            input_file = '/Users/zhaoxuefeng/GitHub/promptlibz/src/promptlibz/core.py'  # 替换为你的 Python 文件路径
            output_file = 'api_documentation_promptlibz.md'
            api_doc = AutoAPIMD().generate_api_docs(input_file, output_file)
            logger.debug(f'api_doc:{api_doc}')
            
            assert api_doc is not None
            system_prompt = f"""
            以下是软件包promptlibz 的api文档, 请有限使用该包完成用户的问题

            API_DOCUMENT:

            {api_doc}
            ---

            """
            prompt = system_prompt + prompt_with_history
            for word in self.bx.product_stream(prompt):
                yield word



        elif model == "long_memory_v2_retriver":
            if not self.query:
                director = Director(BuilderFactory(BuilderType.CHAT_HISTORY_MEMORY_BUILDER))
                self.query = director.construct()
            if len(prompt_with_history.split('\n')) == 1:
                self.query.reload()

            relevant_memories = self.query.retrieve_search(prompt_no_history)
            memories_str = '\n'.join([i.metadata.get('docs') for i in relevant_memories])
            yield memories_str

        elif model == 'chat_with_long_memory_v2':
            """
            # 电脑 内存就是对应chat_history
            # 硬盘 + 内置硬盘 其实就是 大模型潜意识与知识库维度
            # 还要再加一些 寄存器的方式
            """
            logger.info(f"running {model}")

            self.bx.set_model("gemini-2.5-flash-preview-04-17-nothinking")
            system_prompt = ""
            if not self.query:
                director = Director(BuilderFactory(BuilderType.CHAT_HISTORY_MEMORY_BUILDER))
                self.query = director.construct()
            if len(prompt_with_history.split('\n')) == 1:
                self.query.reload()

            if prompt_no_history.startswith("上传记忆"):
                import datetime
                now = datetime.datetime.now()
                date_str_ymd = now.strftime("%Y-%m-%d %H:%M:%S")  # 年-月-日
                #TODO 安装最新版后更新
                # 上传记忆${'tags':"成功",'date':"date_str_ymd"}
                self.query.update(prompt_with_history,metadata = {"tags":'合格',"date":date_str_ymd})
                yield '上传完成'
            elif prompt_no_history.startswith('上传文章'):
                context = f"user: {prompt_no_history}\nassistant: 上传完成"
                print(context,'contextxxxxxxxx')
                self.query.update(context)
                yield '上传完成'
            else:
                with check_time("retriver_search_time",logger = logger):
                    relevant_memories = self.query.retrieve_search(prompt_no_history)
                    memories_str = '\n'.join([i.metadata.get('docs') for i in relevant_memories])
                    prompt = system_prompt +"\n"+ memories_str +"\n"+prompt_with_history
                time1 = time.time()
                for word in self.bx.product_stream(prompt):
                    logger.debug(f"first_tokens_time: {time.time()-time1}")
                    yield word

        elif model == 'Experts_V1':
            logger.info(f"running {model}")

            doc_dict = extra_docs(prompt_with_history)

            if not self.chat_with_agent_notes_object:
                agent = AgentFactory(AgentType.ReactAgent,tools = [take_notes,read_notes])

                agt = EasyAgentz(agent)
                self.chat_with_agent_notes_object = agt

            result = await self.chat_with_agent_notes_object.run(prompt_no_history)
            yield result


        elif model == 'chat_with_Agent_notes':
            logger.info(f"running {model}")

            def take_notes(text: str) -> None:
                """Some important contents can be recorded"""
                with open('notes.txt','a',encoding="utf-8") as f:
                    f.write(text)

            def read_notes() -> str:
                """Read the important contents that were once recorded"""
                with open('notes.txt','r',encoding="utf-8") as f:
                    text = f.read()
                return text

            if not self.chat_with_agent_notes_object:
                agent = AgentFactory(AgentType.ReactAgent,tools = [take_notes,read_notes])

                agt = EasyAgentz(agent)
                self.chat_with_agent_notes_object = agt

            result = await self.chat_with_agent_notes_object.run(prompt_no_history)
            yield result

        elif model == 'Custom_Agent_Latest':
            logger.info(f"running {model}")


            def take_notes(text: str) -> None:
                """Some important contents can be recorded"""
                with open('notes.txt','a',encoding="utf-8") as f:
                    f.write(text)

            def read_notes() -> str:
                """Read the important contents that were once recorded"""
                with open('notes.txt','r',encoding="utf-8") as f:
                    text = f.read()
                return text

            logger.debug('############# prompt_with_history #############')
            logger.debug(prompt_with_history)
            logger.debug('############# prompt_no_history #############')

            if not self.chat_with_agent_notes_object:
                agent = AgentFactory(AgentType.ReactAgent,tools = [take_notes,read_notes])

                agt = EasyAgentz(agent)
                self.chat_with_agent_notes_object = agt

            result = await self.chat_with_agent_notes_object.run(prompt_no_history)
            yield result

        else:
            yield 'pass'
