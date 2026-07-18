---
name: resume-optimizer
description: This skill should be used when a user wants to score, polish, tailor, or export a resume/CV (中文简历 or English resume). Triggers include "resume", "CV", "polish my resume", "score my resume", "tailor for this job", "optimize for ATS", "export resume to PDF/Word". It combines recruiter-eye rewriting, a 100-point scoring model, a 40+ item checklist, JD-based customization, and multi-format export (Word/Markdown/HTML/LaTeX/PDF).
---

# Resume Optimizer

## Overview

Transform a resume into a competitive, ATS-friendly document through recruiter-eye rewriting. Combine a 100-point scoring model, a 40+ item deep-polish checklist, JD-based customization, and multi-format export. The goal is genuine competitiveness, not inflated scores.

## When to Use

- User pastes a resume (or points to a local docx/pdf) and asks to "评分 / 润色 / 优化 / 重写".
- User supplies a job description (JD) and asks to "按这个岗位定制 / 提升匹配度".
- User asks to "导出为 PDF / Word / HTML / LaTeX".
- User says "帮我写一份新简历" and provides background.

## Intent Detection

First classify the request as one of: **score / polish / customize / export / create-new**. If background is missing (work history, education, skills, target role), ask before proceeding.

## Workflow

1. **Baseline (optional but recommended):** For an existing resume, run the scoring model first to establish a baseline score and issue list.
2. **Execute core task** (see Core Capabilities).
3. **Quality recheck:** Re-score after edits; quantify the lift (e.g., 68 → 92); confirm ATS compatibility and clean layout.
4. **Deliver & advise:** Provide the final resume, next steps (channels, interview prep, cover letter), and recommend Markdown as the working master format for easy conversion.

## Core Capabilities

### 1. 100-Point Professional Scoring

Score across five dimensions:

| Dimension | Weight |
|---|---|
| Content quality | 30 |
| Structure & layout | 25 |
| Language & grammar | 20 |
| ATS optimization | 15 |
| Impact & impression | 10 |

Output: total score, grade (A+ to F), per-dimension breakdown, Top 3 strengths, prioritized improvements (each with a Before → After rewrite), and a 5-step action plan. See `references/scoring.md`.

### 2. 40+ Item Deep-Polish Checklist

Cover 8 categories — contact, summary, experience, education, skills, grammar, layout, ATS — with 40+ checks marked ✅ / ❌ / ⚠️. Deliver the polished full text plus a change summary graded 🔴 critical → 🟡 important → 🟢 minor → 💡 suggestion, a strong-verb table, and a quantification guide. See `references/checklist.md`.

### 3. JD-Based Customization

Parse the JD (required skills, nice-to-have skills, responsibilities, keywords) → build a gap matrix → fuse keywords naturally into real experience → produce a match-rate report with before/after coverage comparison. Use `scripts/ats_match.py` to quantify coverage. See `references/customize.md`.

### 4. Multi-Format Export

Support Word / Markdown / HTML / LaTeX / PDF across four templates: professional (finance/legal/consulting), modern (tech/startup), minimal (senior/engineering), academic (research). HTML uses inline CSS with print optimization; LaTeX is XeLaTeX-compatible with CJK support. See `references/export.md` and `assets/professional-resume.html`.

### 5. Create-New Resume

Draft from scratch using the structure above, prioritizing strong verbs and quantified results.

## Output Specs

- **Scoring report** must contain: total score, grade, five-dimension breakdown, Top 3 strengths, prioritized improvements, Before → After examples, 5-step plan.
- **Polish report** must contain: 40+ check results, polished full text, graded change summary, strong-verb table, quantification guide.
- **Customization report** must contain: JD parse, gap matrix, customized resume, before/after keyword coverage comparison.

## Language & Formatting

- Default to Chinese; switch to English only when the user explicitly asks.
- Chinese/English mixing: insert a space between digits/English and Chinese (e.g., "Java 基础", "P99 响应").
- All resume output uses clear Markdown structure; exports strictly follow the target format spec.

## Constraints

- Input resume cap: 10,000 characters. If exceeded, ask the user to trim.
- Never fabricate companies, roles, or metrics. Quantification must be a reasonable deduction from provided material; mark inferred numbers as "需用户确认".
- Keyword fusion must be natural — no stuffing or concealment (avoid ATS spam flags).
- Proactively flag/sanitize sensitive info (ID numbers, salary, health).
- Always optimize for real competitiveness; fix critical issues before minor ones.

## Resources

- `references/scoring.md` — scoring model and report template
- `references/checklist.md` — 40+ item checklist and grading standard
- `references/customize.md` — JD parsing and gap-matrix method
- `references/export.md` — five-format, four-template export spec
- `scripts/ats_match.py` — JD keyword coverage quantifier
- `assets/professional-resume.html` — professional HTML template (inline CSS + print)
