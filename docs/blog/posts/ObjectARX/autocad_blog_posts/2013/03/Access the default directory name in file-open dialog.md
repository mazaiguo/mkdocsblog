---
title: "Access the default directory name in file-open dialog"
date: 2013-03-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - DWG
description: "Where is the variable stored for the default directory name that the File-Open dialog uses, and can it be accessed? This is so that a user can open..."
author: Autodesk
---
# Access the default directory name in file-open dialog

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/access-the-default-directory-name-in-file-open-dialog.html

## 文章内容

By Xiaodong Liang
Issue
Where is the variable stored for the default directory name that the File-Open dialog uses, and can it be accessed? This is so that a user can open a drawing from a directory that is not valid for my application.
Solution
You can get the information about the current drawing in the editor by using these two system variables: DWGNAME and DWGPREFIX. DWGNAME contains the drawing name, including the .DWG extension. DWGPREFIX contains the path where the
drawing resides. Combining these system variables gives the full name of the current drawing.
Note that DWGPREFIX does not always contain the directory that the File-Open dialog defaults to. Instead, it defaults to the path of the last opened drawing, even if that drawing has been closed. Note that there is an exception to this: AutoCAD will not change the default File-Open directory if a file is opened from the history list. AutoCAD writes this information to Windows registry table under the following KEY when quitting and reads it as its history file list when starting.
"HKEY_CURRENT_USER\\Software\\Autodesk\\AutoCAD\\R17.0\\ACAD-xxx.xxx\\Recent File List" 
Where xxx.xxx is the version number of pure AutoCAD or vertical AutoCAD.
When AutoCAD is running, it does not update this information in the registry table; therefore, it is not a practical way to retrieve this information using the following VLISP expression.
(vl-registry-read
"HKEY_CURRENT_USER\\Software\\Autodesk\\AutoCAD\\R17.0\\ACAD-5001:409\\Recent File List" "File1")
It also does not work to set the latest opened file's path to what you want because AutoCAD maintains this information in memory, therefore, the information has not been exposed to a system variable or an API.
Fortunately, you can use the following simple AutoLISP expression to mimic the AutoCAD OPEN command or you can write your own version of the OPEN command.
(getfiled "Select File" "c:/program files/AutoCAD 2012" "dwg" 8)

