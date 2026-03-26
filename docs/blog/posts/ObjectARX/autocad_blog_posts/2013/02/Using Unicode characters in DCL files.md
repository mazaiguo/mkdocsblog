---
title: "Using Unicode characters in DCL files"
date: 2013-02-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
  - Selection
  - Unicode
description: "Some people experienced issues with their DCL files when using them in AutoCAD 2013. Their unicode characters (Cyrillic, Greek, etc.) were not disp..."
author: Autodesk
---
# Using Unicode characters in DCL files

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/using-unicode-characters-in-dcl-files.html

## 文章内容

By Adam Nagy
Some people experienced issues with their DCL files when using them in AutoCAD 2013. Their unicode characters (Cyrillic, Greek, etc.) were not displayed correctly. DCL files by default are saved in ANSI format where the characters depend on the code page being used. In previous versions the character set selection when dispaying the DCL dialogs was based on the OS settings, whereas in the new version it is based on the language version of AutoCAD. This change in behaviour is likely to be reverted.
To avoid this problem you can update your DCL file to UTF-8 format which does not depend on codepages, product language version or OS settings. 
Note: UTF-8 DCL files can only be used from AutoCAD 2013 onwards.
To make your DCL file use the UTF-8 format, simply open it in Notepad, then in the Save As dialog set Encoding to UTF-8. Note that Visual Lisp editor doesn't show UTF-8 files properly, so you'll have to edit those in a unicode compatible editor such as Notepad.
I also tested using the UTF-8 DCL file inside a Visual Lisp Application that can be compiled into a VLX file. There are many posts on the net about creating a Visual Lisp Application. 
Once I compiled the application (File >> Make Application >> Make Application) then I got the VLX file that I could APPLOAD into AutoCAD. The attached sample application includes a command called TestDcl, which should bring up a dialog. If it looks exactly like this then all is fine:

## 评论

**内容**: Alexander Rivilis said...
Note. Not possible add UTF-8 DCL-file to project in order to build vlx-file.
Reply
02/14/2013 at 07:25 AM

---
**内容**: Adam Nagy said...
Hi Alexander,
Thanks for the comment.
I have just tested it in AutoCAD 2013 _VERNUM "G.114.0.0 (UNICODE)" (read only) and things seem to work. I'll update the above post in a second with my files and info on what I did so you can test it on your side.
Cheers,
Adam
Reply
02/14/2013 at 08:39 AM

---
**内容**: Alexander Rivilis said in reply to Adam Nagy...
Hi, Adam! You're absolutely right. Thank you! This mistake was in AutoCAD without Service Pack 1.1
I checked that with AutoCAD 2013 SP 1.1 still displays ANSI DCL-files are not correct, and not thought to check UTF-8 DCL-files in the VLX-files. Now I've checked it and it is all right!
Reply
02/15/2013 at 01:18 AM

---
**内容**: Giorgos said...
thank you. this helped me a lot
Reply
09/15/2013 at 11:23 AM

---
**内容**: Samsung Printer Troubleshooting said...
Issues in your Samsung printer after Windows 10 update is common, try these simple Samsung Printer Troubleshooting hacks to fix it. Call now.
Reply
07/01/2020 at 06:02 AM

---
