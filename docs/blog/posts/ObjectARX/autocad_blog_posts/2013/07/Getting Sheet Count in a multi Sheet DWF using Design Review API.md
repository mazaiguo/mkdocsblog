---
title: "Getting Sheet Count in a multi Sheet DWF using Design Review API"
date: 2013-07-01
categories:
  - AutoCAD
tags:
  - API
description: "Following VBScript code snippet demonstrates how to get the sheet count and activating each of them for view. This code snippet is part of the "Vie..."
author: Autodesk
---
# Getting Sheet Count in a multi Sheet DWF using Design Review API

发布日期: 2013-07-01

原始链接: https://adndevblog.typepad.com/autocad/2013/07/getting-sheet-count-in-a-multi-sheet-dwf-using-design-review-api.html

## 文章内容

By Partha Sarkar
Following VBScript code snippet demonstrates how to get the sheet count and activating each of them for view. This code snippet is part of the "Viewer API Test" sample available in our Developer Center Page DWF Code samples.
function ShowPages
    dim page
 MsgBox Eview.Viewer.Pages.count()
    for each page in Eview.Viewer.Pages
      Eview.Viewer.Page = page.Name
      call Eview.Viewer.WaitForPageLoaded()
      MsgBox Eview.Viewer.Page.Name
    next
end function

## 评论

**内容**: steeloncall said...
Add required brands of steel materials online from our Steeloncall.com page. https://steeloncall.com/light-ms-rounds https://steeloncall.com/blog https://steeloncall.com/brands/simhadri-tmt
Reply
05/10/2020 at 11:21 PM

---
