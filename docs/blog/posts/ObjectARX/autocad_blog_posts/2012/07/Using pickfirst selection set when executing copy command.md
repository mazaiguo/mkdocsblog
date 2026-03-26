---
title: "Using pickfirst selection set when executing copy command"
date: 2012-07-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - Plugin
  - Selection
description: "I have a pickfirst set and I'd like to make a copy of the whole selection set, instead of going through the selection with a for-loop and calling a..."
author: Autodesk
---
# Using pickfirst selection set when executing copy command

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/using-pickfirst-selection-set-when-executing-copy-command.html

## 文章内容

By Balaji Ramamoorthy
Issue :
I have a pickfirst set and I'd like to make a copy of the whole selection set, instead of going through the selection with a for-loop and calling acedCommand (RTSTR, "copy",..) on each entity within the selection set. Is there a way to call acedCommand (RTSTR, "copy",..) just once to copy the whole set, just like what AutoCAD appears to do?
Solution :
You can use a selection set by adding RTPICKS and the selection set in acedCommand:
// Since we will use the pickfirst selection set,
// the command must be defined with ACRX_CMD_USEPICKSET flag
static void AdskArxProject1_CopyPF(void)
{
    ads_name ss;
    acedSSGet(_T("_I"),NULL,NULL,NULL,ss);
    acedCommand(
                    RTSTR,
                    _T("_copy"),
                    RTPICKS,
                    ss,
                    RTSTR,
                    _T(""),
                    RTNONE
                );
    acedSSFree(ss);
}
Since the command uses the pickfirst selection set, ensure that the command is defined with the ACRX_CMD_USEPICKSET flag
Also, in AutoCAD the pickfirst selection must be enabled, which means that the PICKFIRST variable must be one.

