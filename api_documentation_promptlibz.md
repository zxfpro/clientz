# API Documentation

## API for `/Users/zhaoxuefeng/GitHub/promptlibz/src/promptlibz/core.py`

### File Structure

```
core.py
├── class BaseManagedPrompt
│   ├── def __init__()
│   ├── def get_llama_prompt()
│   ├── def format()
│   └── def __str__()
├── class PromptRepository
│   ├── def __init__()
│   ├── def save_prompt()
│   ├── def load_prompt()
│   ├── def list_prompts()
│   ├── def delete_prompt_version()
│   └── def delete_prompt()
└── class PromptManager
    ├── def __init__()
    ├── def add_prompt()
    ├── def get_prompt()
    ├── def list_prompts()
    └── def remove_prompt()
```

## Classes

### `class BaseManagedPrompt`

管理 Prompt 的基类，包装 LlamaIndex 的 Prompt 对象。

#### Methods

```python
def __init__(self, name: str, version: str, description: str, template_content: str, base_class_name: str):
```
No docstring provided.

```python
def get_llama_prompt(self):
```
获取底层的 LlamaIndex Prompt 对象

```python
def format(self):
```
委托格式化操作给底层的 LlamaIndex Prompt

```python
def __str__(self):
```
No docstring provided.

### `class PromptRepository`

负责 Prompt 的文件系统存储和加载。

#### Methods

```python
def __init__(self, base_dir: str | None = None):
```
初始化prompt仓库

Args:
    base_dir (str | None, optional): 仓库地址. Defaults to None. 如果为None 则使用默认地址 /Users/zhaoxuefeng/GitHub/obsidian/Prompts

```python
def save_prompt(self, name: str, version: str, description: str, template_content: str, base_class_name: str):
```
保存 Prompt 版本

```python
def load_prompt(self, name: str, version: str) -> BaseManagedPrompt | None:
```
加载指定版本的 Prompt

```python
def list_prompts(self) -> dict[str, list[str]]:
```
列出所有 Prompt 及其版本

```python
def delete_prompt_version(self, name: str, version: str) -> bool:
```
删除指定版本的 Prompt

```python
def delete_prompt(self, name: str) -> bool:
```
删除 Prompt 的所有版本

### `class PromptManager`

提供 Prompt 管理的高级接口。

#### Methods

```python
def __init__(self, repository: PromptRepository):
```
No docstring provided.

```python
def add_prompt(self, name: str, version: str, description: str, template_content: str, base_class_name: str) -> bool:
```
添加或更新 Prompt 版本

```python
def get_prompt(self, name: str, version: str | None = None) -> BaseManagedPrompt | None:
```
获取 Prompt。如果未指定版本，则获取最新版本。

```python
def list_prompts(self) -> dict[str, list[str]]:
```
列出所有 Prompt 及其版本

```python
def remove_prompt(self, name: str, version: str | None = None) -> bool:
```
删除 Prompt 或指定版本

