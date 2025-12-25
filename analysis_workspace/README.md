# 翻译原则分析工作目录

本目录包含用于分析数据库样本并补充翻译原则的所有文件。

## 目录结构

```
analysis_workspace/
├── README.md                      # 本说明文件
├── extract_samples.py             # 样本数据抽取脚本
├── analyze_patterns.py            # 命名模式分析脚本
├── samples_data.json              # 样本数据（JSON格式）
├── samples_data.txt               # 样本数据（易读文本格式）
├── pattern_analysis.json          # 模式分析结果（JSON格式）
└── pattern_analysis_report.txt    # 模式分析报告（易读文本格式）
```

## 文件说明

### 1. extract_samples.py
**功能**：从数据库中抽取样本数据

**使用方法**：
```bash
cd analysis_workspace
python3 extract_samples.py
```

**输出**：
- `samples_data.json` - JSON格式的样本数据
- `samples_data.txt` - 易读的文本格式样本数据

**抽取策略**：
- 从14个指定表中抽取数据
- 每个表随机抽取30条记录
- 只抽取Name和Comments字段
- 过滤掉Name为空的记录

### 2. analyze_patterns.py
**功能**：分析样本数据中的命名模式和结构

**使用方法**：
```bash
cd analysis_workspace
python3 analyze_patterns.py
```

**输出**：
- `pattern_analysis.json` - JSON格式的分析结果
- `pattern_analysis_report.txt` - 易读的分析报告

**分析维度**：
- 北约代号（NATO Codenames）
- 方括号结构（Bracket Notations）
- 口径/规格格式（Caliber/Specification）
- 制造商名称（Manufacturer Names）
- 中国装备代号（Chinese Designations）
- 俄罗斯装备代号（Russian Designations）
- 舰船命名规则（Ship Designations）
- 年份信息（Year References）
- 数量表达（Quantity Expressions）
- 状态标识（Deprecated/Cancelled Items）

### 3. samples_data.json
**内容**：从数据库抽取的390条样本数据（JSON格式）

**结构**：
```json
{
  "TableName": {
    "total_count": 总记录数,
    "sample_count": 样本数量,
    "has_comments": 是否有Comments字段,
    "samples": [
      {
        "Name": "条目名称",
        "Comments": "注释内容"
      }
    ]
  }
}
```

### 4. samples_data.txt
**内容**：样本数据的易读文本版本

**用途**：便于人工阅读和审查样本数据

### 5. pattern_analysis.json
**内容**：命名模式分析的详细结果（JSON格式）

**结构**：按模式类型分类，每个模式包含所有匹配的样本

### 6. pattern_analysis_report.txt
**内容**：命名模式分析的易读报告

**包含**：
- 统计摘要
- 每种模式的示例（显示前10条）
- 样本数量统计

## 分析结果摘要

基于390条样本的分析结果：

| 模式类型 | 样本数 | 占比 |
|---------|--------|------|
| 包含方括号 | 127 | 32.6% |
| 年份信息 | 42 | 10.8% |
| 数量表达 | 28 | 7.2% |
| 俄罗斯装备 | 26 | 6.7% |
| 中国装备 | 21 | 5.4% |
| 北约代号 | 18 | 4.6% |
| 口径/规格 | 18 | 4.6% |
| 舰船命名 | 14 | 3.6% |
| 状态标识 | 6 | 1.5% |
| 制造商名称 | 3 | 0.8% |

## 数据库表覆盖

分析涵盖以下14个表（注：DataSatelite表在数据库中不存在）：

1. DataAircraft - 飞机（2417条记录，抽取30条）
2. DataShip - 舰船（1807条记录，抽取30条）
3. DataSubmarine - 潜艇（265条记录，抽取30条）
4. DataFacility - 设施（4575条记录，抽取30条）
5. DataGroundUnit - 地面单位（465条记录，抽取30条）
6. DataWeapon - 武器（4436条记录，抽取30条）
7. DataSensor - 传感器（7246条记录，抽取30条）
8. DataMount - 挂载点（4130条记录，抽取30条）
9. DataLoadout - 挂载配置（33788条记录，抽取30条）
10. DataComm - 通信系统（502条记录，抽取30条）
11. DataMagazine - 弹药库（1730条记录，抽取30条）
12. DataWarhead - 弹头（1363条记录，抽取30条）
13. DataPropulsion - 推进系统（4125条记录，抽取30条）

## 如何使用这些文件

### 查看样本数据
```bash
# 查看文本格式的样本
cat samples_data.txt | less

# 或使用你喜欢的编辑器
vim samples_data.txt
```

### 查看分析报告
```bash
# 查看分析报告
cat pattern_analysis_report.txt | less
```

### 重新生成分析
```bash
# 如果需要重新抽取样本
python3 extract_samples.py

# 重新分析模式
python3 analyze_patterns.py
```

## 基于分析的翻译原则补充

根据这些分析结果，我们对原有的11条翻译原则进行了补充，新增了以下内容：

- **原则12**：方括号内容的处理原则
- **原则13**：北约代号的处理
- **原则14**：口径/规格格式的处理
- **原则15**：中国装备代号的处理
- **原则16**：俄罗斯装备代号的处理
- **原则17**：舰船命名规则
- **原则18**：数量表达式的处理
- **原则19**：年份和时间信息的处理
- **原则20**：军事缩写词典
- **原则21**：技术状态标识的处理
- **原则22**：复合命名的优先级

详见根目录下的《更新后的翻译原则.md》文档。

---

**创建日期**：2025-12-25
**数据源**：DB3K_513-精简.db3
**Python版本**：3.x
