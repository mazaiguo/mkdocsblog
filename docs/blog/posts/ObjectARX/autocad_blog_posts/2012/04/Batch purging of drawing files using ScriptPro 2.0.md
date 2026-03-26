---
title: "Batch purging of drawing files using ScriptPro 2.0"
date: 2012-04-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - DWG
description: "This post will explain the procedure to use ScriptPro 2.0 tool to purge a set of AutoCAD drawing files."
author: Autodesk
---
# Batch purging of drawing files using ScriptPro 2.0

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/batch-purging-of-drawing-files-using-scriptpro-20.html

## 文章内容

By Virupaksha Aithal
This post will explain the procedure to use ScriptPro 2.0 tool to purge a set of AutoCAD drawing files.
Step1:
Download the ScriptPro 2.0 tool from http://usa.autodesk.com/adsk/servlet/item?siteID=123112&id=4091678&linkID=9240618
Step2:
Create an AutoCAD Script file which does the purging. You can use the ScriptPro key words to save the drawing with a new name after the purge. Below script file appends the “_Purged” to the drawing name. For example, drawing name “wheel.dwg” will be saved as “wheel_purged.dwg” after running the script. Save the script file.
[Start]
;command
-purge
;Enter type of unused objects to purge
All
;Enter name(s) to purge <*>:
;Verify each name to be purged? [Yes/No]
No
SAVEAS
;Enter file format
;Save drawing as
"<acet:cFolderName>\<acet:cBaseName>_purged.dwg"
[End]
Step3:
Start the ScriptPro tool.
Use the “wizard” options to start the ScriptPro wizard.

Step4:
Browse and selected the Script file saved in Step2 as the Script file to use. Refer “a”
Add the drawing files which need to be purged using “Add” button in wizard. Refer “b”
Select the AutoCAD version to be used for the batch operation. Refer “c”
Press “Finish and Start ScriptPro” button to start the batch purging. Refer “d”.

## 评论

**内容**: Kerry Brown said...
Virupaksha,
I have had ScriptPro2.0 since It was released.
It looks like this build is different ....
it uses a different menu and form design and can use accoreconsole.exe and ACAD2013.
Why is it still called version 2.0 when it is obviously different.
Regards
Kerry
Reply
04/20/2012 at 09:09 PM

---
**内容**: Kerry Brown said...

And I just noticed that you are the Author.
Thanks !
Regards
Kerry
Reply
04/20/2012 at 09:20 PM

---
**内容**: Viru said...
Hi Kerry
Thanks for comments.
Yes, ScriptPro 2.0 has changed a lot from the original version released in November 2010. But the core logic is still the same as the original version. The new version contains few bug fixes and new features like wizard. but the same time we have changed the assembly versions 2.0.3.0.

regards
Viru
Reply
04/23/2012 at 02:19 AM

---
**内容**: Kerry Brown said...

Thanks Viru.
Perhaps one way to let people know the current version would be to add the assembly version to the site. Otherwise people will either miss the update or download each month just to see if it is new :)
... Or post a notice here will suit those of us who visit here.
Regards
Kerry.
Reply
04/23/2012 at 03:59 AM

---
**内容**: Virupaksha aithal said...
Good idea.
I post the update in this blog when I update the ScriptPro next time...
regards
Viru
Reply
04/23/2012 at 04:48 AM

---
**内容**: Patricia said...
Just what I have been looking for! I've tried it and it works - fantastic.
Thank you so much.
Reply
06/07/2012 at 12:49 AM

---
**内容**: Mike Hutchinson said...
I tried ScriptPro 2.0 with accoreconsole.exe. I can run my raw script with accoreconsole and it runs fine to completion. But if I try to harness it with ScriptPro... The log files say: "Error while reading log file for... "
What would you suggest I try?
Reply
03/01/2013 at 03:02 PM

---
**内容**: Virupaksha Aithal said...
Hi,
Tough to say what is going wrong. can you please share the non confidential script file you are using at your end.
Thanks
Viru
Reply
03/06/2013 at 01:05 PM

---
**内容**: Mike Hutchinson said...
On "Error while reading log file..." I had the thought this evening that this may stem form having log file location in a location other then out of the box default. Default log file location for ScriptPro does not automatically change to where the autocad profile points to. Tomorrow I'll try setting both to the same location. Question: Does ScriptPro automatically do LOGFILEON?
Reply
03/06/2013 at 07:10 PM

---
**内容**: Mike Hutchinson said...
Another question: Am I seeing that you cannot use vl-, vla- and vlax- functions with accoreconsole?
Also, LAYOUTLISP I believe is a core lisp function. The console doesn't recognize it?
Reply
03/06/2013 at 07:14 PM

---
**内容**: Thomas said...
I like this little piece of magic :)
I ran into a problem though: I was making a "purge" script for a batch of drawing, but I wasn't able to disable the prompt "Thich block contains dynamic Features. Would you like to open it in the block editor?" when opening a drawing. Thus, resulting in failing my script to run.
Is there any option to disable that prompt?
Reply
06/06/2013 at 05:27 AM

---
**内容**: Walker Macy said...
this would be great if it worked...it hangs when trying to open Autocad 2014, on Windows 7 x64. tried on two different machines. "unable to open autocad" or just hangs and never opens autocad
Reply
10/01/2013 at 03:29 PM

---
**内容**: Jesse (aka) CadDog said...
Well, Looks Great but I haven't been able to get it to work.
I used your purge scr as it first and it failed. I change the scr a little by - to _ just in case but with no luck.
I'm using AutoCAD Civil 3D 2011 on Windows 7x64.
I hope this very cool looking app works soon.
Thanks
Reply
11/12/2013 at 12:17 PM

---
**内容**: ben said...
How can you configure ScriptPro to open password protected files?
Reply
12/11/2013 at 05:05 AM

---
**内容**: Jose Luis said...
Download link don´t open.
Reply
02/19/2014 at 07:15 AM

---
**内容**: philip said...
hi,
I try this link http://usa.autodesk.com/adsk/servlet/item?siteID=123112&id=4091678&linkID=9240618
but there is no scriptpro 2 for download, is anyone know where to download the ScriptPro 2?
many thanks
Reply
03/16/2014 at 01:42 AM

---
**内容**: Virupaksha Aithal said...
Hi,
Yes, we are trying to fix this issue. Till that please get the installer from Gethub @ https://github.com/ADN-DevTech/ScriptPro-installer
Thanks
Viru
Reply
03/18/2014 at 04:41 PM

---
**内容**: kuba said...
Hi Virupaksha,
could you please provide some information how to create scp project file, eventually how to save current project into scp.
se also http://forums.augi.com/showthread.php?147750-ScriptPro

thanks
kuba
Reply
07/22/2015 at 02:51 AM

---
**内容**: Ben said...
I'm getting the following error: "Error while reading log file for... " and it doesn't work. any ideas?
Reply
01/03/2017 at 04:32 PM

---
**内容**: James Maeding said...
BTW, do not use scripts to clean excess reg apps (application IDs). It is a waste of time as the xrefs load when the file opens and your purges either lock or take 20-30 seconds if you really have an app id problem. So many people put -purge R in their startup, but they have yet to experience current drawing and 2 xrefs with 50k+ app ids. That stops everything. Not that app ids are corruption, but they bulk the file and prevent Audit from running (well, finishing) if you need to. Instead use the Autodesk regapp cleaner or my batcher posted in .net forums, or JTB purger - anything but a tool like full acad or coreconsole.
Reply
01/17/2017 at 08:24 AM

---
**内容**: Dutchtower said...
Hi,
I have a simple script to audit and save a drawing that works when I drag it into the AutoCAD Drawing Area, but if I run it in ScriptPro2, it leaves the .dwl and .dwl2 files for the selected drawing in place and shows "Failed in the ScriptPro window.
I am new to scripts so forgive any naiveté.
Here is the script:
audit
y
QSAVE
Thanks in advance
Reply
02/03/2017 at 02:40 PM

---
**内容**: Mel C said in reply to Dutchtower...
Dutchtower,
I'm having the same issue. Did you get a solution?
Thanks
Reply
07/25/2017 at 05:36 AM

---
**内容**: Mel C said in reply to Mel C...
Had an error in my script
Contained an extra "space" at the last line of the script, which acts as an "enter", so it was restarting the previous command, then sitting there waiting to be told what to do next, then timing out.
So lesson is....make sure last line in script is the same as the last input you would enter at the command line in autocad
Reply
07/25/2017 at 06:29 AM

---
**内容**: Ankit said...
I am trying to Purge (including nested data, orphanage data etc. ) in Autocad 2016. What should be the script. I have written the following :
;command
-purge
;Enter type of unused objects to purge
All
;Enter name(s) to purge <*>:
;Verify each name to be purged? [Yes/No]
No
;command
qsave
;command
CLOSE
it is not working. Shows failed in scriptpro window.
Reply
04/23/2017 at 11:36 PM

---
**内容**: Michael Behar said...
Can ScriptPro load .NET Assemblies?
Reply
03/14/2019 at 05:19 PM

---
