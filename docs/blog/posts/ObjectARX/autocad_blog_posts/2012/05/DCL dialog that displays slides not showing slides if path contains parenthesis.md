---
title: "DCL dialog that displays slides not showing slides if path contains parenthesis"
date: 2012-05-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
description: "I have  a DCL dialog that has slides. The slides are not being displayed. I use the "VSLIDE" command and select a sld and I get  an AutoCAD Message..."
author: Autodesk
---
# DCL dialog that displays slides not showing slides if path contains parenthesis

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/dcl-dialog-that-displays-slides-not-showing-slides-if-path-contains-parenthesis.html

## 文章内容

By Wayne Brill
Issue
I have  a DCL dialog that has slides. The slides are not being displayed. I use the "VSLIDE" command and select a sld and I get  an AutoCAD Message that states "Program Files.slb" "Can't find file in search path". How can I get the slides to display? 
Solution
If the directory that contains a SLB file contains parenthesis, such as "Program Files (x86)\", the slides will not display. The DCL call into the slide library is being confused. It uses the parenthesis as a pointer into the library.
The solution is to modify the AutoLISP code not to use the path and move the slide library into support search path that does not contain parenthesis.

