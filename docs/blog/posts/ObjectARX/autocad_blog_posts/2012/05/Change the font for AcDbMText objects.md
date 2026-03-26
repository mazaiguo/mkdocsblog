---
title: "Change the font for AcDbMText objects"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Unicode
description: "Changing the font in the TextStyleTableRecord which this object uses, changes the font of all the AcDbMText objects that use this text style in the..."
author: Autodesk
---
# Change the font for AcDbMText objects

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/change-the-font-for-acdbmtext-objects.html

## 文章内容

By Balaji Ramamoorthy
Changing the font in the TextStyleTableRecord which this object uses, changes the font of all the AcDbMText objects that use this text style in the drawing. To change the font of a particular AcDbMText object, use the MText format codes.
You can apply formatting to individual words or characters, such as underlining text, add a line over text, or create stacked text. You also can change the color, font, and text height, and the spaces between text characters or increase the width of the characters themselves.
The MText format codes are listed in the AutoCAD online help under "Format Multiline Text in an Alternate Text Editor". To change the font, use the \F format code (For example : "Autodesk \Ftimes; AutoCAD"). Alternatively, you can use the AcDbMText::fontChange() method to insert the Font Change formatting character.
To try out the various formatting characters before using it in your code, use the MTEXTED command in AutoCAD to set an alternate text editor such as notepad.exe. You can then experiment with the format codes to choose the right one that suits.

## 评论

**内容**: Charles said...
Thanks for the post
Reply
06/28/2017 at 02:01 AM

---
**内容**: Aniket said...
How to create text frame to mtext
Reply
01/03/2019 at 02:15 AM

---
