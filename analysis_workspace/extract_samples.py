#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从数据库中抽取样本数据用于分析翻译原则
"""

import sqlite3
import json
import random

# 数据库文件路径
DB_PATH = '../DB3K_513-精简.db3'

# 需要分析的表
TABLES = [
    'DataAircraft', 'DataShip', 'DataSubmarine', 'DataFacility',
    'DataGroundUnit', 'DataSatelite', 'DataWeapon', 'DataSensor',
    'DataMount', 'DataLoadout', 'DataComm', 'DataMagazine',
    'DataWarhead', 'DataPropulsion'
]

# 每个表抽取的样本数量
SAMPLE_SIZE = 30

def extract_samples():
    """从数据库中抽取样本"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    all_samples = {}

    for table in TABLES:
        try:
            # 检查表是否存在
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if not cursor.fetchone():
                print(f"表 {table} 不存在，跳过...")
                continue

            # 获取表结构
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]

            # 检查是否有Name和Comments字段
            has_name = 'Name' in column_names
            has_comments = 'Comments' in column_names

            if not has_name:
                print(f"表 {table} 没有Name字段，跳过...")
                continue

            # 构建查询语句
            if has_comments:
                query = f"SELECT Name, Comments FROM {table} WHERE Name IS NOT NULL"
            else:
                query = f"SELECT Name FROM {table} WHERE Name IS NOT NULL"

            cursor.execute(query)
            rows = cursor.fetchall()

            # 随机抽取样本
            if len(rows) > SAMPLE_SIZE:
                samples = random.sample(rows, SAMPLE_SIZE)
            else:
                samples = rows

            # 保存样本
            table_samples = []
            for row in samples:
                if has_comments:
                    table_samples.append({
                        'Name': row[0],
                        'Comments': row[1] if row[1] else ''
                    })
                else:
                    table_samples.append({
                        'Name': row[0],
                        'Comments': ''
                    })

            all_samples[table] = {
                'total_count': len(rows),
                'sample_count': len(samples),
                'has_comments': has_comments,
                'samples': table_samples
            }

            print(f"从表 {table} 抽取了 {len(samples)} 条样本（总共 {len(rows)} 条）")

        except Exception as e:
            print(f"处理表 {table} 时出错: {e}")
            continue

    conn.close()

    return all_samples

def save_samples(samples):
    """保存样本数据"""
    # 保存为JSON格式
    with open('samples_data.json', 'w', encoding='utf-8') as f:
        json.dump(samples, f, ensure_ascii=False, indent=2)

    # 保存为易读的文本格式
    with open('samples_data.txt', 'w', encoding='utf-8') as f:
        for table, data in samples.items():
            f.write(f"\n{'='*80}\n")
            f.write(f"表名: {table}\n")
            f.write(f"总数: {data['total_count']}, 样本数: {data['sample_count']}, 有Comments字段: {data['has_comments']}\n")
            f.write(f"{'='*80}\n\n")

            for i, sample in enumerate(data['samples'], 1):
                f.write(f"{i}. Name: {sample['Name']}\n")
                if sample['Comments']:
                    f.write(f"   Comments: {sample['Comments']}\n")
                f.write("\n")

def main():
    print("开始从数据库抽取样本数据...")
    samples = extract_samples()

    print("\n保存样本数据...")
    save_samples(samples)

    print(f"\n完成！共处理了 {len(samples)} 个表")
    print("样本数据已保存到:")
    print("  - samples_data.json (JSON格式)")
    print("  - samples_data.txt (文本格式)")

if __name__ == '__main__':
    main()
