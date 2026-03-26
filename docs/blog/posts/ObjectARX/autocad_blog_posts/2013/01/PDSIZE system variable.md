---
title: "PDSIZE system variable"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "PDSIZE system variable sets the display size for point objects."
author: Autodesk
---
# PDSIZE system variable

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/pdsize-system-variable.html

## 文章内容

By Virupaksha Aithal
PDSIZE system variable sets the display size for point objects.
If the value is 0, then point size is 5 percent of the drawing area height. If the pdsize is greater then zero, then the same value is used to draw the point. If the pdsize is less then zero, then the value represent the percentage of the viewport size.
[CommandMethod("pdsizeTest")]
public static void pdsizeTest()
{
    //set pdmode so that point is drawn..
    Application.SetSystemVariable("pdmode", 2);
      Document acDoc = Application.DocumentManager.MdiActiveDocument;
    PromptDoubleOptions options =
                     new PromptDoubleOptions("Provide point size");
      PromptDoubleResult result = acDoc.Editor.GetDouble(options);
      if (result.Status != PromptStatus.OK)
        return;
      Application.SetSystemVariable("pdsize", result.Value);
}

