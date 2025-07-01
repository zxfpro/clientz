# API Documentation

## API for `/Users/zhaoxuefeng/GitHub/appscriptz/src/appscriptz/core.py`

脚本交互

### File Structure

```
core.py
├── class Notes
│   └── def write()
├── class Reminder
│   └── def write_reminder()
├── class Calulate
│   ├── def update()
│   └── def delete()
├── class Display
│   ├── def multiple_selection_boxes()
│   ├── def get_multi_level_selection_simple()
│   └── def display_dialog()
├── class ShortCut
│   └── def run_shortcut()
├── def generate_schedule()
├── def run_applescript()
└── def applescript()
```

## Classes

### `class Notes`

No docstring provided.

#### Methods

```python
def write(content):
```
No docstring provided.

### `class Reminder`

No docstring provided.

#### Methods

```python
def write_reminder(content, list_name = 'Reminders', due_date = None, priority = None, notes = ''):
```
No docstring provided.

### `class Calulate`

No docstring provided.

#### Methods

```python
def update(start_date: str = '2025年4月25日8:00', end_date: str = '2025年4月25日9:00', event_name: str = '会议'):
```
No docstring provided.

```python
def delete(event_name: str):
```
No docstring provided.

### `class Display`

No docstring provided.

#### Methods

```python
def multiple_selection_boxes(prompt_text = '请从下面的列表中选择一项：', list_title = '请选择', options: list[str] = None, default_option: str = None):
```
使用 AppleScript 显示一个列表选择框，并返回用户的选择。

Args:
    prompt_text (str): 显示在列表上方的提示信息。
    list_title (str): 选择框窗口的标题。
    options (list): 供用户选择的字符串列表。
    default_option (str): 默认选中的项目。

Returns:
    str: 用户选择的项目。
    None: 如果用户取消或发生错误。

```python
def get_multi_level_selection_simple(warehouse_list: list, action_list: list) -> str:
```
【极简版】通过调用AppleScript在macOS上显示多层级UI对话框来收集用户输入。

此版本移除了所有错误处理。如果用户点击"取消"，脚本会失败。

:param warehouse_list: 字符串列表，用于仓库选择。
:param action_list: 字符串列表，用于动作类型选择。
:return: 格式为 "动作:仓库:标题:描述" 的字符串。

```python
def display_dialog(title, text, buttons = '"OK"', button_cancel = True):
```
使用 AppleScript 显示一个简单的对话框

### `class ShortCut`

No docstring provided.

#### Methods

```python
def run_shortcut(shortcut_name: str, params: str = None):
```
运行快捷指令

Args:
    shortcut_name (str, optional): 快捷指令名称. Defaults to ''.
    params (str, optional): 参数. Defaults to None.

Returns:
    str: 快捷指令的输出

## Functions

```python
def generate_schedule(text: str, habit: str = '') -> str:
```
使用 GPT 模型生成日程安排
:param text: 输入文本
:return: 生成的日程安排结果

```python
def run_applescript(script: str) -> str:
```
运行apple script 脚本

Args:
    script (str): applescript 脚本

Returns:
    str: 脚本的输出

```python
def applescript():
```
https://sspai.com/post/46912

https://sspai.com/post/43758

