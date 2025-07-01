# API Documentation

## API for `/Users/zhaoxuefeng/GitHub/canvaz/src/canvaz/core.py`

这是一个包，用于处理canvas的文件，并提供一些方法来操作canvas
本包的核心思路在于获取canvas 中的Node和Edge 结点, 这些结点都是Box格式
通过直接修改Box的属性值来修改Node和Edge
常见的属性值为 id, text, x, y, width, height, color

### File Structure

```
core.py
├── class Color(Enum)
├── class Range(Enum)
├── class Node
│   ├── def __init__()
│   └── def to_dict()
├── class Edge
│   ├── def __init__()
│   └── def to_dict()
└── class Canvas
    ├── def __init__()
    ├── def add_node()
    ├── def add_edge()
    ├── def delete()
    ├── def select_by_id()
    ├── def select_by_color()
    ├── def select_nodes_by_type()
    ├── def select_nodes_by_text()
    ├── def select_edges_by_text()
    ├── def select_by_styleAttributes()
    ├── def to_file()
    └── def to_mermaid()
```

## Classes

### `class Color(Enum)`

颜色枚举

Args:
    Enum (_type_): 颜色枚举

Attributes:
    gray: 灰色
    red: 红色
    origne: 橙色
    yellow: 黄色
    green: 绿色
    blue: 蓝色
    purpol: 紫色

### `class Range(Enum)`

搜索范围枚举

Args:
    Enum (_type_): 范围枚举

Attributes:
    edge: edge
    node: node
    all: all

### `class Node`

Canvas 的结点概念

#### Methods

```python
def __init__(self, node_info: dict[str, str | dict]):
```
Node对象, 存储Node的属性, 可以使用python标准的属性赋值来修改它

Args:
    node_info (dict[str,str  |  dict]): _description_

Attributes:
    self.id : str
    self.text : str
    self.type : str
    self.width : str
    self.height : str
    self.styleAttributes : dict
    self.x : str
    self.y : str
    self.color : str

```python
def to_dict(self) -> dict:
```
将Edge对象的属性转换为字典格式。

Returns:
    dict: 包含Edge所有属性的字典。

### `class Edge`

Canvas 的边概念

#### Methods

```python
def __init__(self, edge_info: dict[str, str | dict]):
```
Edge对象, 存储Edge的属性, 可以使用python标准的属性赋值来修改它

Args:
    edge_info (dict[str,str  |  dict]): _description_

Attributes:
    self.id : str
    self.fromNode : str
    self.fromSide : str
    self.styleAttributes : str
    self.toNode : str
    self.toSide : str
    self.color : str

```python
def to_dict(self) -> dict:
```
将Edge对象的属性转换为字典格式。

Returns:
    dict: 包含Edge所有属性的字典。

### `class Canvas`

提供一些方法来方便的操作Canvas类文件

#### Methods

```python
def __init__(self, file_path: str):
```
初始化

Args:
    file_path (str, optional): 传入格式为canvas的文件路径. Defaults to None.

有一些可以调用的属性
self.all  canvas文件中的所有源内容
self.edges edges内容
self.nodes nodes内容
self.file_path 文件路径

```python
def add_node(self, text: str, color: Color = Color.gray):
```
添加节点

Args:
    text (str): 节点文本
    color (Color): 节点颜色. Defaults to Color.gray.

```python
def add_edge(self, from_node: str, to_node: str, color: Color | str = Color.gray):
```
TODO 等待实现

```python
def delete(self):
```
TODO 等待实现

```python
def select_by_id(self, id: str = '', range: Range = Range.node) -> Node | Edge:
```
可以通过在key中传入id 获取内容

Args:
    id (str, optional): Node or Edge 类型的id. Defaults to ''.
    range (Range, optional): Range Enum. Defaults to Range.node.

Returns:
    Node | Edge: 输出类型

```python
def select_by_color(self, color: Color = Color.gray, range: Range = Range.node) -> list[Node | Edge]:
```
可以通过在key中传入颜色

Args:
    color (Color, optional): _description_. Defaults to Color.gray.
    range (Range, optional): _description_. Defaults to Range.node.

Returns:
    list[Node | Edge]: _description_

```python
def select_nodes_by_type(self, key: str) -> list[Node]:
```
通过类型筛选节点（Node）。

你可以通过传入类型字符串，获得所有该类型的节点。
例如:
    select_nodes_by_type(key='text')
    select_nodes_by_type(key='file')

参数:
    key (str): 节点类型。

返回:
    list[Node]: 匹配类型的节点列表。

```python
def select_nodes_by_text(self, key: str) -> list[Node]:
```
优先选择文本包含指定关键字的节点。

参数:
    key (str): 要在节点文本中搜索的关键字。

返回:
    list[Node]: 文本包含该关键字的节点列表。

```python
def select_edges_by_text(self, key: str) -> list[Edge]:
```
通过文本内容筛选边（Edge）。
可以通过在 key 中传入文本，获得 label 属性包含该文本的边。

例如:
    select_edges_by_text(key='text')
    select_edges_by_text(key='file')

Args:
    key (str): 要搜索的文本。

Returns:
    list[Edge]: 返回 label 属性包含指定文本的边对象列表。

```python
def select_by_styleAttributes(self, type = 'file', key: Color = ''):
```
TODO 等待实现

```python
def to_file(self, file_path: str) -> None:
```
保存到文件夹

Args:
    file_path (_type_): _description_

```python
def to_mermaid(self):
```
输出为mermaid文件

Returns:
    str: 对应输出的mermaid文件

