---
title: "Displaying the attrib dialog during insert with AcEdCommand"
date: 2013-03-01
categories:
  - AutoCAD C++
tags:
  - AutoLISP
  - C++
  - ObjectARX
description: "How can I force the attribute dialog box to display for an INSERT issued with acedCommand using ObjectARX?"
author: Autodesk
---
# Displaying the attrib dialog during insert with AcEdCommand

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/displaying-the-attrib-dialog-during-insert-with-acedcommand.html

## 文章内容

By Xiaodong Liang
Issue
How can I force the attribute dialog box to display for an _INSERT issued with acedCommand using ObjectARX?
Solution
You need to use a global function in ObjectARX called acedInitDialog. This is parallel to how the initdia function in AutoLISP must be called prior to issuing the INSERT command. 
When dialog initialization occurs before acedCommand, both the "insert" and "Enter Attributes", dialog boxes will display during command execution.Because the "insert" fields do not normally require modification, it is only desirable to display the attributes dialog for user input. In order to display the attribute dialog box instead of command line prompts, divide the command sequence into two parts so that the initialization call is made shortly before
attribute values are solicited.
static void testOut()
{
    //set vars first
    struct resbuf rb;
    rb.restype = RTSHORT;
    rb.resval.rint = 1;
    acedSetVar(L"ATTDIA", &rb);
    acedSetVar(L"ATTREQ", &rb);
      //block position
    ads_point pt1;
    pt1[X] = pt1[Y] = 4.0;
      //call command
    int rterr = acedCommand ( RTSTR, L"_.insert", RTSTR, L"myBlock", RTPOINT,
pt1, RTNONE );
    // ask to display attribute dialog
    acedInitDialog(Adesk::kTrue);
    // continue the command
    acedCommand(RTREAL, 1.0,  RTREAL, 1.0, RTREAL, 0.0, RTNONE);
  }

## 评论

**内容**: Bitlife said...
I am genuinely thankful to the holder of this web page who has shared this wonderful paragraph at at this place
Reply
08/03/2023 at 02:25 AM

---
