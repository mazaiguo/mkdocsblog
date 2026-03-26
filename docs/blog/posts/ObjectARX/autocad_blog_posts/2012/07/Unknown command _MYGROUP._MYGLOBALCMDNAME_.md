---
title: "Unknown command "MYGROUP._MYGLOBALCMDNAME""
date: 2012-07-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
description: "I have a command definied with these properties: groupname: MYGROUP, local command name: MYLOCALCMDNAME, global command name: MYGLOBALCMDNAME. In m..."
author: Autodesk
---
# Unknown command "MYGROUP._MYGLOBALCMDNAME"

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/unknown-command-mygroup_myglobalcmdname.html

## 文章内容

By Adam Nagy
I have a command definied with these properties: groupname: MYGROUP, local command name: MYLOCALCMDNAME, global command name: _MYGLOBALCMDNAME. In my application I used to envoke this command using "MYGROUP._MYGLOBALCMDNAME" but it does not seem to work anymore and AutoCAD says that it's an unknown command. Why is that?
Solution
Underscore '_' and/or dot '.' should not be used as part of a command name definition/declaration - i.e. don't include these prefixes in calls to addCommand(), and don't use them in demandload registry entries.
These characters are used as clues for how to perform a lookup on a given command:
A prefix of '_' means: look in the global command list for a match 
A prefix of '.' means: include undefined commands in the search
There used to be an issue in the ARX Wizard that the automatically generated global command name was prefixed with an underscore '_', but this has been fixed.

