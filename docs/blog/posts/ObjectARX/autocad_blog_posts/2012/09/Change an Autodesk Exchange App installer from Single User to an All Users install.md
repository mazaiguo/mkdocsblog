---
title: "Change an Autodesk Exchange App installer from Single User to an All Users install"
date: 2012-09-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Plugin
description: "The static install folder design (folders that cannot be changed) was specifically designed to help developers bypass the 2nd stage installer issue..."
author: Autodesk
---
# Change an Autodesk Exchange App installer from Single User to an All Users install

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/change-an-autodesk-exchange-app-installer-from-single-user-to-an-all-users-install.html

## 文章内容

By default all Autodesk Exchange App installers are built to deploy the App bundles to the %APPDATA%\Autodesk\ApplicationPlugin folder. This folder is specifically a Single User install location, which means that if any other user logs onto the machine the App will need to be reinstalled for that user to be available, to that user.
The static install folder design (folders that cannot be changed) was specifically designed to help developers bypass the 2nd stage installer issues that comes with installing plugins, particularly difficult in AutoCAD, for the All User installation scenario. The way this was handled was to include a different static folder designed to support loading apps for the All User installation model, this folder can be found in the %PROGRAMDATA%\Autodesk\ApplicationPlugins folder.
The question is, how do I change an Exchange App Installer from being a Single User to an All User installer…
The answer - It’s all about changing the static folder installation path from the %APPDATA%\Autodesk\ApplicationPlugin (Single User) to %PROGRAMDATA%\Autodesk\ApplicationPlugins (All User). There are two ways that this can be achieved:
1) From a DOS command window:
c:\>msiexec /i MyExhangeApp.msi INSTALLDIR=C:\ProgramData\Autodesk\ApplicationPlugins AUTODESK=C:\ProgramData\Autodesk
2) You can edit the MSI directly using ORCA.exe and change the Directory Table->AUTODESK from AppDataFolder to CommonAppDataFolder

## 评论

**内容**: Dave Plumb said...
I don't understand how your method #1 is supposed to work.
Where (or when) do I enter the INSTALLDIR and AUTODESK lines?
Do I need to run the second and third lines before the msi?
Are those DOS SET commands?
When I type in the first line (msiexec /i myapp.msi) it just runs the installer.
Reply
10/08/2012 at 08:11 AM

---
**内容**: Owen Wengerd said in reply to Dave Plumb...
That's all one line.
Reply
10/08/2012 at 09:55 AM

---
**内容**: Dave Plumb said...

Sometimes its the obvious solution.
That worked perfectly.
As long as I'm posting, I'll add something else that's hopefully useful:
Add
/passive
to the end of the msiexec string to get it to run silently.
AFTER thorough testing, of course!
Reply
10/11/2012 at 07:03 AM

---
