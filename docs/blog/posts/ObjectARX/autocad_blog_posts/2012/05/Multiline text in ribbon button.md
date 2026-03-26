---
title: "Multiline text in ribbon button"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - Block
  - CUI
  - Polyline
  - Unicode
description: "To create a ribbon button with multi-line text using the CUI editor :"
author: Autodesk
---
# Multiline text in ribbon button

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/multiline-text-in-ribbon-button.html

## 文章内容

By Balaji Ramamoorthy
To create a ribbon button with multi-line text using the CUI editor :
Open the CUI editor and select the ribbon item
In the “Name” field, enter the words separated by “\r”. For ex : Insert\rBlock
  Please note that control characters such as “\r” do not appear in the edit box after it is saved, but the ribbon item will display the multi-line correctly.
To create a multi-line ribbon button using code, here is a sample code snippet :
Autodesk.Windows.RibbonButton ribButton = new RibbonButton();
ribButton.Text = String.Format("My{0}Polyline", Environment.NewLine);
ribButton.ShowText = true;
ribButton.Size = Autodesk.Windows.RibbonItemSize.Large;
ribButton.CommandParameter = "\x1b\x1b_PLINE ";
ribButton.CommandHandler = new AdskCommandHandler();

## 评论

**内容**: RenderMan said...
Balaji,
The code you posted fails to build, as you have neglected to mention that AdskCommandHandler is a user-defined Class that Implements System.Windows.Input.ICommand, nor did you include a link to any reference for this being required, such as this AU 2009 Course:
API for CUIx Files and the Runtime Ribbon in AutoCAD®
... Not exactly helpful for those who are new to .NET API (like me).
Reply
08/24/2012 at 06:44 AM

---
**内容**: Balaji said in reply to RenderMan...
Sorry, if that created some confusion.
This post is only about dealing with multiline text in the ribbon button. This post may not be right one if you are looking for a complete code sample for ribbon usage.
There are several other posts that my colleagues have authored that contain full code explaining the creation of ribbon buttons.
Here are few that will be helpful :
http://adndevblog.typepad.com/autocad/2012/06/ribbonsplitbutton-with-icons-images.html
http://adndevblog.typepad.com/autocad/2012/05/arrange-ribbon-buttons-into-columns.html
Reply
08/25/2012 at 10:06 AM

---
**内容**: Joris Maes said...
I tried the "\r" option but after a click on Apply, the \r disappears.
Any idea how to achieve a 2-line text in AutoCAD 2016?
Reply
12/02/2015 at 06:32 AM

---
**内容**: Jan said...
"\n" not "\r"
Reply
05/30/2016 at 06:33 AM

---
**内容**: ritusharma said...
It is the most important panel in AutoCAD.
Reply
09/19/2021 at 11:00 PM

---
