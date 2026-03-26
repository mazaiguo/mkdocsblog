---
title: "Working with non-English version of AutoCAD"
date: 2012-07-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
  - Selection
description: "As an example, "acedSSGet(L":S", NULL, NULL, NULL, set)" in a non-English version of AutoCAD returns an error."
author: Autodesk
---
# Working with non-English version of AutoCAD

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/working-with-non-english-version-of-autocad.html

## 文章内容

By Balaji Ramamoorthy
As an example, "acedSSGet(L":S", NULL, NULL, NULL, set)" in a non-English version of AutoCAD returns an error.
Here is an extract from the AutoLISP Developer's guide under the "Foreign Language Support" heading:
<<<
If you develop AutoLISP programs that can be used with a foreign-language version of AutoCAD, the standard AutoCAD commands and key words are automatically translated if you precede each command or key word with an underscore (_).
 
(command "_line" pt1 pt2 pt3 "_c")
 
If you are using the dot prefix (to avoid using redefined commands), you can place the dot and underscore in either order. Both "._line" and "_.line" are valid."
 
So, to ensure compatibility with all localized versions of AutoCAD, you should
use "acedSSGet(L"_:S", ..." instead of "acedSSGet(L":S", ..."
>>>
The same principle applies for the other acedSSGet keywords.
 
You can test your programs on an English version of AutoCAD for globalization problems by setting the undocumented GLOBCHECK system variable to 1.
After setting this system variable to 1, if you try running this :
(command "line" '(0 0 0) '(10 0 0) '(10 10 0) "_c")
AutoCAD recognises that this might cause problems in non-English version of AutoCAD.
Here is a screen capture of the output messsages.

## 评论

**内容**: olivier Eckmann said...
Hello,
How do you know the US option when working in non-US AutoCAD? For command it's easy. Click on button or ribbon, launches the US command, but within a command, option are translated, and it's not always simple to find the US option.
Thanks
Olivier
Reply
07/09/2012 at 12:51 AM

---
**内容**: Balaji said in reply to olivier Eckmann...
Hi Olivier,
Sorry for the delay in responding to your comment. I was on vacation last week.
As you might already know, there is no way to switch the language of AutoCAD while it is running. So to find the US option, I can only think of the following ways :
1) Refer to the English version of the documentation. For example : PLine documentation lists the various options in English : http://docs.autodesk.com/ACD/2010/ENU/AutoCAD%202010%20User%20Documentation/index.html?url=WS1a9193826455f5ffa23ce210c4a30acaf-48f7.htm,topicNumber=d0e290858
2) The other way could be to create a lauch shortcut with "/language en-US". This would launch the English version of AutoCAD which can be used to find the options.
Thank you.
Reply
07/16/2012 at 04:20 PM

---
**内容**: Autocad said...
Now we have many apps to use with GPS and maps with Android apps and others, Technology facilitates humans to investigate and learn
Reply
04/27/2013 at 06:30 PM

---
