---
title: "ObjectARX 2013 integrated documentation installer"
date: 2012-09-01
categories:
  - AutoCAD C++
tags:
  - API
  - AutoCAD
  - C++
  - ObjectARX
description: "A post on the forums reported that the Visual Studio 2013 integrated documentation installer (posted to the AutoCAD Developer Center) isn’t working..."
author: Autodesk
---
# ObjectARX 2013 integrated documentation installer

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/objectarx-2013-integrated-documentation-installer.html

## 文章内容

By Stephen Preston
A post on the forums reported that the Visual Studio 2013 integrated documentation installer (posted to the AutoCAD Developer Center) isn’t working correctly in some situations. This is the installer that allows you to view the ObjectARX documentation in Visual Studio by highlighting an AutoCAD API class/method/property/event and hitting F1.
The problem appears to be caused if you try to install the ObjectARX 2013 documentation when you’ve already installed the 2012 version. The two don’t work well side-by-side and only the 2012 version displays. Here are the steps I have found will allow you to replace the 2012 integrated docs with the 2013 ones. I don’t see a way to make them work together:
Uninstall the 2012 documentation.
Delete or rename the folder C:\ProgramData\Microsoft\HelpLibrary\content\Autodesk, Inc (e.g. to C:\ProgramData\Microsoft\HelpLibrary\content\Autodesk, Inc.old).
Install the 2013 version of the integrated docs.
Another thanks to Lee for telling me step 2.
Let me know via a comment if this doesn’t work for you, and we can take another look at any additional steps needed.
Update September 14th 2012:
If you find the above folder location is empty or doesn’t exist, the you can find the correct location from the ‘Choose online or local help’ option in the Help Viewer:
And Maxence tells me he fixed his problem by repairing his help viewer installation from his add/remove programs control panel.

## 评论

**内容**: Maxence said...
Don't work for me.
I need to add the install path with the Help Library Manager to make it works. And if I click on a link, I've got the message "Can’t find requested content on your computer". There is nothing installed in C:\ProgramData\Microsoft\HelpLibrary.
I'm on Windows 7 x64.
Reply
09/12/2012 at 11:18 PM

---
**内容**: lompav said...
Not working for me neither, with no previous install of ObjectARX documentation 2012. Step 3 done + Visual Studio 2010 Help Library Manager set to local as explained.
Can see the Autodesk, Inc directory created in
C:\ProgramData\Microsoft\HelpLibrary\content\
But it has no effect on Visual Studio Help. F1 on "DocumentManager" class leads to a 404 error of internet explorer with "the topic you requested could not be found in local help." error message.
Reply
09/26/2012 at 07:04 AM

---
**内容**: Madhukar Moogala said in reply to lompav...
Not sure about this one. What version of Visual Studio are you using? (I could understand it not working with Express).
Lee is working on an update to the installer, which I hope will be available soon.
Reply
09/26/2012 at 11:41 AM

---
**内容**: Owen Wengerd said in reply to lompav...
There is no class named DocumentManager. Did you mean AcApDocManager?
Reply
09/26/2012 at 12:14 PM

---
**内容**: Tony Tanzillo said in reply to Owen Wengerd...
DocumentManager is the name of a property of the managed Application object, and has an entry in the help index of arxmgd.chm.
Reply
09/26/2012 at 12:58 PM

---
**内容**: Owen Wengerd said in reply to Tony Tanzillo...
Ah, I see, I didn't realize that the managed API documentation was included.
Reply
09/26/2012 at 01:03 PM

---
**内容**: lompav said...
I'm using the Visual Studio 2010 Professional.
The local help for it is working I can access for exemple to the "EventArgs" class documentation. But nothing about Autodesk.Autocad classes like "ViewTableRecord".
When I open "C:\ProgramData\Microsoft\HelpLibrary\content" I can see the Microsoft folder containing all .mshc .mshi and .metadata for Visual Studio, I can also see the Autodesk, Inc folder containing the same kind of contents (AdskManaged.1 .mshc .mshi and .metadata). But it seems that this part is not referenced by the Visual Studio Help.
Reply
09/27/2012 at 12:45 AM

---
