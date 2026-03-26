---
title: "Importing named Layout in an AutoCAD DWG file using LISP"
date: 2013-06-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
  - DWG
description: "If you are wondering how to import a named Layout into the current drawing file using LISP in AutoCAD, here you go."
author: Autodesk
---
# Importing named Layout in an AutoCAD DWG file using LISP

发布日期: 2013-06-01

原始链接: https://adndevblog.typepad.com/autocad/2013/06/importing-named-layout-in-an-autocad-dwg-file-using-lisp.html

## 文章内容

By Partha Sarkar
If you are wondering how to import a named Layout into the current drawing file using LISP in AutoCAD, here you go.
LISP code snippet below, demonstrates how to import a layout named "ABC" from a selected DWG file to the current drawing file.
(defun C:LayoutImport()

  ;; Select a DWG file to import a Layout
 (setq myFile (getfiled "Select your DWG File:" " " "dwg" 8)) 
 (command"layout" "t" myFile "ABC") 
 (alert "New Layout is inserted!") 
 (princ) 
)
  After executing the above LISP code, you would see a new Layout named “ABC” is imported to the current DWG –

## 评论

**内容**: imadhabash@hotmail.com said...
Hi Partha,
actually i have a very big project using the same floor design . in some cases i have to mirror the xref BUT the problem is that the text mirrored also. i try mirrtext command to solve the problem but nothing happened.
is there is a way or Lisp to mirror Xref’s without mirroring text with it ?
Thanks in advance,,
Habash
Reply
06/15/2013 at 10:46 PM

---
**内容**: Matus Brlit said in reply to imadhabash@hotmail.com...
you can duplicate your texts, put them in two layers, one set of text will be backwards
then, in the mirrored xref, you will turn on the layer with backwars texts
this requires, that the texts are justified to center, otherwise, they will be moved, when changed to backwards (or you will have to reposition them, which might be a lot of work)
Reply
06/29/2013 at 12:27 AM

---
**内容**: Dwg said...
Thank you very much i find this info.I'm very happy :)
Thank you againg.King regards
Reply
10/21/2013 at 09:52 AM

---
**内容**: nolan said...
Thank you so much!
I have send 3 days on trying to do this, so lucky to find out this page.
Reply
09/12/2017 at 03:38 AM

---
