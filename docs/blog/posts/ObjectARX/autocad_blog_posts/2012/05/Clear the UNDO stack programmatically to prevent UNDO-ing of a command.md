---
title: "Clear the UNDO stack programmatically to prevent UNDO-ing of a command"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Forge
description: "I would like to make sure that the user cannot UNDO beyond a certain command. How could I do that?"
author: Autodesk
---
# Clear the UNDO stack programmatically to prevent UNDO-ing of a command

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/clear-the-undo-stack-programmatically-to-prevent-undo-ing-of-a-command.html

## 文章内容

By Adam Nagy
I would like to make sure that the user cannot UNDO beyond a certain command. How could I do that?
Solution
Although there is no direct UNDO API, you could use the UNDO command to achieve what you need. You could call UNDO with Control > None option to switch UNDO recording off, which will also clear the UNDO stack. Then you can switch it back afterwards, so consecutive commands can be undone.
Since UNDO operates on command borders, it should not really be changed inside a command. Therefore, although UNDO can be called synchronously using acedCommand/acedCmd, it's better to call it through sendStringToExecute which will run it asychronously. In case of the latter, do not forget that the UNDO stack will only be cleared after the command you called it from finished, so that will not be UNDO-able either.
Here is a .NET sample code that implements the above:
using System;
using Autodesk.AutoCAD.Runtime;
using acApp = Autodesk.AutoCAD.ApplicationServices.Application;
  [assembly: CommandClass(typeof(CsMgdAcad1.AEN1Commands))]
  namespace CsMgdAcad1
{
  public class AEN1Commands
  {
    /// <summary>
    /// To clear the UNDO stack we need to turn the undo off, then
    /// turn it back on. We also make sure that the settings will be
    /// changed back to the way they were
    /// </summary>
    [CommandMethod("Aen1ClearUndo")]
    static public void Aen1ClearUndo()
    {
      short undoCtl = (short)acApp.GetSystemVariable("UNDOCTL");
      bool isOn = (undoCtl & 1) == 1;
        if (!isOn)
        return;
        bool isOneCmd = (undoCtl & 2) == 2;
      bool isAuto = (undoCtl & 4) == 4;
        string cmdString = "._UNDO _Control _None ._UNDO ";
        if (isOneCmd)
        cmdString += "_One ";
      else
      {
        cmdString += "_All ";
          if (!isAuto)
          cmdString += "._UNDO _Auto _Off ";
      }
        acApp.DocumentManager.MdiActiveDocument.SendStringToExecute(
        cmdString, true, false, true);
    }
  }
}

## 评论

**内容**: Fenton Webb said...
A Part 2 version of this entry can be found here...
http://adndevblog.typepad.com/autocad/2012/06/clear-the-undo-stack-programmatically-to-prevent-undo-ing-of-a-command-part-2.html
Reply
06/22/2012 at 11:14 AM

---
