"""Word 文档处理工具包 — 创建、排版、编辑、模板渲染、读取

依赖: python-docx, docxtpl, python-docx-replace
安装: pip install python-docx docxtpl python-docx-replace

核心能力:
  creator   — 快速创建新文档，段落/表格/标题/样式
  editor    — 打开已有文档进行修改、替换、合并
  template  — 基于 Jinja2 模板批量生成文档
  reader    — 读取文档内容，提取结构化信息
"""

from .creator import DocCreator as DocCreator  # noqa: F401
from .editor import DocEditor as DocEditor  # noqa: F401
from .template import DocTemplate as DocTemplate  # noqa: F401
from .reader import DocReader as DocReader  # noqa: F401
