---
title: "Workaround: Acad.lsp is reloaded when -VBARUN command is used in S::STARTUP"
date: 2012-12-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
  - COM
  - VBA
description: "You might observe that Acad.lsp is reloaded when -VBARUN command is used in the S::STARTUP function to load a drawing. Is this a known behavior and..."
author: Autodesk
---
# Workaround: Acad.lsp is reloaded when -VBARUN command is used in S::STARTUP

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/workaround-acadlsp-is-reloaded-when-vbarun-command-is-used-in-sstartup.html

## 文章内容

By Gopinath Taget
You might observe that Acad.lsp is reloaded when -VBARUN command is used in the S::STARTUP function to load a drawing. Is this a known behavior and is there a way to stop it from reloading?  This happens even when ACADLSPASDOC variable is 0.
The reason that Acad.lsp is reloaded, with a drawing opened by a procedure in  Acad.dvb (called with -VBARUN in S:STARTUP), is that AutoCAD has not finished initializing at the point in the S::STARTUP function where the command -VBARUN is called. 
As a workaround, the VBASTMT command allows you to call VBA functions with arguments, from either the command line or a LISP expression.  In this case, we can use (vla-sendcommand) in the (S::STARTUP) function, to call the VBA "RunMacro" method.  This approach will not cause a reload of Acad.lsp
(defun-q mystartup ( )
   (vl-load-com) ;load ActiveX objects
   ;;replace this line: (command ".-vbarun" "MyModule.MySub") 
   ;;with the following:  
   (arxload "acadvba.arx") ;ensure Acad.dvb is loaded
   (vla-sendcommand 
      (vla-get-activedocument (vlax-get-acad-object))
      "vbastmt\n\ThisDrawing.Application.RunMacro \"MyModule.MySub\"\n"
   )
)
(setq s::startup (append s::startup mystartup))

## 评论

**内容**: James Maeding said...
I encourage everyone to make their acad.lsp be one line "(princ)".
In its place, have a portion of code in your acaddoc.lsp (you do have one right?) do the work that runs once per session, which is the point of acad.lsp.
To get a portion of code to only run once per session, you set a flag variable maybe called STARTUP-HAS-RUN at end of the code chunk, like this:
(vl-load-com)
(IF (NOT STARTUP-HAS-RUN)
...put your code that would be in acad.lsp here....
...then set the flag to prevcent it running again, and propogate to new drawings...
(setq STARTUP-HAS-RUN 1)
(vl-propagate 'STARTUP-HAS-RUN)
)
The advantage is you can get all startup code into one .lsp file, which facilitates less confusion by those new to lisp. It makes for faster editing for those who are not new.
ALWAYS make an acaddoc.lsp and acad.lsp no matter what.
Put them in the top support path, add one if needed. The whole virus startup thing is insanely easy to cure if you have a clue about this, but Autodesk seems to shun the whole topic of using lisp effectively. Only dev sites like this seem and customization DG seem to have the info needed.
Reply
12/18/2012 at 09:43 AM

---
**内容**: John said in reply to James Maeding...
Thank you for your insight.
Reply
07/21/2013 at 04:37 PM

---
