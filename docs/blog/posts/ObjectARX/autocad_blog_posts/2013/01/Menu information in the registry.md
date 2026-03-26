---
title: "Menu information in the registry"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "If you are considering replacing or manipulating AutoCAD menus, here is some information that could be useful."
author: Autodesk
---
# Menu information in the registry

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/menu-information-in-the-registry.html

## 文章内容

By Gopinath Taget
If you are considering replacing or manipulating AutoCAD menus, here is some information that could be useful.
The menu information is stored in the user's profile (of the registry) in two locations:
HKEY_CURRENT_USER\Software\Autodesk\AutoCAD\R19.0\ACAD-B001:409\Profiles\<<Unnamed Profile>>\General Configuration\MenuFile
HKEY_CURRENT_USER\Software\Autodesk\AutoCAD\R19.0\ACAD-B001:409\Profiles\<<Unnamed Profile>>\Menus
Note that the AutoCAD Base Menu is stored in the MenuFile key, and the Partial Menu information is located in the Menus key.
Within the Menus key you have two sets of sub-keys: Groups and Pops.
- GroupX (where X denotes a number) are the menu groups, and each is a string consisting of the menu group name followed by the identification  in the menu file. e.g.
Group2 : "CUSTOM custom"
- PopX are the individual menus, and each is a string containing the menu group followed by the pop menu name. e.g.
Pop8 : "ACAD POP1"
One point to note is that the registry should be manipulated when AutoCAD is not running. If done during the time AutoCAD is running, the information won't be valid for the current session, and could be erased or altered for the current user profile when AutoCAD is shutdown.

## 评论

**内容**: Virginia Lawrence said...
Interesting, thanks for posting! Would you know anything about registry in Calgary, perchance? Any insights or suggestions would be most welcome. Thanks!
Reply
02/12/2013 at 10:37 AM

---
**内容**: Summer Ding said...
Hi Gopinath,
Thanks for your post. I have a question regarding the menu. In my profile, there is no partial menus in the Menus key, but when I use cuiload command to see the menu list, there are a lot of partial cuix, where are these item's information stored?
Reply
04/14/2015 at 10:39 PM

---
