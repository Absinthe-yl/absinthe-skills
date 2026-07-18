#!/usr/bin/env python3
"""ATS keyword coverage checker for resume tailoring.

Reads a resume and a job description, extracts candidate keywords from the JD
(technical terms, skills, tool names), and reports how many appear in the
resume, the coverage rate, and the missing keywords as a gap list.

Usage:
    python ats_match.py --resume resume.md --jd jd.txt [--top N]

The script only does deterministic keyword matching; it does not judge
semantic equivalence. Use its output as a quantitative signal, then apply
human/agent judgment for synonyms and context.
"""
import argparse
import re
from collections import OrderedDict

# High-value technical tokens. Extend as needed for the target domain.
TECH_PATTERN = re.compile(
    r"\b(?:Java|Python|C\+\+|Go|Rust|JavaScript|TypeScript|SQL|Spring|"
    r"SpringBoot|MyBatis|Redis|MySQL|PostgreSQL|MongoDB|Kafka|RabbitMQ|"
    r"Docker|Kubernetes|K8s|AWS|GCP|Azure|Linux|React|Vue|Node\.js|"
    r"TensorFlow|PyTorch|RAG|MCP|Agent|LLM|Prompt|GPT|Microservice|"
    r"Distributed|Concurrency|Async|HTML|CSS|Git|CI/CD|Prometheus|"
    r"Grafana|Elasticsearch|Spark|Flink|Hadoop|WebFlux|CompletableFuture|"
    r"WeCube|IDKey|PGVector|gRPC|Thrift|RPC|Kafka)\b",
    re.IGNORECASE,
)


def read_text(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def extract_keywords(jd_text, top):
    keywords = OrderedDict()
    for t in TECH_PATTERN.findall(jd_text):
        k = t.lower()
        keywords[k] = keywords.get(k, 0) + 1
    # bracketed / quoted skill phrases
    for p in re.findall(r"[「『\"]([^」』\"]{1,30})[」』\"]", jd_text):
        k = p.strip().lower()
        if 2 <= len(k) <= 30:
            keywords[k] = keywords.get(k, 0) + 1
    # requirement-style bullets
    for b in re.findall(r"(?:职责|要求|技能|优先|精通|熟悉|掌握)[：: ]*([^\n。；;]{2,40})", jd_text):
        k = b.strip().lower()
        if 2 <= len(k) <= 30:
            keywords[k] = keywords.get(k, 0) + 1
    return list(keywords.keys())[:top]


def coverage(resume_text, keywords):
    rt = resume_text.lower()
    matched, missing = [], []
    for kw in keywords:
        (matched if kw.lower() in rt else missing).append(kw)
    total = len(keywords) or 1
    rate = round(100 * len(matched) / total, 1)
    return matched, missing, rate


def main():
    ap = argparse.ArgumentParser(description="ATS keyword coverage checker")
    ap.add_argument("--resume", required=True, help="path to resume file")
    ap.add_argument("--jd", required=True, help="path to job description file")
    ap.add_argument("--top", type=int, default=40, help="max keywords to consider")
    args = ap.parse_args()

    resume_text = read_text(args.resume)
    jd_text = read_text(args.jd)
    keywords = extract_keywords(jd_text, args.top)
    matched, missing, rate = coverage(resume_text, keywords)

    print("=" * 48)
    print("ATS KEYWORD COVERAGE REPORT")
    print("=" * 48)
    print(f"JD 关键词总数 (top {len(keywords)}): {len(keywords)}")
    print(f"简历命中: {len(matched)}")
    print(f"覆盖率: {rate}%")
    print("-" * 48)
    print(f"✅ 已覆盖 ({len(matched)}):")
    print("  " + ", ".join(matched) if matched else "  (无)")
    print("-" * 48)
    print(f"❌ 缺失 ({len(missing)}):")
    print("  " + ", ".join(missing) if missing else "  (无)")
    print("=" * 48)
    print(f"SUMMARY|total={len(keywords)}|matched={len(matched)}|rate={rate}")


if __name__ == "__main__":
    main()
