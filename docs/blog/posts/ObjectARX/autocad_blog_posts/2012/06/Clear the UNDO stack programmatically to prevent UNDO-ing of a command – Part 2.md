---
title: "Clear the UNDO stack programmatically to prevent UNDO-ing of a command – Part 2"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "Leading on from Adam’s really cool post on the same subject, someone just pointed out that the CMDECHO=0 is not observed using UNDO via SendStringT..."
author: Autodesk
---
# Clear the UNDO stack programmatically to prevent UNDO-ing of a command – Part 2

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/clear-the-undo-stack-programmatically-to-prevent-undo-ing-of-a-command-part-2.html

## 文章内容

by Fenton Webb
Leading on from Adam’s really cool post on the same subject, someone just pointed out that the CMDECHO=0 is not observed using UNDO via SendStringToExecute(). The initial command pumped is omitted but the command options are not…
The solution is to use my favorite function acedCmd() instead…
#if AC2013
    [DllImport("accore.dll", CallingConvention = CallingConvention.Cdecl, EntryPoint = "acedCmd")]
#else
    [DllImport("acad.exe", CallingConvention = CallingConvention.Cdecl, EntryPoint = "acedCmd")]
#endif
    private static extern int acedCmd(System.IntPtr vlist);
    [CommandMethod("ClearUndoStack")]
    public void ClearUndoStack()
    {
      // remember the cmdecho
      short cmdecho = (short)Application.GetSystemVariable("CMDECHO");
      // turn it off
      Application.SetSystemVariable("CMDECHO", 0);
        short undoCtl = (short)Application.GetSystemVariable("UNDOCTL");
      bool isOn = (undoCtl & 1) == 1;
      if (!isOn)
        return;
        bool isOneCmd = (undoCtl & 2) == 2;
      bool isAuto = (undoCtl & 4) == 4;
        ResultBuffer rb = new ResultBuffer();
      // RTSTR = 5005
      rb.Add(new TypedValue(5005, "_.UNDO"));
      rb.Add(new TypedValue(5005, "_Control"));
      rb.Add(new TypedValue(5005, "_None"));
      rb.Add(new TypedValue(5005, "_.UNDO"));
        if (isOneCmd)
        rb.Add(new TypedValue(5005, "_One"));
      else
      {
        rb.Add(new TypedValue(5005, "_All"));
        if (!isAuto)
        {
          rb.Add(new TypedValue(5005, "_.UNDO"));
          rb.Add(new TypedValue(5005, "_Auto"));
          rb.Add(new TypedValue(5005, "_Off"));
        }
      }
        // start the insert command
      acedCmd(rb.UnmanagedObject);
      // now restore cmdecho
      Application.SetSystemVariable("CMDECHO", cmdecho);
    }

## 评论

**内容**: fadi said...
Well,hi everybody ,im not a computer programmer..i just need to know if i have to re-install autocad 2012,because there is no undo/redo..is there a way to undo more than 1 command
thanks
Reply
01/09/2013 at 10:12 AM

---
