# API Documentation

# api_documentation_toolsz.md## Classes

### GitHubManager
一个将当前github仓库的提交历史打印出来的工具
获取可以用作它途

#### Methods
```python
def __init__(self):
```
No docstring provided.

```python
def get_origin(self):
```
No docstring provided.

```python
def generate_mermaid_git_graph(self, simulated_git_log):
```
# This is a simplified example. In a real scenario, you would run git log.
# Here we simulate the output of git log --all --graph --pretty=format:%h,%d,%s
# based on a simple history.

```python
def work(self):
```
运行

        

```python
def run(self):
```
运行

Returns:
    _type_: _description_

### AutoAPIMD
一个根据 Python 文件自动生成 API Markdown 文档的工具。

功能:
- 提取类、方法和函数的签名及文档字符串。
- 自动忽略以单下划线 `_` 开头的 "受保护" 成员。
- 保留以双下划线 `__` 开头的 "魔术" 成员。
- 在文档顶部生成文件路径和代码结构树。

使用示例:
input_file = 'path/to/your/python_file.py'
output_file = 'api_documentation.md'
AutoAPIMD().generate_api_docs(input_file, output_file)

#### Methods
```python
def __init__(self):
```
No docstring provided.

```python
def generate_tree_structure(self, file_path, classes, functions):
```
生成一个表示文件结构的最小化树状视图。

```python
def parse_python_file(self, file_path):
```
解析 Python 文件，提取类和函数的信息，包括注解和数据类型。

```python
def parse_function_or_method(self, node, kind):
```
解析函数或方法的详细信息，包括注解和数据类型。

```python
def generate_markdown(self, classes, functions, output_file, file_path, tree_string):
```
生成 Markdown API 文档，包含文件路径和结构树。

```python
def generate_api_docs(self, file_path, output_file):
```
生成 API 文档的主函数。

## Functions

```python
def struct():
```
装饰器, 主要是通过注解来严格校验输入与输出的格式, 推荐工程化时使用
    

```python
def safe_operation():
```
上下文方式的异常管理

```python
def package(fn, name: str, description: str):
```
将一般的函数打包成工具

Args:
    fn (function): 编写的函数
    name (str, optional): 函数名.
    description (str, optional): 函数描述. Defaults to None.

Returns:
    FunctionTool: functioncall

```python
def input_multiline():
```
解决某些时候换行代表enter 的情况

Returns:
    _type_: _description_

