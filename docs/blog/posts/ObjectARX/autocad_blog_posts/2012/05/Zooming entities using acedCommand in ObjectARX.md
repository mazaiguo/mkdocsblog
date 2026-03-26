---
title: "Zooming entities using acedCommand in ObjectARX"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
  - Selection
description: "Few days back Fenton Webb showed me the below ObjectARX way of zooming the selected entities."
author: Autodesk
---
# Zooming entities using acedCommand in ObjectARX

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/zooming-entities-using-acedcommand-in-objectarx.html

## 文章内容

By Virupaksha Aithal
Few days back Fenton Webb showed me the below ObjectARX way of zooming the selected entities.
void zoomTest()
{
    ads_name ss;
    int err = acedSSGet(NULL, NULL, NULL, NULL, ss);
    if (err != RTNORM)
    {
        return;
    }
    acedCommand(RTSTR, _T("_.zoom"), RTSTR, _T("_Object"),
                        RTPICKS, ss, RTSTR, _T(""), RTNONE);
    acedSSFree( ss );
}

## 评论

**内容**: petcon said...
NEVER USE acedCommand IN ARX
and why not post the real arx code to show how to get zoom done
Reply
05/16/2012 at 09:50 PM

---
**内容**: Virupaksha aithal said...
Hi,
Not sure why you think developer needs to avoid using “acedCommand”. In this case use of acedCommand will reduce the effort of the developers finding the extent and then setting the setting.
Having said that, we will write similar post in future on zooming the entities without acedcommand.
Thanks
Viru
Reply
05/16/2012 at 10:04 PM

---
**内容**: petcon said...
zooming the entities without acedcommand. this is what like.
yes i know acedCommand is easy and quick solution.
but i should say it is NOT a good solution,do u think so?
Reply
05/17/2012 at 03:35 AM

---
**内容**: Account Deleted said...
Patcon! "NOT good solution" and "NEVER USE" - these are two very different ideas. Agree? ;-)
Reply
05/17/2012 at 03:39 AM

---
**内容**: petcon said in reply to Account Deleted...
agree.and i will never use. :D
Reply
05/17/2012 at 10:22 PM

---
**内容**: Madhukar Moogala said...
acedCommand is a very good solution to a lot of problems. Its an extremely powerful way to synchronously use the functionality provided by AutoCAD commands within your code. As a purist, you might prefer to write all your functionality from scratch, but (as a realist) why would I spend a long time reverse-engineering an AutoCAD command when I can use acedCommand and spend the time I save working on other code (or - better still - sitting by the pool sipping a cold beer).
Reply
05/17/2012 at 08:13 AM

---
**内容**: petcon said in reply to Madhukar Moogala...
i agree " (as a realist) why would I spend a long time reverse-engineering an AutoCAD command when I can use acedCommand and spend the time I save working on other code".
OK.never invent the wheel.
but as i know acedCommand will cause some unkown side effect,is that true?.
Reply
05/17/2012 at 10:29 PM

---
**内容**: Madhukar Moogala said...
Any API can cause unexpected results if you use it wrongly. But acedCommand (or (command) in LISP) is a very mature API, and is safe to use as documented in the ObjectARX helpfiles.
Perhaps you got confused between ObjectARX and .NET. P/Invoking acedCommand in a .NET plug-in could cause problems due to AutoCAD's use of Fibers - which .NET doesn't support - so you have to use it with more care there.
Reply
05/18/2012 at 03:50 PM

---
