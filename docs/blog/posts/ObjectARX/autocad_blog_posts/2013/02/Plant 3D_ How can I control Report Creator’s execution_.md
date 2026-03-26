---
title: "Plant 3D: How can I control Report Creator’s execution?"
date: 2013-02-01
categories:
  - Plant 3D
tags:
  - DWG
  - Plant 3D
description: "Does Report Creator have any command line options?"
author: Autodesk
---
# Plant 3D: How can I control Report Creator’s execution?

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/plant-3d-how-can-i-control-report-creators-execution.html

## 文章内容

By Marat Mirgaleev
Issue
Does Report Creator have any command line options?
Solution
Here are the Report Creator command line options:
/CONFIG <Filename> · Specify report configuration file to use.
/DWG <filename1[,filename2,filename3, …]>
· Specify the drawings to include in the report.
/HIDDEN
· Hides the main dialog and generates the report(s) or preview.
· If you don’t specify this, then we show the main dialog with all the other settings filled in, like report configuration file, drawings to select, and which project.
/PREVIEW
· Show report preview.
/PROJECT <Filename>
· Specify the Plant project file to use.
/QUIET
· Be quiet. Turns off error dialogs.

## 评论

**内容**: mnl_ignacio@yahoo.com said...
Hi..Thanks for sharing these command lines.
However I'm using AP3D 2017.The line "/DWG" is not recognized when running the batch file.
May I know what's the new command as replacement?
Thanks in advance.
Cheers!
Reply
07/24/2018 at 05:34 PM

---
