---
title: "Wait for oemmakewizard.exe to finish when used from a batch file"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - OEM
description: "I migrated my project from OEM 2008 to 2011 and now my batch file that builds these projects do not work properly. In case of OEM 2008 when I start..."
author: Autodesk
---
# Wait for oemmakewizard.exe to finish when used from a batch file

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/wait-for-oemmakewizardexe-to-finish-when-used-from-a-batch-file.html

## 文章内容

By Adam Nagy
I migrated my project from OEM 2008 to 2011 and now my batch file that builds these projects do not work properly. In case of OEM 2008 when I started the wizard the execution in the batch file stopped and only continued once the OEM Make Wizard finished. This is important for me because in the batch file I want to further process the built project. However with OEM 2011 the execution continues and does not wait for the Wizard to finish, so the additional parts in the batch file fail because the project is not created yet. I also tried using the START /WAIT function in the batch file but that did not help either. What could I do?
Solution
It does seem to be the case that when calling oemmakewizard.exe from a batch file the execution continues straight away.
One solution would be to keep checking the oemmakewizard.exe process among the running tasks, and only continue once it finished. This can be done using batch commands. To poll the system less about the list of runing processes we can wait a second in the loop. Since Windows does not have a SLEEP function we would need to use something else, e.g. CHOICE or PING
@echo off

echo.Starting build

"C:\Program Files\Autodesk\AutoCAD OEM 2011\Toolkit\oemmakewizard.exe" OemTest 013260521 /BALL

:wait
choice /t 1 /d Y > nul:
tasklist /FI "IMAGENAME eq oemmakewizard.exe" | find /I "oemmakewizard.exe" > nul:
if not errorlevel 1 goto wait

echo.Build finished

