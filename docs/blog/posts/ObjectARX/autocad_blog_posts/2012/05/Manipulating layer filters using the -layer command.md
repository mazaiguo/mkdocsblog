---
title: "Manipulating layer filters using the -layer command"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - C++
  - Database
  - Layer
  - ObjectARX
description: "I've seen that using the hidden option of the -LAYER command called 'FI' I can create layer filters, but I did not find the exact property setting ..."
author: Autodesk
---
# Manipulating layer filters using the -layer command

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/manipulating-layer-filters-using-the-layer-command.html

## 文章内容

By Adam Nagy
I've seen that using the hidden option of the -_LAYER command called '_FI' I can create layer filters, but I did not find the exact property setting names to use.
Could you please list them?
Solution
The layer filter related settings can be found in the Extension Dictionary of the Layer Table.
To check the options you could create a layer filter in the user interface and then look into the appropriate part of the database to see how the options have been stored.
You could use the ArxDbg.arx application for this, which is part of the ObjectARX SDK.

I’ve created a filter where I set all options apart from Plot Style and got the following string:
"USED==\"TRUE\" AND VPOVERRIDES==\"FALSE\" AND NAME==\"A*\" AND OFF==\"False\" AND FROZEN==\"True\" AND LOCKED==\"True\" AND COLOR==\"10\" AND LINETYPE==\"DASHED\" AND LINEWEIGHT==\"0.18\" AND PLOTTABLE==\"True\" AND NEWVPFROZEN==\"True\""
Once you know which options you want to use then you can place it in a LISP command like this:
(command "_LAYER" "_FI" "_N" "_P" "" "USED==\"TRUE\" AND NAME==\"A*\"" "MyFilter" "")

## 评论

**内容**: Raymarcher said...
Thanks for the blogpost, I have a question.
What to add to the lisp to populate multiple NAME rows?
Reply
03/30/2016 at 05:33 AM

---
