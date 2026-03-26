---
title: "Calling Lisp commands from Palette"
date: 2015-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - AutoLISP
  - Palette
description: "If you want to invoke Lisp commands from .Net code, the Application.Invoke should help. This should work ok for Lisp commands that do not use (comm..."
author: Autodesk
---
# Calling Lisp commands from Palette

发布日期: 2015-04-01

原始链接: https://adndevblog.typepad.com/autocad/2015/04/calling-lisp-commands-from-palette.html

## 文章内容

By Balaji Ramamoorthy
If you want to invoke Lisp commands from .Net code, the Application.Invoke should help. This should work ok for Lisp commands that do not use (command-s ...) to invoke other AutoCAD commands. 
As an example, consider this Lisp command to create two circles.
 (defun c:mycircles1()
    (setq ms (vla-get-ModelSpace 
  (vla-get-ActiveDocument (vlax-get-acad-object))))
       (setq myCircle1
   (progn 
    (setq ctrPt <span'(0.0 0.0 0.0))
    (setq radius 5.0)
    (vla-addCircle ms 
    (vlax-3d-point ctrPt) radius)
   )
     )
    (setq myCircle2
   (progn 
    (setq ctrPt <span'(10.0 0.0 0.0))
    (setq radius 5.0)
    (vla-addCircle ms 
    (vlax-3d-point ctrPt) radius)
   )
     )
    (princ "SUCCESS !" )
 )
  This can be invoked from a button click handler in your palette using the following code snippet :
 private  void  DrawCirclesBtn1_Click(object sender, EventArgs e)
 {
     DocumentCollection acDocMgr 
   = Autodesk.AutoCAD.ApplicationServices
   .Application.DocumentManager;
     Document acDoc = acDocMgr.MdiActiveDocument;
       using  (DocumentLock dl = acDoc.LockDocument())
     {
         Editor ed = acDoc.Editor;
         using  (ResultBuffer rb = new  ResultBuffer())
         {
             rb.Add(new  TypedValue((int )LispDataType.Text, 
     "c:mycircles1" ));
             ResultBuffer rbRes = Autodesk.AutoCAD.
    ApplicationServices.Application.Invoke(rb);
             if  (rbRes != null)
             {
                 TypedValue[] tvalues = rbRes.AsArray();
                 foreach (TypedValue tv in tvalues)
                     ed.WriteMessage("\\n"  + tv.ToString());
                 rbRes.Dispose();
             }
             else 
                 ed.WriteMessage("\\n  
     Result buffer is null."); 
         }
     }
 }
  But, consider this Lisp command that relies on using AutoCAD's native CIRCLE command to create the two circles.
 (defun c:mycircles2()
    (command-s "CIRCLE"  "0,0,0"  5.0)
    (command-s "CIRCLE"  "10,0,0"  5.0)
    (princ "SUCCESS !" )
 )
  To invoke this version of the Lisp command from .Net, it becomes important to use the right context. As the .Net code for the button click event handler runs in session context, it is not appropriate for invoking Lisp commands that need to run in document context. Here is a version of the button click event handler to invoke the Lisp command using the command context. In earlier releases prior to 2016, you will need to use SendStringToExecute. In AutoCAD 2016, it is simpler to use the "ExecuteInCommandContextAsync" as shown in the below code snippet.
 private  async void  DrawCirclesBtn2_Click(
      object sender, 
      EventArgs e)
 {
     DocumentCollection docManager 
   = Autodesk.AutoCAD.ApplicationServices.
   Application.DocumentManager;
     Document doc = docManager.MdiActiveDocument;
     Editor ed = doc.Editor;
       // Option 1 :  
     //acDoc.SendStringToExecute("(c:mycircles2) ", 
  // true, false, false); 
       // Option 2 :  
     // run the command in command context. Works in 2016+ 
     await docManager.ExecuteInCommandContextAsync(
         async (obj) =>
         {
             using  (ResultBuffer rb = new  ResultBuffer())
             {
                 rb.Add(new  TypedValue((int )LispDataType.Text,
      "c:mycircles2" ));
                 ResultBuffer rbRes = Autodesk.AutoCAD.
    ApplicationServices.Application.Invoke(rb);
                 if  (rbRes != null)
                 {
                     TypedValue[] tvalues = rbRes.AsArray();
                     foreach (TypedValue tv in tvalues)
                       ed.WriteMessage("\\n"  + tv.ToString());
                     rbRes.Dispose();
                 }
                 else 
                     ed.WriteMessage("\\n  
                     Result buffer is null."); 
             }
         },
         null
     );
 }

## 评论

**内容**: Yuri Venenkovich said...
'In AutoCAD 2016, it is simpler to use the "ExecuteInCommandContextAsync" as shown in the below code snippet'
Hi. How is ExecuteInCommandContextAsync simpler than SendStringToExecute() (which is one line of code)?
Reply
03/31/2017 at 06:50 PM

---
