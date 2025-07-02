# API Documentation

## API for `/Users/zhaoxuefeng/GitHub/obwikilink/src/obwikilink/core.py`

### File Structure

```
core.py
├── class WikiLink
│   ├── def __init__()
│   ├── def is_valid()
│   ├── def get_target_path()
│   └── def __repr__()
├── class WikiLinkFactory
│   ├── def create_from_text()
│   └── def create_from_target()
├── class ILinkGenerationStrategy
│   └── def generate_link()
├── class KeywordStrategy(ILinkGenerationStrategy)
│   └── def generate_link()
├── class SimilarityStrategy(ILinkGenerationStrategy)
│   └── def generate_link()
├── class ObsidianMarkdownSDK
│   ├── def __init__()
│   ├── def set_link_generation_strategy()
│   ├── def read_markdown()
│   ├── def write_markdown()
│   ├── def find_wikilinks()
│   ├── def insert_wikilink()
│   ├── def refactor_to_wikilink()
│   ├── def extract_sections()
│   ├── def find_tags()
│   └── def add_tags()
└── class SimilarityStrategy(ILinkGenerationStrategy)
    └── def generate_link()
```

## Classes

### `class WikiLink`

Represents an Obsidian wikilink (e.g., `[[TargetNote]]` or `[[TargetNote|Display Text]]`).

:param target_name: The name of the target note.
:type target_name: str
:param full_text: The full wikilink text, including brackets.
:type full_text: str
:param display_text: Optional display text for the wikilink. Defaults to None.
:type display_text: Optional[str]
:param start_pos: The starting position of the wikilink in the source text. Defaults to None.
:type start_pos: Optional[int]
:param end_pos: The ending position of the wikilink in the source text. Defaults to None.
:type end_pos: Optional[int]
:param source_file: The path to the file where the wikilink was found. Defaults to None.
:type source_file: Optional[str]

#### Methods

```python
def __init__(self, target_name: str, full_text: str, display_text: Optional[str] = None, start_pos: Optional[int] = None, end_pos: Optional[int] = None, source_file: Optional[str] = None):
```
No docstring provided.

```python
def is_valid(self) -> bool:
```
Checks if the WikiLink object is valid (has target_name and full_text).

:returns: True if the wikilink is valid, False otherwise.
:rtype: bool

```python
def get_target_path(self) -> str:
```
Generates the expected file path for the target note.

Currently, it appends '.md' to the target name.
:returns: The expected file path for the target note.
:rtype: str

```python
def __repr__(self):
```
Returns a string representation of the WikiLink object.

### `class WikiLinkFactory`

A factory class for creating WikiLink objects.

#### Methods

```python
def create_from_text(full_text: str, start_pos: int, end_pos: int, source_file: Optional[str] = None) -> WikiLink:
```
Creates a WikiLink object from a full wikilink string.

:param full_text: The full wikilink text (e.g., "[[TargetNote]]" or "[[TargetNote|Display]]").
:type full_text: str
:param start_pos: The starting position of the wikilink in the source text.
:type start_pos: int
:param end_pos: The ending position of the wikilink in the source text.
:type end_pos: int
:param source_file: The path to the file where the wikilink was found. Defaults to None.
:type source_file: Optional[str]
:returns: A WikiLink object.
:rtype: WikiLink
:raises ValueError: If the provided full_text is not a valid wikilink format.

```python
def create_from_target(target_name: str, display_text: Optional[str] = None, source_file: Optional[str] = None) -> WikiLink:
```
Creates a WikiLink object from a target name and optional display text.

:param target_name: The name of the target note.
:type target_name: str
:param display_text: Optional display text for the wikilink. Defaults to None.
:type display_text: Optional[str]
:param source_file: The path to the file where the wikilink will be created. Defaults to None.
:type source_file: Optional[str]
:returns: A WikiLink object.
:rtype: WikiLink

### `class ILinkGenerationStrategy`

Abstract base class for defining link generation strategies.

Concrete strategies should inherit from this class and implement the `generate_link` method.

#### Methods

```python
def generate_link(self, content: str, context: any) -> WikiLink:
```
Generates a WikiLink based on the provided content and context.

:param content: The markdown content to analyze for link generation.
:type content: str
:param context: Additional context that might be needed by the strategy (e.g., a list of keywords, a similarity model).
:type context: any
:returns: A WikiLink object if a link can be generated, otherwise None.
:rtype: WikiLink
:raises NotImplementedError: This method must be implemented by concrete strategy classes.

### `class KeywordStrategy(ILinkGenerationStrategy)`

A concrete strategy for generating WikiLinks based on predefined keywords.

This is a placeholder implementation. In a real scenario, it would identify keywords in the content
and create WikiLink objects for them.

#### Methods

```python
def generate_link(self, content: str, context: any) -> WikiLink:
```
Generates a WikiLink if the content contains the keyword "keyword".

:param content: The markdown content to analyze.
:type content: str
:param context: Not used in this placeholder implementation.
:type context: any
:returns: A WikiLink object for "keyword" if found, otherwise None.
:rtype: WikiLink

### `class SimilarityStrategy(ILinkGenerationStrategy)`

A concrete strategy for generating WikiLinks based on content similarity.

This is a placeholder implementation. In a real scenario, it would use NLP techniques
to find similar concepts and create WikiLink objects.

#### Methods

```python
def generate_link(self, content: str, context: any) -> WikiLink:
```
Generates a WikiLink if the content contains the keyword "similarity".

:param content: The markdown content to analyze.
:type content: str
:param context: Not used in this placeholder implementation.
:type context: any
:returns: A WikiLink object for "similarity" if found, otherwise None.
:rtype: WikiLink

### `class ObsidianMarkdownSDK`

A facade class providing a simplified interface for interacting with Obsidian Markdown documents.

This SDK offers atomic, composable operations for creating and managing Obsidian wikilinks and tags,
facilitating the efficient construction of knowledge networks.

#### Methods

```python
def __init__(self, link_generation_strategy: Optional[ILinkGenerationStrategy] = None):
```
Initializes the ObsidianMarkdownSDK.

:param link_generation_strategy: An optional strategy for generating links.
                                 If None, no automatic link generation will occur.
:type link_generation_strategy: Optional[ILinkGenerationStrategy]

```python
def set_link_generation_strategy(self, strategy: ILinkGenerationStrategy):
```
Sets the link generation strategy for the SDK.

:param strategy: The strategy to be used for generating links.
:type strategy: ILinkGenerationStrategy

```python
def read_markdown(self, file_path: str) -> str:
```
Reads the content of a Markdown file.

:param file_path: The path to the Markdown file.
:type file_path: str
:returns: The content of the Markdown file as a string.
:rtype: str
:raises FileNotFoundError: If the specified file does not exist.

```python
def write_markdown(self, file_path: str, content: str) -> bool:
```
Writes content to a Markdown file.

If the directory for the file does not exist, it will be created.

:param file_path: The path to the Markdown file.
:type file_path: str
:param content: The content to write to the file.
:type content: str
:returns: True if the content was successfully written, False otherwise.
:rtype: bool

```python
def find_wikilinks(self, markdown_content: str) -> List[WikiLink]:
```
Identifies and extracts all Obsidian wikilinks from the given Markdown content.

:param markdown_content: The Markdown content to search within.
:type markdown_content: str
:returns: A list of WikiLink objects found in the content.
:rtype: List[WikiLink]

```python
def insert_wikilink(self, markdown_content: str, wikilink: WikiLink, position: int = -1) -> str:
```
Inserts a WikiLink object into the Markdown content at a specified position.

:param markdown_content: The original Markdown content.
:type markdown_content: str
:param wikilink: The WikiLink object to insert.
:type wikilink: WikiLink
:param position: The character position at which to insert the wikilink.
                 If -1 (default), the wikilink is appended to the end of the content.
:type position: int
:returns: The Markdown content with the wikilink inserted.
:rtype: str
:raises ValueError: If an invalid WikiLink object is provided.

```python
def refactor_to_wikilink(self, original_file_path: str, content_to_extract: str, new_note_name: str, new_note_dir: str = '') -> Tuple[str, str]:
```
Extracts specific content from an original Markdown file into a new note,
and replaces the extracted content in the original file with a wikilink to the new note.

:param original_file_path: The path to the original Markdown file.
:type original_file_path: str
:param content_to_extract: The exact content string to be extracted.
:type content_to_extract: str
:param new_note_name: The name of the new note (will be used as the target name for the wikilink).
:type new_note_name: str
:param new_note_dir: Optional directory where the new note will be created. Defaults to current directory.
:type new_note_dir: str
:returns: A tuple containing the path to the new note and the updated content of the original file.
:rtype: Tuple[str, str]
:raises ValueError: If the content to extract is not found in the original file.

```python
def extract_sections(self, markdown_content: str, section_type: str = 'paragraph') -> List[str]:
```
Extracts sections from Markdown content based on a specified type.

:param markdown_content: The Markdown content to extract sections from.
:type markdown_content: str
:param section_type: The type of sections to extract ('paragraph' or 'heading'). Defaults to 'paragraph'.
:type section_type: str
:returns: A list of extracted sections.
:rtype: List[str]
:raises ValueError: If an unsupported section type is provided.

```python
def find_tags(self, markdown_content: str) -> List[str]:
```
Identifies and extracts all Obsidian tags (e.g., `#tag` or `#tag/subtag`) from the given Markdown content.

:param markdown_content: The Markdown content to search within.
:type markdown_content: str
:returns: A list of unique tags found in the content.
:rtype: List[str]

```python
def add_tags(self, markdown_content: str, tags: List[str]) -> str:
```
Adds specified tags to the Markdown content.

Currently, tags are appended to the end of the content.

:param markdown_content: The original Markdown content.
:type markdown_content: str
:param tags: A list of tags (strings, without '#') to add.
:type tags: List[str]
:returns: The Markdown content with the new tags added.
:rtype: str

### `class SimilarityStrategy(ILinkGenerationStrategy)`

Strategy for generating WikiLinks based on similarity.

#### Methods

```python
def generate_link(self, content: str, context: any) -> WikiLink:
```
No docstring provided.

