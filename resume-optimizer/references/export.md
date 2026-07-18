# 多格式专业导出 (Multi-Format Export)

## 五格式 × 四模板

### 格式
- **Markdown**：工作主格式。标准 `##` 章节 + 列表，中英文间加空格。
- **Word (.docx)**：用 pandoc（`pandoc resume.md -o resume.docx`）或 python-docx 生成；避免复杂表格与文本框。
- **HTML**：内联 CSS，A4 宽度，`@media print` 优化；专业风模板见 `assets/professional-resume.html`。
- **LaTeX**：XeLaTeX 编译，CTeX / xeCJK 处理中文；可用 moderncv / altacv 风格。
- **PDF**：由上述任一格式生成；确保文本可选（非图片 PDF）以利 ATS。

### 四套模板风格
| 模板 | 适用 | 风格 |
|---|---|---|
| professional | 金融 / 法律 / 咨询 | 稳重、单栏、衬线 |
| modern | 科技 / 创业 | 无衬线、强调项目、可双栏 |
| minimal | 资深 / 工程 | 极简、留白、去装饰 |
| academic | 学术 / 科研 | 含发表 / 项目 / 教学 |

## ATS 导出守则
- 使用标准章节标题（工作经历 / 教育背景 / 技能）。
- 保留关键词原文，不转成图片。
- 无分栏、无文本框、无表格嵌套。
- 联系方式独立成行、可解析。

## HTML 模板使用
复制 `assets/professional-resume.html`，替换 `{{姓名}}` 等占位为真实内容（或直接重写结构）。打印时浏览器「另存为 PDF」即可得到 ATS 友好文件。

## LaTeX 中文最小示例
```latex
\documentclass[11pt]{article}
\usepackage{xeCJK}
\setCJKmainfont{Noto Serif CJK SC}
\begin{document}
\section*{陈珏龙}
电话：178xxxx | 邮箱：xxx@qq.com\\
\section{实习经历}
\subsection{腾讯 WXG}
...
\end{document}
```
编译：`xelatex resume.tex`
