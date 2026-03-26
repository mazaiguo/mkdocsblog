---
title: "When is the selection set returned by acedGetCurrentSelectionSet() valid in ObjectARX?"
date: 2013-04-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
  - Selection
description: "I'm confused when acedGetCurrentSelectionSet() should return me a valid Selection Set, can you explain please?"
author: Autodesk
---
# When is the selection set returned by acedGetCurrentSelectionSet() valid in ObjectARX?

发布日期: 2013-04-01

原始链接: https://adndevblog.typepad.com/autocad/2013/04/when-is-the-selection-set-returned-by-acedgetcurrentselectionset-valid-in-objectarx.html

## 文章内容

by Fenton Webb
Issue
I'm confused when acedGetCurrentSelectionSet() should return me a valid Selection Set, can you explain please?
Also, how do I clear the PickFirst Selection Set?
Solution
The function acedGetCurrentSelectionSet() fills an selection set with the object IDs of all entities in the Current Selection Set within AutoCAD. The "Current Selection Set" may be one of the following: a pickfirst set, a selection set selected by the select command or any other command that does a selection (that is, similar to the "Previous" selection option), or the most recent set from calling the function ssget().
You may not get a result calling acedGetCurrentSelectionSet() from a command which does not have the ACRX_CMD_USEPICKSET flag defined. The problem is that you must tell AutoCAD to allow your command to receive the PICK FIRST selection set, otherwise AutoCAD will simply clear it when the command is invoked. Simply add the ACRX_CMD_USEPICKSET to your ACRX_CMD_TRANSPARENT defined command. Be sure to read the ObjectARX Reference guide regarding AcEdCommand::commandFlags for more details.
To clear the PICKFIRST selection set you just need to call acedSSSetFirst(NULL, NULL);

