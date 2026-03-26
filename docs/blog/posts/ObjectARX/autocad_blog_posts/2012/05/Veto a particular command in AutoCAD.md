---
title: "Veto a particular command in AutoCAD"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "You can Veto any command inside “DocumentCollection.DocumentLockModeChanged” event. This event is called just before AutoCAD start processing the c..."
author: Autodesk
---
# Veto a particular command in AutoCAD

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/veto-a-particular-command-in-autocad.html

## 文章内容

By Virupaksha Aithal
You can Veto any command inside “DocumentCollection.DocumentLockModeChanged” event. This event is called just before AutoCAD start processing the command. Refer below code which prevents the quitting of AutoCAD.
[CommandMethod("AddVetoToQuit")]
static public void AddVetoToQuit()
{
    DocumentCollection doc = Application.DocumentManager;
    doc.DocumentLockModeChanged +=
        new DocumentLockModeChangedEventHandler(
                            doc_DocumentLockModeChanged);
  }
  [CommandMethod("RemoveVetoToQuit")]
static public void RemoveVetoToQuit()
{
    DocumentCollection doc = Application.DocumentManager;
    doc.DocumentLockModeChanged -=
                new DocumentLockModeChangedEventHandler(
                               doc_DocumentLockModeChanged);
  }
  static void doc_DocumentLockModeChanged(object sender,
                            DocumentLockModeChangedEventArgs e)
{
    if (string.Compare(e.GlobalCommandName, "QUIT", true) == 0)
    {
        e.Veto();
    }
}

## 评论

**内容**: Matinau said...
I know this is an old post but any chance you could provide the AutoLISP equivalent? I've been playing around with this (vlr-DocManager-Reactor nil '((:vlr-documentLockModeChanged . VetoCommand))) and getting nowhere fast.
Reply
04/23/2017 at 11:18 PM

---
**内容**: Matinau said...
My main issue is the actual veto, escaping works for some commands but not open.
(defun VetoCommand (sender arg / *globalCommand*)
(setq *globalCommand* (nth 4 arg)
*document* (nth 0 arg)
)
(if (wcmatch (strcase *globalCommand*) "OPEN")
(progn
(princ "\nCommand intercepted")
(vla-SendCommand *document* "\e\e\e")
)
)
)
Reply
04/24/2017 at 02:13 AM

---
