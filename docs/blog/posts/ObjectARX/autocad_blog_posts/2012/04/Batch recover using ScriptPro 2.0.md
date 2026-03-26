---
title: "Batch recover using ScriptPro 2.0"
date: 2012-04-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - DWG
description: "This post will explain the procedure to use ScriptPro 2.0 tool to recover a set of AutoCAD drawing files."
author: Autodesk
---
# Batch recover using ScriptPro 2.0

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/batch-recover-using-scriptpro-20.html

## 文章内容

By Virupaksha Aithal
This post will explain the procedure to use ScriptPro 2.0 tool to recover a set of AutoCAD drawing files.
Step1:
Download the ScriptPro 2.0 tool from http://usa.autodesk.com/adsk/servlet/item?siteID=123112&id=4091678&linkID=9240618
Step2:
Create and save an AutoCAD script file which does the recover for a given drawing file. You can use the ScriptPro key words to open and save the drawing file. Refer below script file. Below script file appends the “_recovered” to the drawing file after recovery. For example, drawing name “wheel.dwg” will be saved as “wheel_recovered.dwg” after running the script.
[Start]
QAFLAGS 31
RECOVER
"<acet:cFullFileName>"
_SAVEAS
"<acet:cFolderName>\<acet:cBaseName>_recovered.dwg"
Close
[End]
Step 3:
Start the ScriptPro tool.
Use the “wizard” options to start the ScriptPro wizard.
Step 4:
Browse and selected the Script file saved in Step2 as the script file to use. Refer “a”
Add the drawing files which need to be purged using “Add” button in wizard. Refer “b”
Select the AutoCAD version to be used for the batch operation. Refer “c”
Press “Finish” button to close wizard dialog. Refer “d”.
Step 5:
As recovery command opens the drawing file, we need to make sure that the ScriptPro tool does not open the drawing file. so click settings button in the wizard
Select options "Run script without opening drawing file". Modify the process time value if your drawings are large and need extra time to open
Press OK.
Step 6:
Run the ScriptPro tool

## 评论

**内容**: Andre said...
Hi there,
I can check Run script drawing without opening drawing file but it will still open Autocad session.

Thanks
Reply
10/29/2013 at 10:35 AM

---
**内容**: Evgeny said...
Thank you for the tip, it's very useful.
I ran the script and found that some my filed failed on the process. The reason is that the "Process timeout..." parameter value is not enough to finish recover process for drawing.
It would be nice if you can mention that in your tip. Thank you.
Reply
11/08/2013 at 07:06 AM

---
**内容**: viru said...
Thanks. I have edited the post
regards
Viru
Reply
11/10/2013 at 10:34 PM

---
**内容**: Kerry Brown said...
Is a more recent build available for this product ??
I have seen references on AutoDesk blogs to a 64 bit build of the product ... where can it be downloaded.
Regards,
Reply
01/04/2016 at 04:11 PM

---
**内容**: viru said in reply to Kerry Brown...
Hi,
ScriptPro 2.0 should work on 64 bit machines... same tool should work against AutoCAD 2016. Please let me know if the tool fails to work on AutoCAD 2016 64 bit
Viru
Reply
01/04/2016 at 09:02 PM

---
**内容**: Logan said...
This is not working with Autocad 2016 (no recover file is created)
Reply
03/03/2016 at 12:28 PM

---
**内容**: viru said...
Hi Logan,
please provide non confidential drawing file against which we try the recover script in AutoCAD 2016.
regards
Viru
Reply
03/03/2016 at 10:51 PM

---
**内容**: Alex Chow said...
It fails to work on AutoCAD 2016 64 bit:
Error message:
[ Status summary ]
Failed

Error while reading log file for C:\
Reply
01/23/2017 at 10:20 AM

---
