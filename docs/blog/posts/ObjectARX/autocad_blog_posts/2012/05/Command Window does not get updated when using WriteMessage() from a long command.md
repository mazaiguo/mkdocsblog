---
title: "Command Window does not get updated when using WriteMessage() from a long command"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C#
  - Unicode
description: "I'm using WriteMessage() in a longer command and would like to keep the user updated by writing messages to the command window. Unfortunately, when..."
author: Autodesk
---
# Command Window does not get updated when using WriteMessage() from a long command

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/command-window-does-not-get-updated-when-using-writemessage-from-a-long-command.html

## 文章内容

By Adam Nagy
I'm using WriteMessage() in a longer command and would like to keep the user updated by writing messages to the command window. Unfortunately, when I use WriteMessage(), its content only appears once my command finished. How could I update/refresh the Command Window to show the text I wrote?
Solution
If you add a carriage return (C# \n, VB.NET vbCr/vbCrLf) to the end of your text then it will appear straight away. As mentioned in the comments section, VB.NET vbCr might not work as well as vbCrLf does.
[CommandMethod("AEN1WriteInfo")]
static public void AEN1WriteInfo()
{
  Editor ed = Autodesk.AutoCAD.ApplicationServices.Application.
      DocumentManager.MdiActiveDocument.Editor;
  ed.WriteMessage("Something\n");
  for (int i = 0; i < 3; i++)
  {
    System.Threading.Thread.Sleep(1000);
    // carriage return at the end
    ed.WriteMessage(i.ToString() + "\n");
  }
}

## 评论

**内容**: Rolando Hijar said...
I had the same problem. For me the solution was to add
"System.Windows.Forms.Application.DoEvents()" inside the "For Loop".
Reply
05/27/2013 at 12:19 PM

---
**内容**: Michael Leslie said...
This is a useful trick, but I have found using AutoCAD 2013 and VB 2012 that if I pass vbCr my message does not display whereas with vbCrLf it does.
Is this new to this version? I notice in most sample code, they use "/n" or vbCr, so it works for them . . .
You may want to change the VB.NET note at the end of your example. Thanks.
Reply
08/20/2013 at 11:54 AM

---
**内容**: Maxence said...
Don't work for me. I need to call DoEvents to force the refresh like @Rolando
Reply
06/05/2014 at 01:25 AM

---
**内容**: build now gg said...
I would like to advise you to keep improving and keep doing what you're doing.
Reply
03/23/2024 at 12:49 AM

---
