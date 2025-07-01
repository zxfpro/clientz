# API Documentation

## API for `/Users/zhaoxuefeng/GitHub/kanbanz/src/kanbanz/core.py`

用Obsidian做KanBan管理, 本质是特殊格式的Markdown文件, 可视作KanBan的SDK

### File Structure

```
core.py
├── class Pool(Enum)
├── class Kanban
│   ├── def __init__()
│   ├── def pull()
│   ├── def push()
│   ├── def insert()
│   ├── def pop()
│   ├── def get_tasks_in()
│   └── def get_task_by_word()
└── class KanBanManager
    ├── def __init__()
    ├── def sync_ready()
    ├── def sync_order()
    └── def sync_run()
```

## Classes

### `class Pool(Enum)`

任务池类型枚举类。

用于标识任务在看板中的不同状态池，包括：
    - 预备池：任务尚未准备好进入流程,是一个任务的集中地.
    - 就绪池：任务已准备好，添加了一些任务必要的信息,可以开始执行。
    - 阻塞池：任务因某些原因被阻塞，暂时无法继续。
    - 执行池：正在进行中的任务。
    - 完成池：已完成的任务。
    - 酱油池：无关紧要或暂时搁置的任务。

Args:
    Enum (enum.Enum): 枚举基类，用于定义一组常量。

### `class Kanban`

看板管理SDK

#### Methods

```python
def __init__(self, kanban_path: str):
```
初始化 Kanban 实例。

Args:
    kanban_path (str): 看板文件的路径。

```python
def pull(self) -> None:
```
从文档拉取信息到 kanban_dict 属性。

该方法会打开指定的看板文件（self.kanban_path），读取其内容，并使用 read 方法解析文本内容，
最终将解析后的数据存储到 kanban_dict 属性中，便于后续操作。

```python
def push(self) -> None:
```
将当前 kanban_dict 的内容序列化并保存到看板文件。

本方法会调用 write(self.kanban_dict) 将字典内容转为文本，
并以 UTF-8 编码写入 self.kanban_path 指定的文件，实现数据持久化。

```python
def insert(self, text: str, pool: Pool) -> None:
```
在指定的池中插入一条新的任务信息。

Args:
    text (str): 任务的描述信息。
    pool (Pool): 要插入任务的池。

Returns:
    None

```python
def pop(self, text: str, pool: Pool) -> list['task']:
```
从指定的池中删除一条任务信息。

Args:
    text (str): 用于匹配的任务信息，可以是描述或ID。
    pool (Pool): 要从中删除任务的池。

Returns:
    None

```python
def get_tasks_in(self, pool: Pool) -> list[str]:
```
获取事件池中的任务

Args:
    pool (Pool): 枚举的池类型

Returns:
    list[str]: 返回对应的事件名称列表

```python
def get_task_by_word(self, word: str, pool: Pool | None = None) -> list[str]:
```
通过关键字查询任务

Args:
    word (str): 关键字
    pool (Pool | None, optional): 任务池,枚举类型.. Defaults to None.

Returns:
    list[str]: 返回查询到的任务列表

### `class KanBanManager`

No docstring provided.

#### Methods

```python
def __init__(self, kanban_path: str, pathlibs: list[str]):
```
看板管理类

Args:
    kanban_path (str): 看板文件路径 for example kb/x.md
    pathlibs (list[str]): 列表, 元素为所有监听的canvas文件路径

for example:
    pathlibs = ["/工程系统级设计/项目级别/DigitalLife/DigitalLife.canvas",
        "/工程系统级设计/项目级别/近期工作/近期工作.canvas",
        "/工程系统级设计/项目级别/coder/coder.canvas",]

```python
def sync_ready(self):
```
将任务从各canvas文件中提取出, 汇总到预备池

```python
def sync_order(self, by = 'code'):
```
将预备池中的任务进行加工,并添加到就绪池

Args:
    by (str, optional): 使用何种方式预估任务时间 支持code 与 llm 模式. Defaults to 'code'.

Returns:
    None: _description_

```python
def sync_run(self, max_p = 14):
```
将就绪池的排好顺序的任务移动到执行池中, 以填充一天的工作量

Args:
    max_p (int, optional): 1P代表半小时, 该参数表示填充的最大工作时长, 也和之前的任务耗时估计有联系, 不超过max_p. Defaults to 14.

Returns:
    None: _description_

