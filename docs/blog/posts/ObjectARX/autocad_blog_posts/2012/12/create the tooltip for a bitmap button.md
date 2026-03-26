---
title: "create the tooltip for a bitmap button"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - CUI
  - Unicode
description: "I have created a CAcUiBitmapButton. How do I create the tooltip text that"
author: Autodesk
---
# create the tooltip for a bitmap button

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/create-the-tooltip-for-a-bitmap-button.html

## 文章内容

By Xiaodong Liang
Issue
I have created a CAcUiBitmapButton. How do I create the tooltip text that
displays when the cursor is placed over the button?
Solution
CAcUiBitmapButton has implemented everything necessary for doing this; you only need to provide the tooltip string within the caption, such as SAMP|Sample Button1.
Notice the SAMP before the vertical bar is the bitmap's resource ID name. This is when you design the dialog button and set the properties. Also, make sure you choose owner draw style for the button.
In addition, you can create multiple lines of tooltip by overriding OnGetTipText() and modifying the reference parameter to the text string you want.
To test these approaches, the attached sample application has two separate buttons; one uses CAcUiBitmapButton and the other is derived from CAdUiOwnerDrawButton. In addition, it shows how to draw a text button that changes it appearance when it is clicked. Note that this approach also applies to all CAxUiWhatever control classes, such as CAcUiColorComboBox, CAcUiAngleComboBox, CAcUiAngleEdit, and so on.
Download Create_tooltip_bitmap_button_VS2008

