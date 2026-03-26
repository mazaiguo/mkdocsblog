---
title: "AutoCAD OEM Error Message “This object contains too many unknown fonts and cannot be accurately represented within the editor”"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - OEM
  - Unicode
description: "When I call either .MTEXT for new text or .DDEDIT on existing text I get the"
author: Autodesk
---
# AutoCAD OEM Error Message “This object contains too many unknown fonts and cannot be accurately represented within the editor”

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/autocad-oem-error-message-this-object-contains-too-many-unknown-fonts-and-cannot-be-accurately-represented-within-the-editor.html

## 文章内容

by Fenton Webb
Issue
When I call either ._MTEXT for new text or ._DDEDIT on existing text I get the
error message:
"This object contains too many unknown fonts and cannot be accurately
represented within the editor."
Solution
You need to copy the file mtextmap.ini into the same directory as acmted.arx in-order for it to work properly.

