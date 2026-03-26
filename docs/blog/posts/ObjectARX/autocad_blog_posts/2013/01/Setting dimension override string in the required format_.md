---
title: "Setting dimension override string in the required format?"
date: 2013-01-01
categories:
  - AutoCAD VBA
tags:
  - Dimension
  - Unicode
  - VBA
description: "How can I set the overridden text in the required units and format for a given dimension object? For example, I am using the "AddDimAligned" method..."
author: Autodesk
---
# Setting dimension override string in the required format?

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/setting-dimension-override-string-in-the-required-format.html

## 文章内容

By Daniel Du
Issue
How can I set the overridden text in the required units and format for a given dimension object? For example, I am using the "AddDimAligned" method to create a dimension between two lines, that is 3'-0". I then use the "TextOverride" property to override the dimension of 3'-0" to 1.667' but 1.667' is now a string. How can I convert the 1.667' value to display it in Architectural units as 1'-8"?
Solution
TextOverride is a string property and hence you can use data type conversion utilities to format the number to the style you want. In the following VBA example, RealToString method of Utility object is used to format the number to the required style. To control the suppression of zeros, set the DIMZIN system variable.
In this example the value of DIMZIN is set to 1. This will Include zero feet and precisely zero inches while performing the conversions using realToString. You can also use this string "<>" in the TextOverride to display the actual measurement.
For example, you can specify dimobj.TextOverride = "length = <> mm". This would set the override as "length = 10 mm" if the dimension's measurement is 10mm.
Sub f_test()
    Dim po_dim As AcadDimAligned
    Dim p1(2) As Double
    Dim p2(2) As Double
 
    p1(0) = 0 : p1(1) = 0
    p2(0) = 10 : p2(1) = 10
 
    po_dim = ThisDrawing.ModelSpace.AddDimAligned(p1, p2, p2)
    po_dim.TextOverride = ThisDrawing.Utility.RealToString(1.667 * 12,
                                                acArchitectural, 6)
 
    'set the DIMZIN to required format
    ThisDrawing.SetVariable("DIMZIN", 1)
 
    'to test the required format
    MsgBox(ThisDrawing.Utility.RealToString(48, acArchitectural, 6))
 
End Sub

