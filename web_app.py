# -*- coding: utf-8 -*-
"""
机器学习算法 Python 实现 —— 结果展示网站
扫描各模块目录下的 result_*.png 图片，以画廊形式展示运行结果。
"""
import os
import glob
from flask import Flask, render_template_string, send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 模块元信息：目录名 -> (中文名, 英文名, 描述, 关键指标)
MODULES = [
    {
        "dir": "LinearRegression",
        "name": "线性回归",
        "en": "Linear Regression",
        "no": "01",
        "desc": "用梯度下降法拟合数据，实现代价函数最小化；包含均值归一化与 scikit-learn 对照实现。",
        "metrics": [("学习率", "α=0.01"), ("迭代次数", "1500"), ("结果", "梯度下降收敛")],
    },
    {
        "dir": "LogisticRegression",
        "name": "逻辑回归",
        "en": "Logistic Regression",
        "no": "02",
        "desc": "二分类与多分类（OneVsAll 手写数字识别），含正则化、多项式特征映射与 scipy 优化。",
        "metrics": [("二分类准确率", "83%"), ("OneVsAll 准确率", "96.48%"), ("数字集", "5000 张")],
    },
    {
        "dir": "NeuralNetwok",
        "name": "BP 神经网络",
        "en": "Neural Network",
        "no": "03",
        "desc": "三层前馈网络 + 反向传播，实现手写数字识别，含梯度检查与权重可视化。",
        "metrics": [("隐藏层", "25 单元"), ("准确率", "98.58%"), ("数字集", "5000 张")],
    },
    {
        "dir": "SVM",
        "name": "支持向量机",
        "en": "SVM",
        "no": "04",
        "desc": "线性核与 RBF 高斯核的分类边界，对比不同 C / σ 参数下的 margin 效果。",
        "metrics": [("核函数", "Linear / RBF"), ("数据集", "3 组"), ("结果", "决策边界可视化")],
    },
    {
        "dir": "K-Means",
        "name": "K-Means 聚类",
        "en": "K-Means",
        "no": "05",
        "desc": "无监督聚类算法，含聚类中心迭代过程可视化与图片压缩应用（16 色压缩）。",
        "metrics": [("聚类数 K", "3 / 16"), ("应用", "图片压缩"), ("迭代", "收敛")],
    },
    {
        "dir": "PCA",
        "name": "主成分分析",
        "en": "PCA",
        "no": "06",
        "desc": "降维算法，2D→1D 与高维人脸数据集降维，含数据恢复与主成分个数选择。",
        "metrics": [("降维", "2D→1D / 人脸"), ("保留方差", "99%"), ("数据集", "人脸 + 模拟")],
    },
    {
        "dir": "AnomalyDetection",
        "name": "异常检测",
        "en": "Anomaly Detection",
        "no": "07",
        "desc": "基于高斯分布的异常检测算法，通过 F1 分数选择阈值 ε，含单元与多元高斯分布。",
        "metrics": [("阈值 ε", "8.99e-05"), ("F1 分数", "0.875"), ("异常点", "已标记")],
    },
]

app = Flask(__name__)


def get_module_images(module_dir):
    """获取模块目录下所有 result_*.png 图片，按文件名排序。"""
    pattern = os.path.join(BASE_DIR, module_dir, "result_*.png")
    files = sorted(glob.glob(pattern))
    return [os.path.relpath(f, BASE_DIR).replace("\\", "/") for f in files]


@app.route("/")
def index():
    modules_data = []
    for m in MODULES:
        images = get_module_images(m["dir"])
        modules_data.append({
            "name": m["name"],
            "en": m["en"],
            "no": m["no"],
            "desc": m["desc"],
            "metrics": m["metrics"],
            "images": images,
            "dir": m["dir"],
        })
    return render_template_string(TEMPLATE, modules=modules_data)


@app.route("/<path:filepath>")
def serve_image(filepath):
    safe_path = os.path.normpath(filepath)
    if safe_path.startswith("..") or os.path.isabs(safe_path):
        return "Forbidden", 403
    full_path = os.path.join(BASE_DIR, safe_path)
    if not os.path.isfile(full_path):
        return "Not Found", 404
    directory = os.path.dirname(full_path)
    filename = os.path.basename(full_path)
    return send_from_directory(directory, filename)


TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>机器学习算法 Python 实现 · 结果展示</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700;9..144,900&family=Manrope:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #faf8f5;
    --bg-soft: #f3efe8;
    --surface: #ffffff;
    --surface-2: #fbf9f6;
    --ink: #1a1a1a;
    --ink-2: #4a4a4a;
    --ink-3: #8a8578;
    --line: #e8e2d8;
    --line-2: #d9d2c5;
    --accent: #c8553d;
    --accent-soft: #f2e6e1;
    --accent-2: #2d5d4f;
    --gold: #b08d57;
    --radius: 14px;
    --radius-sm: 8px;
    --shadow-sm: 0 1px 3px rgba(26,26,26,0.04), 0 1px 2px rgba(26,26,26,0.03);
    --shadow-md: 0 4px 20px rgba(26,26,26,0.06), 0 2px 6px rgba(26,26,26,0.04);
    --shadow-lg: 0 20px 50px rgba(26,26,26,0.1), 0 8px 20px rgba(26,26,26,0.05);
    --ease: cubic-bezier(0.22, 1, 0.36, 1);
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  html { scroll-behavior: smooth; }

  body {
    font-family: "Manrope", -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
    background: var(--bg);
    color: var(--ink);
    line-height: 1.7;
    -webkit-font-smoothing: antialiased;
    overflow-x: hidden;
  }

  /* 纸张纹理背景 */
  body::before {
    content: "";
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.025'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
  }

  /* ============ 阅读进度条 ============ */
  .progress-bar {
    position: fixed;
    top: 0;
    left: 0;
    height: 3px;
    width: 0%;
    background: linear-gradient(90deg, var(--accent), var(--gold));
    z-index: 200;
    transition: width 0.1s linear;
  }

  /* ============ 左侧粘性导航 ============ */
  .side-nav {
    position: fixed;
    left: 32px;
    top: 50%;
    transform: translateY(-50%);
    z-index: 90;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }
  .side-nav a {
    display: flex;
    align-items: center;
    gap: 10px;
    text-decoration: none;
    color: var(--ink-3);
    font-size: 0.72rem;
    font-weight: 500;
    padding: 7px 4px;
    transition: all 0.3s var(--ease);
    opacity: 0.55;
  }
  .side-nav a .sn-no {
    font-family: "JetBrains Mono", monospace;
    font-size: 0.65rem;
    min-width: 18px;
    transition: all 0.3s var(--ease);
  }
  .side-nav a .sn-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--line-2);
    transition: all 0.3s var(--ease);
  }
  .side-nav a .sn-label {
    font-family: "JetBrains Mono", monospace;
    white-space: nowrap;
    transform: translateX(-4px);
    opacity: 0;
    transition: all 0.3s var(--ease);
  }
  .side-nav a:hover {
    opacity: 1;
    color: var(--ink);
  }
  .side-nav a:hover .sn-label {
    opacity: 1;
    transform: translateX(0);
  }
  .side-nav a.active {
    opacity: 1;
    color: var(--accent);
  }
  .side-nav a.active .sn-dot {
    background: var(--accent);
    transform: scale(1.6);
  }
  .side-nav a.active .sn-no {
    color: var(--accent);
    font-weight: 700;
  }
  @media (max-width: 1100px) {
    .side-nav { display: none; }
  }

  /* ============ 顶部导航 ============ */
  .nav {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 100;
    padding: 18px 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(250, 248, 245, 0.75);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--line);
    transition: all 0.4s var(--ease);
  }
  .nav.scrolled {
    padding: 12px 40px;
    background: rgba(250, 248, 245, 0.92);
  }
  .nav-logo {
    font-family: "Fraunces", serif;
    font-weight: 700;
    font-size: 1.25rem;
    color: var(--ink);
    letter-spacing: -0.01em;
  }
  .nav-logo .dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    background: var(--accent);
    border-radius: 50%;
    margin-right: 8px;
    vertical-align: middle;
  }
  .nav-links {
    display: flex;
    gap: 28px;
    list-style: none;
  }
  .nav-links a {
    color: var(--ink-2);
    text-decoration: none;
    font-size: 0.85rem;
    font-weight: 500;
    transition: color 0.2s;
    position: relative;
  }
  .nav-links a:hover { color: var(--accent); }
  .nav-links a::after {
    content: "";
    position: absolute;
    bottom: -4px;
    left: 0;
    width: 0;
    height: 1.5px;
    background: var(--accent);
    transition: width 0.3s var(--ease);
  }
  .nav-links a:hover::after { width: 100%; }

  /* ============ Hero ============ */
  .hero {
    position: relative;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 120px 40px 80px;
    text-align: center;
    overflow: hidden;
  }
  .hero-bg {
    position: absolute;
    inset: 0;
    z-index: -1;
    overflow: hidden;
  }
  .hero-blob {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.4;
    animation: float 20s ease-in-out infinite;
  }
  .hero-blob-1 {
    width: 500px; height: 500px;
    background: radial-gradient(circle, var(--accent-soft), transparent 70%);
    top: -100px; left: -100px;
  }
  .hero-blob-2 {
    width: 600px; height: 600px;
    background: radial-gradient(circle, #e8ede9, transparent 70%);
    bottom: -150px; right: -150px;
    animation-delay: -7s;
  }
  .hero-blob-3 {
    width: 400px; height: 400px;
    background: radial-gradient(circle, #f5ede0, transparent 70%);
    top: 40%; left: 50%;
    transform: translate(-50%, -50%);
    animation-delay: -14s;
  }
  @keyframes float {
    0%, 100% { transform: translate(0, 0) scale(1); }
    33% { transform: translate(40px, -30px) scale(1.05); }
    66% { transform: translate(-30px, 40px) scale(0.95); }
  }

  .hero-eyebrow {
    font-family: "JetBrains Mono", monospace;
    font-size: 0.8rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 28px;
    opacity: 0;
    animation: rise 0.8s var(--ease) 0.1s forwards;
  }
  .hero h1 {
    font-family: "Fraunces", serif;
    font-size: clamp(2.8rem, 7vw, 5.5rem);
    font-weight: 600;
    line-height: 1.05;
    letter-spacing: -0.03em;
    color: var(--ink);
    max-width: 900px;
    margin-bottom: 28px;
    opacity: 0;
    animation: rise 0.9s var(--ease) 0.25s forwards;
  }
  .hero h1 em {
    font-style: italic;
    font-weight: 400;
    color: var(--accent);
    position: relative;
  }
  .hero h1 em::after {
    content: "";
    position: absolute;
    bottom: 0.08em;
    left: 0;
    right: 0;
    height: 0.12em;
    background: var(--accent-soft);
    z-index: -1;
    border-radius: 2px;
  }
  .hero-sub {
    font-size: 1.15rem;
    color: var(--ink-2);
    max-width: 600px;
    margin-bottom: 48px;
    font-weight: 300;
    opacity: 0;
    animation: rise 0.9s var(--ease) 0.4s forwards;
  }
  .hero-stats {
    display: flex;
    gap: 56px;
    opacity: 0;
    animation: rise 0.9s var(--ease) 0.55s forwards;
  }
  .hero-stat {
    text-align: center;
  }
  .hero-stat .num {
    font-family: "Fraunces", serif;
    font-size: 3rem;
    font-weight: 600;
    color: var(--ink);
    line-height: 1;
    letter-spacing: -0.02em;
  }
  .hero-stat .num span {
    color: var(--accent);
  }
  .hero-stat .label {
    font-size: 0.8rem;
    color: var(--ink-3);
    margin-top: 8px;
    letter-spacing: 0.05em;
  }
  .hero-scroll {
    position: absolute;
    bottom: 36px;
    left: 50%;
    transform: translateX(-50%);
    color: var(--ink-3);
    font-size: 0.75rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    opacity: 0;
    animation: rise 0.9s var(--ease) 0.8s forwards;
  }
  .hero-scroll::after {
    content: "";
    display: block;
    width: 1px;
    height: 40px;
    background: var(--line-2);
    margin: 12px auto 0;
    animation: scrollLine 2s ease-in-out infinite;
  }
  @keyframes scrollLine {
    0%, 100% { transform: scaleY(0.4); transform-origin: top; }
    50% { transform: scaleY(1); }
  }
  @keyframes rise {
    from { opacity: 0; transform: translateY(24px); }
    to { opacity: 1; transform: translateY(0); }
  }

  /* ============ 主体 ============ */
  main {
    position: relative;
    z-index: 1;
    max-width: 1280px;
    margin: 0 auto;
    padding: 60px 40px 120px;
  }
  .section-label {
    font-family: "JetBrains Mono", monospace;
    font-size: 0.75rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--ink-3);
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .section-label::before {
    content: "";
    width: 32px;
    height: 1px;
    background: var(--line-2);
  }
  .section-title {
    font-family: "Fraunces", serif;
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 600;
    letter-spacing: -0.02em;
    margin-bottom: 8px;
    color: var(--ink);
  }
  .section-desc {
    color: var(--ink-2);
    font-size: 1rem;
    max-width: 560px;
    margin-bottom: 60px;
  }

  /* ============ 模块卡片 ============ */
  .module {
    position: relative;
    margin-bottom: 80px;
    opacity: 0;
    transform: translateY(40px);
    transition: opacity 0.8s var(--ease), transform 0.8s var(--ease);
  }
  .module.visible {
    opacity: 1;
    transform: translateY(0);
  }
  .module-header {
    display: flex;
    align-items: flex-end;
    gap: 20px;
    margin-bottom: 32px;
    padding-bottom: 24px;
    border-bottom: 1px solid var(--line);
  }
  .module-no {
    font-family: "Fraunces", serif;
    font-size: 4.5rem;
    font-weight: 300;
    color: var(--accent);
    line-height: 0.8;
    opacity: 0.6;
    font-style: italic;
  }
  .module-title-group {
    flex: 1;
  }
  .module h2 {
    font-family: "Fraunces", serif;
    font-size: clamp(1.8rem, 3.5vw, 2.6rem);
    font-weight: 600;
    letter-spacing: -0.02em;
    color: var(--ink);
    line-height: 1.1;
  }
  .module-en {
    font-family: "JetBrains Mono", monospace;
    font-size: 0.8rem;
    color: var(--ink-3);
    letter-spacing: 0.1em;
    margin-top: 6px;
    text-transform: uppercase;
  }
  .module-desc {
    color: var(--ink-2);
    font-size: 0.95rem;
    max-width: 480px;
    margin-left: auto;
    padding-left: 20px;
    border-left: 2px solid var(--accent-soft);
  }
  .metrics {
    display: flex;
    gap: 10px;
    margin-bottom: 28px;
    flex-wrap: wrap;
  }
  .metric {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 100px;
    padding: 7px 16px;
    font-size: 0.8rem;
    box-shadow: var(--shadow-sm);
    transition: all 0.25s var(--ease);
  }
  .metric:hover {
    border-color: var(--accent);
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
  }
  .metric .k {
    color: var(--ink-3);
    font-family: "JetBrains Mono", monospace;
  }
  .metric .v {
    color: var(--accent);
    font-weight: 600;
    margin-left: 6px;
    font-family: "JetBrains Mono", monospace;
  }

  /* ============ 画廊 ============ */
  .gallery {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
  }
  .img-card {
    position: relative;
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    overflow: hidden;
    cursor: zoom-in;
    box-shadow: var(--shadow-sm);
    transition: all 0.4s var(--ease);
    aspect-ratio: 4 / 3;
  }
  .img-card.featured {
    grid-column: span 2;
    aspect-ratio: 16 / 7;
    background: var(--surface-2);
  }
  .img-card.featured img {
    background: var(--surface);
  }
  .img-card:hover {
    transform: translateY(-6px);
    box-shadow: var(--shadow-lg);
    border-color: var(--line-2);
  }
  .img-card img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    background: var(--surface-2);
    display: block;
    transition: transform 0.5s var(--ease);
  }
  .img-card:hover img {
    transform: scale(1.03);
  }
  .img-card .cap {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 10px 16px;
    font-family: "JetBrains Mono", monospace;
    font-size: 0.72rem;
    color: var(--ink-2);
    background: linear-gradient(to top, rgba(255,255,255,0.95), rgba(255,255,255,0));
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .img-card .cap .idx {
    color: var(--accent);
    font-weight: 600;
  }
  .img-card .zoom-hint {
    position: absolute;
    top: 12px;
    right: 12px;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: rgba(255,255,255,0.9);
    border: 1px solid var(--line);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    color: var(--ink-2);
    opacity: 0;
    transform: scale(0.8);
    transition: all 0.3s var(--ease);
  }
  .img-card:hover .zoom-hint {
    opacity: 1;
    transform: scale(1);
  }
  @media (max-width: 640px) {
    .img-card.featured { grid-column: span 1; aspect-ratio: 4/3; }
  }

  /* ============ 底部 ============ */
  footer {
    position: relative;
    z-index: 1;
    text-align: center;
    padding: 60px 40px 40px;
    border-top: 1px solid var(--line);
    color: var(--ink-3);
    font-size: 0.85rem;
  }
  footer .brand {
    font-family: "Fraunces", serif;
    font-size: 1.4rem;
    color: var(--ink);
    margin-bottom: 8px;
  }
  footer .env {
    font-family: "JetBrains Mono", monospace;
    font-size: 0.75rem;
    color: var(--ink-3);
    margin-top: 12px;
    letter-spacing: 0.02em;
  }

  /* ============ 回到顶部 ============ */
  .back-top {
    position: fixed;
    bottom: 32px;
    right: 32px;
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: var(--ink);
    color: var(--bg);
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    box-shadow: var(--shadow-md);
    opacity: 0;
    visibility: hidden;
    transform: translateY(16px);
    transition: all 0.3s var(--ease);
    z-index: 99;
  }
  .back-top.show {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
  }
  .back-top:hover {
    background: var(--accent);
    transform: translateY(-2px);
  }

  /* ============ 灯箱 ============ */
  .lightbox {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(20, 18, 15, 0.94);
    z-index: 1000;
    justify-content: center;
    align-items: center;
    cursor: zoom-out;
    opacity: 0;
    transition: opacity 0.3s;
  }
  .lightbox.active {
    display: flex;
    opacity: 1;
  }
  .lightbox img {
    max-width: 88vw;
    max-height: 86vh;
    object-fit: contain;
    border-radius: 8px;
    box-shadow: 0 30px 80px rgba(0,0,0,0.5);
    transform: scale(0.95);
    transition: transform 0.3s var(--ease);
  }
  .lightbox.active img { transform: scale(1); }
  .lightbox-close {
    position: absolute;
    top: 24px;
    right: 24px;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: rgba(255,255,255,0.1);
    color: #fff;
    border: 1px solid rgba(255,255,255,0.2);
    cursor: pointer;
    font-size: 1.3rem;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
  }
  .lightbox-close:hover { background: rgba(255,255,255,0.2); }
  .lb-nav {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.18);
    color: #fff;
    font-size: 1.4rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
    z-index: 2;
  }
  .lb-nav:hover { background: rgba(255,255,255,0.18); }
  .lb-prev { left: 28px; }
  .lb-next { right: 28px; }
  .lb-counter {
    position: absolute;
    bottom: 24px;
    left: 50%;
    transform: translateX(-50%);
    font-family: "JetBrains Mono", monospace;
    font-size: 0.8rem;
    color: rgba(255,255,255,0.6);
    letter-spacing: 0.1em;
  }

  @media (max-width: 768px) {
    .nav { padding: 14px 20px; }
    .nav-links { display: none; }
    .hero { padding: 100px 20px 60px; }
    .hero-stats { gap: 32px; }
    .hero-stat .num { font-size: 2.2rem; }
    main { padding: 40px 20px 80px; }
    .module-header { flex-direction: column; align-items: flex-start; gap: 12px; }
    .module-no { font-size: 3rem; }
    .module-desc { margin-left: 0; padding-left: 0; border-left: none; }
    .gallery { grid-template-columns: 1fr; }
  }
</style>
</head>
<body>

<div class="progress-bar" id="progressBar"></div>

<!-- 左侧粘性导航 -->
<nav class="side-nav" id="sideNav">
  {% for m in modules %}
  <a href="#{{ m.dir }}" data-target="{{ m.dir }}">
    <span class="sn-no">{{ m.no }}</span>
    <span class="sn-dot"></span>
    <span class="sn-label">{{ m.name }}</span>
  </a>
  {% endfor %}
</nav>

<!-- 导航 -->
<nav class="nav" id="nav">
  <div class="nav-logo"><span class="dot"></span>ML · Gallery</div>
  <ul class="nav-links">
    <li><a href="#overview">概览</a></li>
    <li><a href="#LinearRegression">线性回归</a></li>
    <li><a href="#NeuralNetwok">神经网络</a></li>
    <li><a href="#SVM">SVM</a></li>
    <li><a href="#PCA">PCA</a></li>
  </ul>
</nav>

<!-- Hero -->
<section class="hero" id="overview">
  <div class="hero-bg">
    <div class="hero-blob hero-blob-1"></div>
    <div class="hero-blob hero-blob-2"></div>
    <div class="hero-blob hero-blob-3"></div>
  </div>
  <div class="hero-eyebrow">Machine Learning · Python Implementation</div>
  <h1>经典机器学习算法<br><em>复现与可视化</em></h1>
  <p class="hero-sub">基于 lawlite19/MachineLearning_Python 的工程复现，涵盖 7 大经典算法的完整实现、运行结果与性能指标。</p>
  <div class="hero-stats">
    <div class="hero-stat"><div class="num">{{ modules|length }}<span>.</span></div><div class="label">算法模块</div></div>
    <div class="hero-stat"><div class="num">{{ modules|map(attribute='images')|map('length')|sum }}<span>+</span></div><div class="label">结果可视化</div></div>
    <div class="hero-stat"><div class="num">13<span>/13</span></div><div class="label">脚本运行成功</div></div>
  </div>
  <div class="hero-scroll">Scroll</div>
</section>

<!-- 主体 -->
<main>
  <div class="section-label">Algorithm Gallery</div>
  <h2 class="section-title">七大经典算法</h2>
  <p class="section-desc">从监督学习到无监督学习，从回归到聚类与降维，每个模块均已在本机环境完整跑通，点击图片可查看大图。</p>

  {% for m in modules %}
  <section class="module" id="{{ m.dir }}">
    <div class="module-header">
      <div class="module-no">{{ m.no }}</div>
      <div class="module-title-group">
        <h2>{{ m.name }}</h2>
        <div class="module-en">{{ m.en }}</div>
      </div>
      <p class="module-desc">{{ m.desc }}</p>
    </div>
    <div class="metrics">
      {% for k, v in m.metrics %}
      <div class="metric"><span class="k">{{ k }}</span><span class="v">{{ v }}</span></div>
      {% endfor %}
    </div>
    <div class="gallery">
      {% for img in m.images %}
      <div class="img-card{% if loop.first %} featured{% endif %}" onclick="openLightbox('{{ img }}', {{ loop.index0 }}, {{ m.images|length }})">
        <img src="{{ img }}" alt="{{ m.name }} 结果图 {{ loop.index }}" loading="lazy">
        <div class="zoom-hint">↗</div>
        <div class="cap"><span class="idx">Fig.{{ loop.index }}</span><span>result_{{ "%02d"|format(loop.index) }}.png</span></div>
      </div>
      {% else %}
      <div style="color:var(--ink-3); padding:20px; grid-column:1/-1;">暂无结果图</div>
      {% endfor %}
    </div>
  </section>
  {% endfor %}
</main>

<footer>
  <div class="brand">MachineLearning_Python</div>
  <div>经典机器学习算法的 Python 实现与复现</div>
  <div class="env">Python 3.11 · numpy 1.26 · scikit-learn 1.5 · matplotlib 3.9 · scipy 1.13</div>
</footer>

<button class="back-top" id="backTop" onclick="window.scrollTo({top:0,behavior:'smooth'})">↑</button>

<div class="lightbox" id="lightbox" onclick="closeLightbox()">
  <button class="lightbox-close" onclick="event.stopPropagation();closeLightbox()">✕</button>
  <button class="lb-nav lb-prev" onclick="event.stopPropagation();navLightbox(-1)">‹</button>
  <button class="lb-nav lb-next" onclick="event.stopPropagation();navLightbox(1)">›</button>
  <img id="lightbox-img" src="" alt="">
  <div class="lb-counter" id="lbCounter"></div>
</div>

<script>
  // 导航滚动效果 + 进度条
  const nav = document.getElementById('nav');
  const backTop = document.getElementById('backTop');
  const progressBar = document.getElementById('progressBar');
  const sideNavLinks = document.querySelectorAll('.side-nav a');
  const moduleSections = document.querySelectorAll('.module');

  function onScroll() {
    const y = window.scrollY;
    const docH = document.documentElement.scrollHeight - window.innerHeight;
    const pct = docH > 0 ? (y / docH) * 100 : 0;
    progressBar.style.width = pct + '%';
    nav.classList.toggle('scrolled', y > 40);
    backTop.classList.toggle('show', y > 500);

    // 滚动高亮当前模块
    let current = null;
    moduleSections.forEach(sec => {
      const rect = sec.getBoundingClientRect();
      if (rect.top <= 200 && rect.bottom > 200) current = sec.id;
    });
    sideNavLinks.forEach(a => {
      a.classList.toggle('active', a.dataset.target === current);
    });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // 模块滚动渐入
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -60px 0px' });
  document.querySelectorAll('.module').forEach(m => io.observe(m));

  // 灯箱（支持翻页）
  let lbImages = [];
  let lbIndex = 0;
  function openLightbox(src, idx, total) {
    // 收集当前模块所有图片
    const cards = document.querySelectorAll('.img-card');
    lbImages = Array.from(cards).map(c => c.querySelector('img').src);
    lbIndex = lbImages.indexOf(src) >= 0 ? lbImages.indexOf(src) : 0;
    // 由于多模块共享，用相对索引更简单：直接按点击的模块定位
    // 简化：用全局图片列表
    showLightboxImage();
    document.getElementById('lightbox').classList.add('active');
    document.body.style.overflow = 'hidden';
  }
  function showLightboxImage() {
    document.getElementById('lightbox-img').src = lbImages[lbIndex];
    document.getElementById('lbCounter').textContent = (lbIndex + 1) + ' / ' + lbImages.length;
  }
  function navLightbox(dir) {
    lbIndex = (lbIndex + dir + lbImages.length) % lbImages.length;
    showLightboxImage();
  }
  function closeLightbox() {
    document.getElementById('lightbox').classList.remove('active');
    document.body.style.overflow = '';
  }
  document.addEventListener('keydown', e => {
    if (!document.getElementById('lightbox').classList.contains('active')) return;
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowLeft') navLightbox(-1);
    if (e.key === 'ArrowRight') navLightbox(1);
  });
</script>
</body>
</html>
"""

if __name__ == "__main__":
    total_imgs = sum(len(get_module_images(m["dir"])) for m in MODULES)
    print(f"[ML Web] 模块数: {len(MODULES)}, 结果图总数: {total_imgs}")
    print("[ML Web] 启动网站: http://127.0.0.1:5050")
    app.run(host="127.0.0.1", port=5050, debug=False)
