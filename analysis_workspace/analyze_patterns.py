#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析样本数据中的命名模式，为翻译原则提供补充建议
"""

import json
import re
from collections import defaultdict

def load_samples():
    """加载样本数据"""
    with open('samples_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_naming_patterns(samples):
    """分析命名模式"""
    patterns = {
        'nato_codenames': [],  # 北约代号
        'with_brackets': [],  # 包含方括号的名称
        'with_slashes': [],  # 包含斜杠（型号/规格）
        'manufacturer_names': [],  # 制造商名称
        'model_numbers': [],  # 型号编号
        'abbreviations': [],  # 缩写
        'chinese_designations': [],  # 中国装备代号
        'russian_designations': [],  # 俄罗斯装备代号
        'ship_designations': [],  # 舰船命名
        'with_parentheses': [],  # 包含圆括号的Comments
        'technical_specs': [],  # 技术规格
        'year_references': [],  # 包含年份
        'quantity_expressions': [],  # 数量表达
        'deprecated_items': [],  # 废弃项目
    }

    # 北约代号列表
    nato_codes = ['Flanker', 'Fulcrum', 'Fishbed', 'Frogfoot', 'Bear', 'Backfire',
                  'Blackjack', 'Hind', 'Hip', 'Havoc', 'Hokum', 'Flogger', 'Foxbat',
                  'Fishcan', 'Finback', 'Grumble', 'Guideline', 'Gimlet', 'Grail',
                  'Sovremenny', 'Udaloy', 'Krivak', 'Akula', 'Oscar', 'Typhoon',
                  'Yankee', 'Delta', 'Kilo', 'Victor', 'Charlie', 'Echo']

    # 制造商列表
    manufacturers = ['Boeing', 'Lockheed', 'Northrop', 'General', 'Raytheon',
                    'McDonnell', 'Sikorsky', 'Bell', 'Airbus', 'Dassault',
                    'Sukhoi', 'MiG', 'Tupolev', 'Antonov', 'Kamov', 'Mil',
                    'MTU', 'Rolls-Royce', 'Pratt', 'Whitney', 'Waukesha']

    for table, data in samples.items():
        for sample in data['samples']:
            name = sample['Name']
            comments = sample['Comments']

            # 检测北约代号
            for nato in nato_codes:
                if nato in name:
                    patterns['nato_codenames'].append({
                        'table': table,
                        'name': name,
                        'comments': comments
                    })
                    break

            # 检测方括号（通常是别名或技术型号）
            if '[' in name and ']' in name:
                patterns['with_brackets'].append({
                    'table': table,
                    'name': name,
                    'comments': comments
                })

            # 检测斜杠（口径/规格）
            if '/' in name and re.search(r'\d+mm/', name):
                patterns['with_slashes'].append({
                    'table': table,
                    'name': name,
                    'comments': comments
                })

            # 检测制造商名称
            for mfr in manufacturers:
                if mfr in name:
                    patterns['manufacturer_names'].append({
                        'table': table,
                        'name': name,
                        'manufacturer': mfr,
                        'comments': comments
                    })
                    break

            # 检测中国装备代号
            if re.search(r'^(J|JH|H|Y|Z|Q|K|JZ)-\d+', name) or \
               re.search(r'Type \d+', name) or \
               re.search(r'(HQ|PL|YJ|CJ|DF|CSS)-', name):
                patterns['chinese_designations'].append({
                    'table': table,
                    'name': name,
                    'comments': comments
                })

            # 检测俄罗斯装备代号
            if re.search(r'^(Su|MiG|Tu|Il|An|Mi|Ka)-\d+', name) or \
               re.search(r'Pr\.\d+', name) or \
               re.search(r'(PLA|SS|SA|AT)-', name):
                patterns['russian_designations'].append({
                    'table': table,
                    'name': name,
                    'comments': comments
                })

            # 检测舰船命名（编号 + 名称）
            if table == 'DataShip' and re.search(r'^[A-Z]+\s+\d+\s+', name):
                patterns['ship_designations'].append({
                    'table': table,
                    'name': name,
                    'comments': comments
                })

            # 检测Comments中的圆括号
            if '(' in comments and ')' in comments:
                patterns['with_parentheses'].append({
                    'table': table,
                    'name': name,
                    'comments': comments
                })

            # 检测年份
            if re.search(r'\b(19|20)\d{2}\b', comments):
                patterns['year_references'].append({
                    'table': table,
                    'name': name,
                    'comments': comments
                })

            # 检测数量表达
            if re.search(r'\d+x', comments):
                patterns['quantity_expressions'].append({
                    'table': table,
                    'name': name,
                    'comments': comments
                })

            # 检测废弃项目
            if 'DEPRECATED' in name.upper() or 'DEPRECATED' in comments.upper() or \
               'Cancelled' in comments or 'Retired' in comments:
                patterns['deprecated_items'].append({
                    'table': table,
                    'name': name,
                    'comments': comments
                })

    return patterns

def generate_statistics(patterns):
    """生成统计信息"""
    stats = {}
    for pattern_type, items in patterns.items():
        stats[pattern_type] = len(items)
    return stats

def save_analysis(patterns, stats):
    """保存分析结果"""
    # 保存详细的模式分析
    with open('pattern_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(patterns, f, ensure_ascii=False, indent=2)

    # 保存易读的分析报告
    with open('pattern_analysis_report.txt', 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("样本数据命名模式分析报告\n")
        f.write("="*80 + "\n\n")

        f.write("统计摘要:\n")
        f.write("-"*80 + "\n")
        for pattern_type, count in stats.items():
            f.write(f"{pattern_type}: {count} 个样本\n")

        f.write("\n\n")

        # 详细列出每种模式的示例
        for pattern_type, items in patterns.items():
            if items:
                f.write("="*80 + "\n")
                f.write(f"模式: {pattern_type}\n")
                f.write(f"样本数: {len(items)}\n")
                f.write("="*80 + "\n\n")

                # 只显示前10个示例
                for i, item in enumerate(items[:10], 1):
                    f.write(f"{i}. [{item['table']}]\n")
                    f.write(f"   Name: {item['name']}\n")
                    if item['comments']:
                        f.write(f"   Comments: {item['comments']}\n")
                    f.write("\n")

                if len(items) > 10:
                    f.write(f"   ... 还有 {len(items) - 10} 个样本\n\n")

def main():
    print("加载样本数据...")
    samples = load_samples()

    print("分析命名模式...")
    patterns = analyze_naming_patterns(samples)

    print("生成统计信息...")
    stats = generate_statistics(patterns)

    print("保存分析结果...")
    save_analysis(patterns, stats)

    print("\n分析完成!")
    print(f"详细分析已保存到: pattern_analysis.json")
    print(f"分析报告已保存到: pattern_analysis_report.txt")

    print("\n统计摘要:")
    print("-"*60)
    for pattern_type, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"{pattern_type:30s}: {count:4d} 个样本")

if __name__ == '__main__':
    main()
