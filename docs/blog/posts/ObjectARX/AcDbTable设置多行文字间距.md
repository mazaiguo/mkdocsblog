---
title: AcDbTable设置多行文字的行间距
date: 2025-12-08
categories:
  - windows程序
tags:
  - ObjectARX
  - AcDbTable
description: AcDbTable设置多行文字的行间距
author: JerryMa
---

# AcDbTable设置多行文字的行间距

## 直接在文字字符串中填写\pse格式

```cpp
// 全局常量 —— 直接改这里就行
const double DEFAULT_TEXT_HEIGHT_MM = 4.0;    // 你要求的全图默认字高 4.0 mm
const double DEFAULT_ROW_HEIGHT_MM = 12.0;    // 推荐行高（可根据需要调大）
double FactorToExactMM(double factor)
{
    // 字高 4.0mm 的情况下，各倍数对应的真实毫米距离（已精确计算）
    const double h = 4.0;
    return factor * h * (5.0 / 3.0);    // AutoCAD 内部单倍行距系数正是 5/3
}

// 在你的代码里直接这样写（推荐封装成函数）：
void SetCellTextWithLineSpacing(AcDbTable* pTable, int row, int col,
    double lineSpacingFactor, const ACHAR* text)
{
    double distMM = FactorToExactMM(lineSpacingFactor);

    AcString s;
    // 关键！！必须用 \pse + 数值，且数值要足够精确（建议保留2~3位小数）
    s.format(L"\\pse%.3f;%s\\P第2行文字\\P第3行文字", distMM, text);

    pTable->setTextString(row, col, s);
}

static void Cmd_CreateTable40()
{
    AcDbDatabase* pDb = acdbHostApplicationServices()->workingDatabase();
    if (!pDb) return;

    AcDbBlockTable* pBT = nullptr;
    pDb->getBlockTable(pBT, AcDb::kForRead);

    AcDbBlockTableRecord* pMS = nullptr;
    pBT->getAt(ACDB_MODEL_SPACE, pMS, AcDb::kForWrite);
    pBT->close();

    AcDbTable* pTable = new AcDbTable();
    pTable->setSize(9, 4);                          // 9 行演示不同行距

    // 全局统一设置字高 4.0 mm
    pTable->setTextHeight(DEFAULT_TEXT_HEIGHT_MM);
    pTable->setColumnWidth(1, 100.0);
    // 所有行统一行高（必须大于文字+行距，否则会被压扁）
    for (int i = 0; i < 9; ++i)
        pTable->setRowHeight(i, DEFAULT_ROW_HEIGHT_MM);

    pTable->generateLayout();

    //AcString s;
    pTable->setTextString(0, 1, L"默认行距（强制Exactly模式）\n第2行文字\n第3行文字");
    // 直接写死也行（字高4.0mm 时对应的精确值）：
    // 正确！字高 4.0 mm 时真正的“1.15 倍”视觉效果
    pTable->setTextString(1, 1, L"\\pse1.15;1.15 倍观感（非常紧凑微松）\\P第2行文字\\P第3行文字");
    pTable->setTextString(2, 1, L"\\pse1.3;1.3 倍观感（推荐）\\P第2行文字\\P第3行文字");
    pTable->setTextString(3, 1, L"\\pse1.5;1.5 倍观感（最舒适）\\P第2行文字\\P第3行文字");
    pTable->setTextString(4, 1, L"\\pse1.8;1.8 倍观感（宽松）\\P第2行文字\\P第3行文字");
    pTable->setTextString(5, 1, L"\\pse2.0;2.0 倍观感（双倍）\\P第2行文字\\P第3行文字");

    // 加入模型空间
    pMS->appendAcDbEntity(pTable);
    pTable->close();
    pMS->close();

    acutPrintf(L"\n【字高 4.0 mm 表格创建完成】共 8 种行距演示，请放大查看！");
    acutPrintf(L"\n输入命令：TABLE40 即可重复运行");
}
```

![image-20251208172139573](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2025/12/8_17_21_42_20251208-image-20251208172139573.png)