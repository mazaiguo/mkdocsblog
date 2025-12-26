---
title: CGridCtrl 详细使用文档
date: 2025-12-16
categories:
  - windows程序
tags:
  - ObjectARX
  - CGridCtrl 
  - MFC
description: CGridCtrl 详细使用文档
author: JerryMa
---

# CGridCtrl 详细使用文档

## 目录
- [1. 简介](#1-简介)
- [2. 快速开始](#2-快速开始)
- [3. 初始化和配置](#3-初始化和配置)
- [4. 数据操作](#4-数据操作)
- [5. 外观定制](#5-外观定制)
- [6. 编辑功能](#6-编辑功能)
- [7. 选择和焦点](#7-选择和焦点)
- [8. 排序和搜索](#8-排序和搜索)
- [9. 事件处理](#9-事件处理)
- [10. 高级功能](#10-高级功能)
- [11. 常用方法参考](#11-常用方法参考)
- [12. 完整示例](#12-完整示例)

---

## 简介

### 什么是 CGridCtrl

`CGridCtrl` 是一个功能强大的 MFC 网格控件，提供类似 Excel 的表格显示和编辑功能。它支持：

- ✅ 多行多列的表格显示
- ✅ 固定行/列（表头）
- ✅ 单元格编辑
- ✅ 行列调整大小
- ✅ 排序
- ✅ 颜色自定义
- ✅ 键盘和鼠标导航
- ✅ 拖放支持
- ✅ 打印支持

### 包含文件

```cpp
#include "GridCtrl_src/GridCtrl.h"

// 链接库（如果需要）
#pragma comment(lib, "GridCtrl.lib")
```

---

## 快速开始

### 基本步骤

```cpp
// 1. 在对话框头文件中声明
class CMyDialog : public CDialog
{
private:
    CGridCtrl m_grid;
};

// 2. 在资源文件中添加占位控件（可选）
// 或在 DoDataExchange 中绑定
void CMyDialog::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    DDX_Control(pDX, IDC_GRID, m_grid);
}

// 3. 在 OnInitDialog 中初始化
BOOL CMyDialog::OnInitDialog()
{
    CDialog::OnInitDialog();
    
    // 启用拖放
    m_grid.EnableDragAndDrop(TRUE);
    
    // 设置默认单元格背景色
    m_grid.GetDefaultCell(FALSE, FALSE)->SetBackClr(RGB(255, 255, 224));
    
    // 设置可编辑
    m_grid.SetEditable(TRUE);
    
    // 设置行列数
    m_grid.SetFixedRowCount(1);     // 表头行数
    m_grid.SetFixedColumnCount(1);  // 表头列数
    m_grid.SetRowCount(10);          // 总行数（包含表头）
    m_grid.SetColumnCount(5);        // 总列数（包含表头）
    
    return TRUE;
}
```

---

## 初始化和配置

### 创建网格

#### 方法1：通过资源文件（推荐）

1. 在对话框资源中添加一个 Custom Control
2. 设置 Class 为 `MFCGridCtrl`
3. 设置 ID 为 `IDC_GRID`
4. 使用 `DDX_Control` 绑定

```cpp
DDX_Control(pDX, IDC_GRID, m_grid);
```

#### 方法2：动态创建

```cpp
CRect rect(10, 10, 600, 400);
m_grid.Create(WS_CHILD | WS_VISIBLE | WS_BORDER | WS_TABSTOP, 
              rect, this, IDC_GRID);
```

### 设置行列数

```cpp
// 设置固定行列（表头）
m_grid.SetFixedRowCount(1);    // 1行表头
m_grid.SetFixedColumnCount(1);  // 1列行号

// 设置总行列数
m_grid.SetRowCount(10);         // 10行（包含表头）
m_grid.SetColumnCount(5);       // 5列（包含行号列）
```

### 设置列宽和行高

```cpp
// 设置列宽
m_grid.SetColumnWidth(0, 50);   // 第0列宽度50像素
m_grid.SetColumnWidth(1, 100);  // 第1列宽度100像素

// 设置行高
m_grid.SetRowHeight(0, 30);     // 第0行高度30像素
m_grid.SetRowHeight(1, 25);     // 第1行高度25像素

// 自动调整列宽以适应内容
m_grid.AutoSizeColumn(1);       // 自动调整第1列
m_grid.AutoSizeColumns();       // 自动调整所有列

// 扩展最后一列填充剩余空间
m_grid.ExpandLastColumn();

// 隐藏列（设置宽度为0）
m_grid.SetColumnWidth(0, 0);    // 隐藏第0列
```

### 基本属性设置

```cpp
// 是否可编辑
m_grid.SetEditable(TRUE);

// 是否显示网格线
m_grid.SetGridLines(TRUE);

// 允许用户调整大小
m_grid.SetRowResize(TRUE);      // 允许调整行高
m_grid.SetColumnResize(TRUE);   // 允许调整列宽

// 单行选择模式
m_grid.SetSingleRowSelection(TRUE);

// 固定行/列选择
m_grid.SetFixedRowSelection(TRUE);
m_grid.SetFixedColumnSelection(TRUE);

// 启用列隐藏
m_grid.EnableColumnHide(TRUE);

// 启用拖放
m_grid.EnableDragAndDrop(TRUE);
```

---

## 数据操作

### 设置单元格文本

```cpp
// 方法1：直接设置
m_grid.SetItemText(row, col, _T("文本内容"));

// 方法2：使用 GV_ITEM 结构
GV_ITEM item;
item.mask = GVIF_TEXT;
item.row = 1;
item.col = 2;
item.strText = _T("Hello");
m_grid.SetItem(&item);
```

### 获取单元格文本

```cpp
CString strText = m_grid.GetItemText(row, col);
```

### 设置表头

```cpp
// 设置列标题
for (int col = 0; col < m_grid.GetColumnCount(); col++)
{
    CString strHeader;
    strHeader.Format(_T("列 %d"), col);
    m_grid.SetItemText(0, col, strHeader);
}

// 设置固定列（行号）
for (int row = 0; row < m_grid.GetRowCount(); row++)
{
    CString strRowNum;
    strRowNum.Format(_T("%d"), row);
    m_grid.SetItemText(row, 0, strRowNum);
}
```

### 插入行

```cpp
// 在末尾添加行
int nNewRow = m_grid.InsertRow(_T(""));

// 在指定位置插入行
int nNewRow = m_grid.InsertRow(_T(""), 5);  // 在第5行位置插入

// 设置新行的数据
if (nNewRow >= 0)
{
    m_grid.SetItemText(nNewRow, 0, _T("数据1"));
    m_grid.SetItemText(nNewRow, 1, _T("数据2"));
    m_grid.SetItemText(nNewRow, 2, _T("数据3"));
}
```

### 插入列

```cpp
// 在末尾添加列
int nNewCol = m_grid.InsertColumn(_T("新列"));

// 在指定位置插入列
int nNewCol = m_grid.InsertColumn(_T("新列"), DT_CENTER|DT_VCENTER, 3);
```

### 删除行

```cpp
// 删除指定行
m_grid.DeleteRow(5);

// 删除所有非固定行（保留表头）
m_grid.DeleteNonFixedRows();

// 删除所有内容
m_grid.DeleteAllItems();
```

### 删除列

```cpp
// 删除指定列
m_grid.DeleteColumn(3);
```

### 批量设置数据

```cpp
// 循环设置多行数据
for (int row = 1; row < m_grid.GetRowCount(); row++)
{
    for (int col = 1; col < m_grid.GetColumnCount(); col++)
    {
        CString strValue;
        strValue.Format(_T("R%dC%d"), row, col);
        m_grid.SetItemText(row, col, strValue);
    }
}
```

---

## 外观定制

### 设置单元格颜色

```cpp
// 设置背景色
m_grid.SetItemBkColour(row, col, RGB(255, 255, 200));

// 设置前景色（文字颜色）
m_grid.SetItemFgColour(row, col, RGB(255, 0, 0));

// 批量设置整行颜色
for (int col = 0; col < m_grid.GetColumnCount(); col++)
{
    m_grid.SetItemBkColour(row, col, RGB(144, 238, 144));
    m_grid.SetItemFgColour(row, col, RGB(0, 0, 255));
}
```

### 设置单元格格式

```cpp
// 使用 GV_ITEM 设置多个属性
GV_ITEM item;
item.mask = GVIF_TEXT | GVIF_BKCLR | GVIF_FGCLR | GVIF_FORMAT;
item.row = 2;
item.col = 3;
item.strText = _T("格式化文本");
item.crBkClr = RGB(255, 255, 200);
item.crFgClr = RGB(255, 0, 0);
item.nFormat = DT_CENTER | DT_VCENTER | DT_SINGLELINE;  // 居中对齐
m_grid.SetItem(&item);
```

### 设置字体

```cpp
// 获取单元格
CGridCellBase* pCell = m_grid.GetCell(row, col);
if (pCell)
{
    // 创建字体
    CFont font;
    font.CreatePointFont(100, _T("Arial"));
    
    // 设置字体
    pCell->SetFont(&font);
}
```

### 设置表头样式

```cpp
// 设置固定行（表头）颜色
for (int col = 0; col < m_grid.GetColumnCount(); col++)
{
    m_grid.SetItemBkColour(0, col, RGB(70, 130, 180));  // 钢蓝色
    m_grid.SetItemFgColour(0, col, RGB(255, 255, 255)); // 白色文字
}

// 设置固定列（行号）颜色
for (int row = 0; row < m_grid.GetRowCount(); row++)
{
    m_grid.SetItemBkColour(row, 0, RGB(192, 192, 192));  // 灰色
}
```

### 设置默认样式

```cpp
// 设置默认单元格样式（影响新创建的单元格）
CGridDefaultCell* pDefCell = (CGridDefaultCell*)m_grid.GetDefaultCell(FALSE, FALSE);
if (pDefCell)
{
    pDefCell->SetBackClr(RGB(255, 255, 224));     // 浅黄色背景
    pDefCell->SetTextClr(RGB(0, 0, 0));           // 黑色文字
    pDefCell->SetFormat(DT_LEFT | DT_VCENTER);    // 左对齐，垂直居中
}
```

---

## 编辑功能

### 启用编辑

```cpp
// 启用/禁用编辑
m_grid.SetEditable(TRUE);

// 检查是否可编辑
BOOL bEditable = m_grid.IsEditable();

// 设置单个单元格是否可编辑
m_grid.SetItemState(row, col, m_grid.GetItemState(row, col) | GVIS_READONLY);
```

### 编程方式编辑

```cpp
// 进入编辑模式
CCellID cell(row, col);
m_grid.EnsureVisible(cell);
m_grid.SetFocusCell(cell);
m_grid.EditCell(cell);

// 结束编辑
m_grid.EndEditing();
```

### 编辑验证

```cpp
// 重写虚函数进行验证
class CMyGridCtrl : public CGridCtrl
{
protected:
    virtual BOOL ValidateEdit(int nRow, int nCol, LPCTSTR str)
    {
        // 验证输入
        CString strValue(str);
        
        // 例如：验证数字列
        if (nCol == 3)
        {
            int nValue = _ttoi(strValue);
            if (nValue < 0 || nValue > 100)
            {
                AfxMessageBox(_T("Please enter a value between 0 and 100!"));
                return FALSE;
            }
        }
        
        return TRUE;
    }
};
```

---

## 选择和焦点

### 设置焦点单元格

```cpp
// 设置焦点到指定单元格
CCellID cell(row, col);
m_grid.SetFocusCell(cell);

// 或直接指定行列
m_grid.SetFocusCell(row, col);

// 获取当前焦点单元格
CCellID focusCell = m_grid.GetFocusCell();
int row = focusCell.row;
int col = focusCell.col;
```

### 选择单元格

```cpp
// 选择单个单元格
m_grid.SetSelectedRange(row, col, row, col);

// 选择一行
m_grid.SetSelectedRange(row, 0, row, m_grid.GetColumnCount()-1);

// 选择一列
m_grid.SetSelectedRange(0, col, m_grid.GetRowCount()-1, col);

// 选择区域
m_grid.SetSelectedRange(startRow, startCol, endRow, endCol);

// 清除选择
m_grid.ResetSelectedRange();
```

### 获取选择范围

```cpp
// 获取选择的单元格范围
CCellRange selection = m_grid.GetSelectedCellRange();
int nMinRow = selection.GetMinRow();
int nMaxRow = selection.GetMaxRow();
int nMinCol = selection.GetMinCol();
int nMaxCol = selection.GetMaxCol();

// 检查单元格是否被选中
BOOL bSelected = m_grid.IsCellSelected(row, col);
```

### 确保可见

```cpp
// 滚动到指定单元格使其可见
m_grid.EnsureVisible(row, col);

// 检查单元格是否可见
BOOL bVisible = m_grid.IsCellVisible(row, col);
```

---

## 排序和搜索

### 排序

```cpp
// 按列排序（文本排序）
m_grid.SetSortColumn(1);            // 设置排序列
m_grid.SetSortAscending(TRUE);      // 设置升序
m_grid.SortTextItems(1, TRUE);      // 执行排序

// 数字排序
m_grid.SortItems(1, TRUE);          // 按第1列升序排序数字

// 自定义排序
m_grid.SortItems(1, TRUE, MyCompareFunc);
```

### 搜索文本

```cpp
// 在网格中搜索文本
CString strSearch = _T("查找内容");
BOOL bFound = FALSE;
int nFoundRow = -1;
int nFoundCol = -1;

for (int row = m_grid.GetFixedRowCount(); row < m_grid.GetRowCount(); row++)
{
    for (int col = m_grid.GetFixedColumnCount(); col < m_grid.GetColumnCount(); col++)
    {
        CString strCell = m_grid.GetItemText(row, col);
        if (strCell.Find(strSearch) >= 0)
        {
            bFound = TRUE;
            nFoundRow = row;
            nFoundCol = col;
            break;
        }
    }
    if (bFound) break;
}

if (bFound)
{
    // 定位到找到的单元格
    m_grid.SetFocusCell(nFoundRow, nFoundCol);
    m_grid.EnsureVisible(nFoundRow, nFoundCol);
    
    // 高亮显示
    m_grid.SetItemBkColour(nFoundRow, nFoundCol, RGB(255, 255, 0));
    m_grid.Refresh();
}
```

---

## 事件处理

### 常用通知消息

在父窗口的消息映射中添加：

```cpp
BEGIN_MESSAGE_MAP(CMyDialog, CDialog)
    ON_NOTIFY(GVN_BEGINLABELEDIT, IDC_GRID, OnGridBeginEdit)
    ON_NOTIFY(GVN_ENDLABELEDIT, IDC_GRID, OnGridEndEdit)
    ON_NOTIFY(NM_CLICK, IDC_GRID, OnGridClick)
    ON_NOTIFY(NM_DBLCLK, IDC_GRID, OnGridDblClick)
    ON_NOTIFY(GVN_SELCHANGED, IDC_GRID, OnGridSelChanged)
END_MESSAGE_MAP()
```

### 单元格编辑事件

```cpp
// 开始编辑
void CMyDialog::OnGridBeginEdit(NMHDR *pNotifyStruct, LRESULT* pResult)
{
    NM_GRIDVIEW* pItem = (NM_GRIDVIEW*)pNotifyStruct;
    
    int nRow = pItem->iRow;
    int nCol = pItem->iColumn;
    
    // 可以在这里限制某些单元格不能编辑
    if (nCol == 0)
    {
        *pResult = -1;  // 阻止编辑
        return;
    }
    
    *pResult = 0;
}

// 结束编辑
void CMyDialog::OnGridEndEdit(NMHDR *pNotifyStruct, LRESULT* pResult)
{
    NM_GRIDVIEW* pItem = (NM_GRIDVIEW*)pNotifyStruct;
    
    int nRow = pItem->iRow;
    int nCol = pItem->iColumn;
    
    CString strText = m_grid.GetItemText(nRow, nCol);
    
    // 处理编辑后的数据
    // 例如：保存到数据库
    
    *pResult = 0;
}
```

### 单击事件

```cpp
// 单击
void CMyDialog::OnGridClick(NMHDR *pNotifyStruct, LRESULT* pResult)
{
    NM_GRIDVIEW* pItem = (NM_GRIDVIEW*)pNotifyStruct;
    
    int nRow = pItem->iRow;
    int nCol = pItem->iColumn;
    
    TRACE(_T("Clicked cell [%d, %d]\n"), nRow, nCol);
    
    *pResult = 0;
}

// 双击
void CMyDialog::OnGridDblClick(NMHDR *pNotifyStruct, LRESULT* pResult)
{
    NM_GRIDVIEW* pItem = (NM_GRIDVIEW*)pNotifyStruct;
    
    int nRow = pItem->iRow;
    int nCol = pItem->iColumn;
    
    TRACE(_T("Double-clicked cell [%d, %d]\n"), nRow, nCol);
    
    *pResult = 0;
}
```

### 选择改变事件

```cpp
void CMyDialog::OnGridSelChanged(NMHDR *pNotifyStruct, LRESULT* pResult)
{
    NM_GRIDVIEW* pItem = (NM_GRIDVIEW*)pNotifyStruct;
    
    CCellID focusCell = m_grid.GetFocusCell();
    TRACE(_T("Selection changed to [%d, %d]\n"), focusCell.row, focusCell.col);
    
    *pResult = 0;
}
```

---

## 高级功能

### 虚拟模式（大数据量）

```cpp
// 启用虚拟模式
m_grid.SetVirtualMode(TRUE);

// 设置数据回调
m_grid.SetCallbackFunc(MyDataCallback, (LPARAM)this);

// 回调函数
BOOL CALLBACK MyDataCallback(GV_DISPINFO *pDispInfo, LPARAM lParam)
{
    CMyDialog* pDlg = (CMyDialog*)lParam;
    
    // 根据请求返回数据
    if (pDispInfo->item.mask & GVIF_TEXT)
    {
        CString strValue;
        strValue.Format(_T("R%dC%d"), 
                        pDispInfo->item.row, 
                        pDispInfo->item.col);
        pDispInfo->item.strText = strValue;
    }
    
    return TRUE;
}
```

### 合并单元格

```cpp
// 合并单元格范围
CCellRange range(1, 1, 3, 3);  // 从(1,1)到(3,3)
m_grid.SetCellRange(range);
```

### 冻结行列

```cpp
// 固定行（冻结表头）
m_grid.SetFixedRowCount(2);  // 冻结前2行

// 固定列
m_grid.SetFixedColumnCount(1);  // 冻结第1列
```

### 导出到CSV

```cpp
// 保存为CSV文件
m_grid.Save(_T("C:\\output.csv"), _T(','));

// 从CSV加载
m_grid.Load(_T("C:\\input.csv"), _T(','));
```

### 打印

```cpp
// 打印网格
m_grid.Print();
```

### 拖放

```cpp
// 启用拖放
m_grid.EnableDragAndDrop(TRUE);

// 允许行拖放
m_grid.SetRowDrag(TRUE);

// 允许列拖放
m_grid.SetColumnDrag(TRUE);
```

### 右键菜单

```cpp
// 在鼠标右键事件中显示菜单
void CMyDialog::OnGridRClick(NMHDR *pNotifyStruct, LRESULT* pResult)
{
    NM_GRIDVIEW* pItem = (NM_GRIDVIEW*)pNotifyStruct;
    
    // 创建上下文菜单
    CMenu menu;
    menu.CreatePopupMenu();
    menu.AppendMenu(MF_STRING, ID_MENU_COPY, _T("复制"));
    menu.AppendMenu(MF_STRING, ID_MENU_PASTE, _T("粘贴"));
    menu.AppendMenu(MF_STRING, ID_MENU_DELETE, _T("删除"));
    
    // 显示菜单
    CPoint point;
    GetCursorPos(&point);
    menu.TrackPopupMenu(TPM_LEFTALIGN | TPM_RIGHTBUTTON, 
                        point.x, point.y, this);
    
    *pResult = 0;
}
```

---

## 常用方法参考

### 行列操作

| 方法 | 说明 |
|------|------|
| `GetRowCount()` | 获取总行数 |
| `GetColumnCount()` | 获取总列数 |
| `SetRowCount(int)` | 设置总行数 |
| `SetColumnCount(int)` | 设置总列数 |
| `InsertRow(LPCTSTR, int)` | 插入行 |
| `InsertColumn(LPCTSTR, UINT, int)` | 插入列 |
| `DeleteRow(int)` | 删除行 |
| `DeleteColumn(int)` | 删除列 |
| `DeleteNonFixedRows()` | 删除所有数据行 |
| `DeleteAllItems()` | 删除所有内容 |

### 单元格操作

| 方法 | 说明 |
|------|------|
| `GetItemText(int, int)` | 获取单元格文本 |
| `SetItemText(int, int, LPCTSTR)` | 设置单元格文本 |
| `GetCell(int, int)` | 获取单元格对象 |
| `SetItem(GV_ITEM*)` | 设置单元格属性 |
| `GetItem(GV_ITEM*)` | 获取单元格属性 |
| `SetItemBkColour(int, int, COLORREF)` | 设置背景色 |
| `SetItemFgColour(int, int, COLORREF)` | 设置前景色 |
| `SetItemState(int, int, UINT)` | 设置单元格状态 |
| `GetItemState(int, int)` | 获取单元格状态 |

### 显示和刷新

| 方法 | 说明 |
|------|------|
| `Refresh()` | 刷新整个网格 |
| `RedrawCell(int, int)` | 重绘单个单元格 |
| `RedrawRow(int)` | 重绘一行 |
| `RedrawColumn(int)` | 重绘一列 |
| `EnsureVisible(int, int)` | 确保单元格可见 |
| `IsCellVisible(int, int)` | 检查单元格是否可见 |
| `SetRedraw(BOOL)` | 启用/禁用重绘 |

### 选择和焦点

| 方法 | 说明 |
|------|------|
| `GetFocusCell()` | 获取焦点单元格 |
| `SetFocusCell(int, int)` | 设置焦点单元格 |
| `GetSelectedCellRange()` | 获取选择范围 |
| `SetSelectedRange(int, int, int, int)` | 设置选择范围 |
| `ResetSelectedRange()` | 清除选择 |
| `IsCellSelected(int, int)` | 检查是否选中 |

### 编辑

| 方法 | 说明 |
|------|------|
| `SetEditable(BOOL)` | 设置是否可编辑 |
| `IsEditable()` | 检查是否可编辑 |
| `IsCellEditable(int, int)` | 检查单元格是否可编辑 |
| `EditCell(int, int)` | 进入编辑模式 |
| `EndEditing()` | 结束编辑 |

### 大小调整

| 方法 | 说明 |
|------|------|
| `GetColumnWidth(int)` | 获取列宽 |
| `SetColumnWidth(int, int)` | 设置列宽 |
| `GetRowHeight(int)` | 获取行高 |
| `SetRowHeight(int, int)` | 设置行高 |
| `AutoSizeColumn(int)` | 自动调整列宽 |
| `AutoSizeColumns()` | 自动调整所有列 |
| `AutoSizeRow(int)` | 自动调整行高 |
| `AutoSizeRows()` | 自动调整所有行 |
| `ExpandLastColumn()` | 扩展最后一列 |

### 排序

| 方法 | 说明 |
|------|------|
| `SortItems(int, BOOL)` | 数字排序 |
| `SortTextItems(int, BOOL)` | 文本排序 |
| `SetSortColumn(int)` | 设置排序列 |
| `GetSortColumn()` | 获取排序列 |
| `SetSortAscending(BOOL)` | 设置升序/降序 |
| `GetSortAscending()` | 获取排序方向 |

---

## 完整示例

### 完整的对话框实现

**MyDialog.h**

```cpp
#pragma once
#include "GridCtrl_src/GridCtrl.h"

class CMyDialog : public CDialog
{
    DECLARE_DYNAMIC(CMyDialog)

public:
    CMyDialog(CWnd* pParent = nullptr);
    virtual ~CMyDialog();

    enum { IDD = IDD_MY_DIALOG };

protected:
    virtual void DoDataExchange(CDataExchange* pDX);
    virtual BOOL OnInitDialog();

    DECLARE_MESSAGE_MAP()

private:
    CGridCtrl m_grid;
    
    void InitializeGrid();
    void LoadSampleData();
    
    afx_msg void OnBtnAdd();
    afx_msg void OnBtnRemove();
    afx_msg void OnBtnSort();
    afx_msg void OnGridEndEdit(NMHDR *pNotifyStruct, LRESULT* pResult);
};
```

**MyDialog.cpp**

```cpp
#include "stdafx.h"
#include "MyDialog.h"

IMPLEMENT_DYNAMIC(CMyDialog, CDialog)

BEGIN_MESSAGE_MAP(CMyDialog, CDialog)
    ON_BN_CLICKED(IDC_BTN_ADD, &CMyDialog::OnBtnAdd)
    ON_BN_CLICKED(IDC_BTN_REMOVE, &CMyDialog::OnBtnRemove)
    ON_BN_CLICKED(IDC_BTN_SORT, &CMyDialog::OnBtnSort)
    ON_NOTIFY(GVN_ENDLABELEDIT, IDC_GRID, OnGridEndEdit)
END_MESSAGE_MAP()

CMyDialog::CMyDialog(CWnd* pParent)
    : CDialog(IDD_MY_DIALOG, pParent)
{
}

CMyDialog::~CMyDialog()
{
}

void CMyDialog::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    DDX_Control(pDX, IDC_GRID, m_grid);
}

BOOL CMyDialog::OnInitDialog()
{
    CDialog::OnInitDialog();
    
    InitializeGrid();
    LoadSampleData();
    
    return TRUE;
}

void CMyDialog::InitializeGrid()
{
    // 启用基本功能
    m_grid.EnableDragAndDrop(TRUE);
    m_grid.SetEditable(TRUE);
    m_grid.SetRowResize(TRUE);
    m_grid.SetColumnResize(TRUE);
    m_grid.SetFixedRowSelection(TRUE);
    m_grid.SetFixedColumnSelection(TRUE);
    
    // 设置默认样式
    CGridDefaultCell* pDefCell = (CGridDefaultCell*)m_grid.GetDefaultCell(FALSE, FALSE);
    if (pDefCell)
    {
        pDefCell->SetBackClr(RGB(255, 255, 224));
        pDefCell->SetFormat(DT_LEFT | DT_VCENTER | DT_SINGLELINE);
    }
    
    // 设置行列数
    m_grid.SetFixedRowCount(1);
    m_grid.SetFixedColumnCount(1);
    m_grid.SetRowCount(2);      // 1 header + 1 empty data row
    m_grid.SetColumnCount(5);   // 1 row number + 4 data columns
    
    // 设置列标题
    m_grid.SetItemText(0, 0, _T(""));
    m_grid.SetItemText(0, 1, _T("Name"));
    m_grid.SetItemText(0, 2, _T("Age"));
    m_grid.SetItemText(0, 3, _T("City"));
    m_grid.SetItemText(0, 4, _T("Email"));
    
    // 设置列宽
    m_grid.SetColumnWidth(0, 50);
    m_grid.SetColumnWidth(1, 120);
    m_grid.SetColumnWidth(2, 60);
    m_grid.SetColumnWidth(3, 100);
    m_grid.SetColumnWidth(4, 200);
    
    // 设置表头样式
    for (int col = 0; col < m_grid.GetColumnCount(); col++)
    {
        m_grid.SetItemBkColour(0, col, RGB(70, 130, 180));
        m_grid.SetItemFgColour(0, col, RGB(255, 255, 255));
    }
}

void CMyDialog::LoadSampleData()
{
    // 示例数据
    struct Person {
        CString name;
        int age;
        CString city;
        CString email;
    } people[] = {
        {_T("Alice"), 25, _T("Beijing"), _T("alice@example.com")},
        {_T("Bob"), 30, _T("Shanghai"), _T("bob@example.com")},
        {_T("Charlie"), 28, _T("Guangzhou"), _T("charlie@example.com")},
    };
    
    // 添加数据
    for (int i = 0; i < _countof(people); i++)
    {
        int nRow = m_grid.InsertRow(_T(""));
        
        CString strRowNum;
        strRowNum.Format(_T("%d"), i + 1);
        m_grid.SetItemText(nRow, 0, strRowNum);
        m_grid.SetItemText(nRow, 1, people[i].name);
        m_grid.SetItemText(nRow, 2, CString(std::to_string(people[i].age).c_str()));
        m_grid.SetItemText(nRow, 3, people[i].city);
        m_grid.SetItemText(nRow, 4, people[i].email);
        
        // 设置行号列为灰色
        m_grid.SetItemBkColour(nRow, 0, RGB(192, 192, 192));
    }
    
    m_grid.Refresh();
}

void CMyDialog::OnBtnAdd()
{
    int nNewRow = m_grid.InsertRow(_T(""));
    
    if (nNewRow >= 0)
    {
        // 设置行号
        CString strRowNum;
        strRowNum.Format(_T("%d"), nNewRow);
        m_grid.SetItemText(nNewRow, 0, strRowNum);
        m_grid.SetItemBkColour(nNewRow, 0, RGB(192, 192, 192));
        
        // 设置焦点到第一个可编辑列
        m_grid.SetFocusCell(nNewRow, 1);
        m_grid.EnsureVisible(nNewRow, 1);
        m_grid.Refresh();
    }
}

void CMyDialog::OnBtnRemove()
{
    CCellID focusCell = m_grid.GetFocusCell();
    
    if (focusCell.row < m_grid.GetFixedRowCount())
    {
        AfxMessageBox(_T("Please select a data row!"), MB_ICONWARNING);
        return;
    }
    
    if (AfxMessageBox(_T("Delete selected row?"), MB_YESNO | MB_ICONQUESTION) == IDYES)
    {
        m_grid.DeleteRow(focusCell.row);
        m_grid.Refresh();
    }
}

void CMyDialog::OnBtnSort()
{
    // 按姓名列排序
    m_grid.SetSortColumn(1);
    m_grid.SetSortAscending(TRUE);
    m_grid.SortTextItems(1, TRUE);
    m_grid.Refresh();
}

void CMyDialog::OnGridEndEdit(NMHDR *pNotifyStruct, LRESULT* pResult)
{
    NM_GRIDVIEW* pItem = (NM_GRIDVIEW*)pNotifyStruct;
    
    int nRow = pItem->iRow;
    int nCol = pItem->iColumn;
    
    CString strValue = m_grid.GetItemText(nRow, nCol);
    
    // 这里可以进行数据验证和保存
    TRACE(_T("Cell [%d,%d] edited: %s\n"), nRow, nCol, strValue);
    
    *pResult = 0;
}
```

---

## 常见问题和解决方案

### 编译错误

**问题**: 找不到 GridCtrl.h

**解决**: 
- 确保将 GridCtrl 源码添加到项目中
- 在项目属性中添加包含目录

### 窗口创建失败

**问题**: `Create()` 返回 FALSE

**解决**:
- 检查窗口类是否已注册
- 确保父窗口句柄有效
- 检查样式标志是否正确

### 数据不显示

**问题**: 设置了数据但网格为空

**解决**:
- 调用 `Refresh()` 强制刷新
- 检查行列索引是否正确
- 确保设置了正确的行列数

### 编辑不工作

**问题**: 无法编辑单元格

**解决**:
- 调用 `SetEditable(TRUE)`
- 检查单元格是否设置为只读
- 确保窗口有焦点

### 性能问题

**问题**: 大数据量时很慢

**解决**:
- 使用虚拟模式
- 批量操作时调用 `SetRedraw(FALSE)`
- 操作完成后调用 `SetRedraw(TRUE)`

```cpp
m_grid.SetRedraw(FALSE);
// 批量操作
for (int i = 0; i < 10000; i++)
{
    // ...
}
m_grid.SetRedraw(TRUE);
m_grid.Refresh();
```

---

## 最佳实践

1. **初始化顺序**: 先设置行列数，再设置数据
2. **性能优化**: 大量操作时禁用重绘
3. **错误处理**: 检查返回值，处理异常情况
4. **资源管理**: 及时释放不需要的资源
5. **用户体验**: 提供视觉反馈，如高亮、颜色变化
6. **数据验证**: 在编辑结束时验证数据
7. **内存管理**: 对于大数据量使用虚拟模式

---

## 参考资源

- [CodeProject - The Ultimate Grid](https://www.codeproject.com/Articles/8/MFC-Grid-control)
- [GitHub - MFC-GridCtrl](https://github.com/jplommer/mfcgridctrl)
- MSDN - MFC 文档

---

**文档版本**: 1.0  
**最后更新**: 2025-12  
**作者**: AI Assistant


