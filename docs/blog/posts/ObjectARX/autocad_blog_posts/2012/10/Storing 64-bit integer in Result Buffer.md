---
title: "Storing 64-bit integer in Result Buffer"
date: 2012-10-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - DWG
  - DXF
description: "I cannot find a DXF code to store a 64-bit integer in the Extended Data. Is there any?"
author: Autodesk
---
# Storing 64-bit integer in Result Buffer

发布日期: 2012-10-01

原始链接: https://adndevblog.typepad.com/autocad/2012/10/storing-64-bit-integer-in-result-buffer.html

## 文章内容

By Marat Mirgaleev
Issue
I cannot find a DXF code to store a 64-bit integer in the Extended Data. Is there any?
Solution
No, there is no DXF code to indicate a 64-bit value in Extended Data (XData). It is by design, because earlier AutoCAD versions wouldn't be able to read such a DWG file.
One workaround for this is to split your 64-bit value into two 32-bit values (high 32-bits and low 32-bits) and precede them with a code of your choosing to indicate to your application that they should be combined to 64-bit values.
Another workaround is using XRecords instead of XData, since there is support of kDxfInt64 in XRecords. When saving the XRecords back to 2007 and earlier formats, the 64-bit XRecord opcodes are converted into round-trip XData that is attached to the XRecord objects.

