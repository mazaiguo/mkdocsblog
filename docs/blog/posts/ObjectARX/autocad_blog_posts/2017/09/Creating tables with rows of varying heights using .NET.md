---
title: "Creating tables with rows of varying heights using .NET"
date: 2017-09-01
categories:
  - AutoCAD .NET
tags:
  - .NET
description: "Creating table using the Table.InsertColumns and Table.InsertRows is quite tricky and below are certain scenarios that can be useful :"
author: Autodesk
---
# Creating tables with rows of varying heights using .NET

发布日期: 2017-09-01

原始链接: https://adndevblog.typepad.com/autocad/2017/09/creating-tables-and-tables-with-rows-of-varying-heights-using-net-.html

## 文章内容

By Deepak Nadig
Creating table using the Table.InsertColumns and Table.InsertRows is quite tricky and below are certain scenarios that can be useful :
Scenario 1: Using only table.InsertColumns :
Along with the specified number of columns, a single default row(without cells) is created at row index 0.
Scenario 2: Using only table.InsertRows :
Along with the specified number of rows,a single default column is created (with cells) at column index 0.
for example, table.InsertRows(0, 5, 3); creates table as shown below: 
         Scenario 3: Using index to create rows or columns :
Here, the method is table.InsertRows(int row,double height,int rows)
int row = row index
double height = rows(exculding default row)
int rows = number of rows inserted
As in the above example, table.InsertRows(0, 5, 3); creates a table with 4 rows( 3 + 1 default row) and 1 column at index 0.
Since first parameter(index) is 0, every row is inserted at position 0 and pushes the previously inserted row(if any) below. So we can find the default row at the bottom most position after creation.
Scenario 4:  We can use table.InsertRows in a loop to create rows of varying height :
Rows of varying height can be created as follows :            
List<double> rowHeight = new List<double>();
rowHeight.Add(10);
rowHeight.Add(20);
rowHeight.Add(30);
int nRows = rowHeight.Count;
for (int iRow = 0; iRow < nRows; iRow++)
{
    table.InsertRows(0, rowHeight[iRow], 1);
}
 Image of the table created for above code :
          NOTE : the default row and column can be deleted if not required using DeleteColumns and DeleteRows API

