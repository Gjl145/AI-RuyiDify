"""文档创建与排版 — 快速生成格式化的 Word 文档

用法:
    from src.docx import DocCreator

    doc = DocCreator("output.docx")
    doc.add_title("标题")
    doc.add_heading("一级标题", level=1)
    doc.add_paragraph("正文内容")
    doc.add_table([["列1", "列2"], ["值1", "值2"]])
    doc.save()
"""

from pathlib import Path

from docx import Document
from docx.shared import Cm, Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT


class DocCreator:
    """创建并排版 Word 文档"""

    def __init__(self, path: str | Path | None = None):
        self.doc = Document()
        self.path = Path(path) if path else None
        self._setup_default_style()

    def _setup_default_style(self):
        style = self.doc.styles["Normal"]
        style.font.name = "微软雅黑"
        style.font.size = Pt(11)
        style.paragraph_format.space_after = Pt(6)

    # ── 标题 ──────────────────────────────────

    def add_title(self, text: str):
        """添加文档大标题（居中、加粗、24pt）"""
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.font.size = Pt(24)
        run.bold = True
        self.doc.add_paragraph()
        return p

    def add_heading(self, text: str, level: int = 1):
        """添加章节标题"""
        return self.doc.add_heading(text, level=level)

    # ── 段落 ──────────────────────────────────

    def add_paragraph(self, text: str, bold: bool = False, color: str | None = None,
                      size: int | None = None, align: str = "left"):
        """添加段落"""
        p = self.doc.add_paragraph()
        run = p.add_run(text)
        if bold:
            run.bold = True
        if color:
            run.font.color.rgb = RGBColor.from_string(color.strip("#"))
        if size:
            run.font.size = Pt(size)
        aligns = {"left": 0, "center": 1, "right": 2}
        p.alignment = WD_ALIGN_PARAGRAPH(aligns.get(align, 0))
        return p

    def add_bullet(self, items: list[str]):
        """添加项目符号列表"""
        for item in items:
            self.doc.add_paragraph(item, style="List Bullet")

    def add_numbered(self, items: list[str]):
        """添加编号列表"""
        for item in items:
            self.doc.add_paragraph(item, style="List Number")

    # ── 表格 ──────────────────────────────────

    def add_table(self, rows: list[list[str]], header: bool = True,
                  col_widths: list[float] | None = None):
        """添加表格。rows[0] 作为表头"""
        if not rows:
            return
        n_cols = max(len(r) for r in rows)
        table = self.doc.add_table(rows=len(rows), cols=n_cols, style="Light Grid Accent 1")
        table.alignment = WD_TABLE_ALIGNMENT.CENTER

        for i, row_data in enumerate(rows):
            for j, cell_text in enumerate(row_data):
                cell = table.cell(i, j)
                cell.text = str(cell_text)
                if i == 0 and header:
                    for p in cell.paragraphs:
                        for run in p.runs:
                            run.bold = True

        if col_widths:
            for i, w in enumerate(col_widths):
                for row in table.rows:
                    row.cells[i].width = Inches(w)
        return table

    # ── 页面设置 ──────────────────────────────

    def set_page(self, margin_cm: float = 2.5, orientation: str = "portrait"):
        """设置页边距和方向"""
        for attr in ["top", "bottom", "left", "right"]:
            setattr(self.doc.sections[0], f"{attr}_margin", Cm(margin_cm))
        if orientation == "landscape":
            self.doc.sections[0].orientation = 1
            self.doc.sections[0].page_width, self.doc.sections[0].page_height = \
                self.doc.sections[0].page_height, self.doc.sections[0].page_width

    # ── 保存 ──────────────────────────────────

    def save(self, path: str | Path | None = None):
        """保存文档"""
        target = Path(path) if path else self.path
        if target is None:
            raise ValueError("请指定保存路径")
        target.parent.mkdir(parents=True, exist_ok=True)
        self.doc.save(str(target))
        print(f"已保存: {target}")
