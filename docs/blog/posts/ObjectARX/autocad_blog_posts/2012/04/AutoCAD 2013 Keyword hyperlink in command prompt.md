---
title: "AutoCAD 2013 Keyword hyperlink in command prompt"
date: 2012-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - C++
  - ObjectARX
description: "AutoCAD 2013 can display keywords / subcommands as hyperlinks that can be selected using the mouse. In ObjectARX, for your keywords to appear as hy..."
author: Autodesk
---
# AutoCAD 2013 Keyword hyperlink in command prompt

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/autocad-2013-keyword-hyperlink-in-command-prompt.html

## 文章内容

By Balaji Ramamoorthy
AutoCAD 2013 can display keywords / subcommands as hyperlinks that can be selected using the mouse. In ObjectARX, for your keywords to appear as hyperlinks, simply add them to the prompt message within square brackets each separated by a forward slash. For ex : "Specify floor [ First / Second ]"
In AutoCAD .Net API, just adding keywords will make them appear as hyperlinks. You will not need to modify the prompt message.
Here is sample code using ObjectARX :
AcGePoint3d point;
int ret = RTNORM;
  acedInitGet(RSG_NONULL, _T("First Second"));
  ret = acedGetPoint
(
NULL,
ACRX_T("\nSelect a point [First / Second]"),
asDblArray(point)
);
  if (ret == RTKWORD)
{
TCHAR kw[20];
acedGetInput(kw);
acutPrintf(kw);
}
else if(ret == RTNORM)
{
acutPrintf(
ACRX_T
(
"\nSelected Point : %lf, %lf, %lf"),
point.x,
point.y,
point.z
);
}
else
{
acutPrintf(ACRX_T("\nNothing selected"));
}
Here is a sample code using AutoCAD .Net API :
Document doc = Application.DocumentManager.MdiActiveDocument;
Editor ed = doc.Editor;
  PromptPointOptions ppo = new PromptPointOptions("Pick a point ");
ppo.Keywords.Add("First");
ppo.Keywords.Add("Second");
  PromptPointResult ppr = ed.GetPoint(ppo);
  if (ppr.Status == PromptStatus.Keyword)
    ed.WriteMessage(ppr.StringResult);
else if (ppr.Status == PromptStatus.OK)
    ed.WriteMessage(ppr.Value.ToString());
else
    ed.WriteMessage("Cancelled");

## 评论

**内容**: Martin said...
Thanks for sharing
Reply
08/08/2017 at 04:05 AM

---
**内容**: Dani Regar said...
Thanks for sharing
Reply
04/27/2018 at 03:41 PM

---
**内容**: Rubel Ahmed said...
Hello,
I’d like to edit the cookie opt-in checkbox text “Save my name, email, and website in this browser for the next time I comment.”
Basically I’d like to remove the word “website” as my comment post section does not have a Website field.
See more article here

Thanks.
Reply
03/25/2019 at 09:23 AM

---
**内容**: bitlife said...
Regards for sharing
Reply
03/23/2024 at 12:48 AM

---
