# -*- coding: utf-8 -*-
"""
批量复现运行器：
1. 强制 matplotlib 使用 Agg 后端（不弹窗）
2. patch plt.show -> 自动 savefig 到 result_*.png
3. 按模块逐个运行脚本并捕获 stdout
用法: python run_all.py
"""
import os
import sys
import io
import contextlib
import traceback

os.environ['MPLBACKEND'] = 'Agg'
os.environ['PYTHONIOENCODING'] = 'utf-8'

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# patch plt.show 以自动保存图片
_fig_counter = {'n': 0}
_orig_show = plt.show
def _patched_show(*args, **kwargs):
    _fig_counter['n'] += 1
    try:
        fig = plt.gcf()
        out = f'result_{_fig_counter["n"]:02d}.png'
        fig.savefig(out, dpi=100, bbox_inches='tight')
        print(f'  [saved {out}]')
    except Exception as e:
        print(f'  [savefig failed: {e}]')
    plt.close('all')
    return _orig_show(*args, **kwargs)
plt.show = _patched_show

# 待运行脚本
SCRIPTS = [
    ('LinearRegression', 'LinearRegression.py'),
    ('LinearRegression', 'LinearRegression_scikit-learn.py'),
    ('LogisticRegression', 'LogisticRegression.py'),
    ('LogisticRegression', 'LogisticRegression_scikit-learn.py'),
    ('LogisticRegression', 'LogisticRegression_OneVsAll.py'),
    ('LogisticRegression', 'LogisticRegression_OneVsAll_scikit-learn.py'),
    ('NeuralNetwok', 'NeuralNetwork.py'),
    ('SVM', 'SVM_scikit-learn.py'),
    ('K-Means', 'K-Menas.py'),
    ('K-Means', 'K-Means_scikit-learn.py'),
    ('PCA', 'PCA.py'),
    ('PCA', 'PCA_scikit-learn.py'),
    ('AnomalyDetection', 'AnomalyDetection.py'),
]

ROOT = os.path.dirname(os.path.abspath(__file__))
results = []

for folder, name in SCRIPTS:
    cwd = os.path.join(ROOT, folder)
    script_path = os.path.join(cwd, name)
    print(f'\n{"="*70}')
    print(f'RUN: {folder}/{name}')
    print('='*70)
    _fig_counter['n'] = 0
    old_cwd = os.getcwd()
    os.chdir(cwd)
    # 为每个脚本重置 figure
    plt.close('all')
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            with open(name, 'r', encoding='utf-8') as f:
                code = compile(f.read(), name, 'exec')
                exec(code, {'__name__': '__main__', '__file__': script_path})
        out = buf.getvalue()
        print(out)
        results.append((folder, name, 'OK', out))
    except Exception as e:
        out = buf.getvalue()
        print(out)
        tb = traceback.format_exc()
        print(f'ERROR: {e}\n{tb}')
        results.append((folder, name, f'FAIL: {e}', out + tb))
    finally:
        os.chdir(old_cwd)

# 汇总
print(f'\n{"="*70}')
print('汇总')
print('='*70)
ok = sum(1 for r in results if r[2] == 'OK')
fail = len(results) - ok
print(f'成功: {ok} / {len(results)}    失败: {fail}')
for folder, name, status, _ in results:
    print(f'  [{status[:4]:>4}] {folder}/{name}')
