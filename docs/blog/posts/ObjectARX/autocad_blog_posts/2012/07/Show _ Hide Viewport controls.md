---
title: "Show / Hide Viewport controls"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "Viewport controls were introduced in AutoCAD 2012 and lets you easily change the view or the visual style."
author: Autodesk
---
# Show / Hide Viewport controls

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/show-hide-viewport-controls.html

## 文章内容

By Balaji Ramamoorthy
Viewport controls were introduced in AutoCAD 2012 and lets you easily change the view or the visual style.
It is displayed at the top left corner of the viewport and here is a screenshot :

To control the visibility of this control, launch the options dialog using the "Options" command, switch to "3d Modeling" tab and check / uncheck the "Display the Viewport controls" checkbox.
To control it programmatically, set the "VPCONTROL" system variable to 1 or 0.
Application.SetSystemVariable("VPCONTROL", 1);
            //OR
Application.SetSystemVariable("VPCONTROL", 0);

## 评论

**内容**: Daniel Balogh said...
Hello,
I konw ,this is not a forum. After some research I did not find any answer (yet) :)
So, is it possible, to create an own control in this manner?
Is this exposed to the API (.net 4.0/ACA2014/x64) in any way?
Thanks in advanca,
Daniel
Reply
11/01/2014 at 12:53 AM

---
**内容**: Daniel Balogh said in reply to Daniel Balogh...
Sorry for the typos :D
Reply
11/01/2014 at 12:54 AM

---
**内容**: Roffer Jally said...
I have the same question in my mind related to create our own control which we can use later in the same manner. Is anyone there who can help. Do we need API to create our own controls or we can get direct access to it.
Reply
05/27/2018 at 12:51 AM

---
