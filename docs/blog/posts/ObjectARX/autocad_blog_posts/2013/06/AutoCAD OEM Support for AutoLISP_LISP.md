---
title: "AutoCAD OEM Support for AutoLISP/LISP"
date: 2013-06-01
categories:
  - AutoLISP
tags:
  - API
  - AutoCAD
  - AutoLISP
  - COM
  - OEM
description: "AutoCAD OEM does support LISP, but there are a few restrictions:"
author: Autodesk
---
# AutoCAD OEM Support for AutoLISP/LISP

发布日期: 2013-06-01

原始链接: https://adndevblog.typepad.com/autocad/2013/06/autocad-oem-support-for-autolisplisp.html

## 文章内容

by Fenton Webb
AutoCAD OEM does support LISP, but there are a few restrictions:
LISP applications must be compiled into .fas, raw .lsp files are not supported.
You must compile your LISP applications using the inbuilt “AutoCAD OEM” (aoem.exe) application that is installed with the AutoCAD OEM CD.
Once the .lsp has been compiled into a .fas, you must then bind the fas file to the OEM product in the build process. This means that you can never just load LISP files (.fas) into an OEM product, it must be registered at build time.
The ActiveX API is not supported in LISP; that means vlax functions do not work.
The VLIDE and APPLOAD commands are omitted in 3rd party AutoCAD OEM products.
The user-entered LISP interpreter is disabled in 3rd party AutoCAD OEM products. The (command) still works fine when invoked from an OEM bound .fas file.

## 评论

**内容**: Adam Davis said...
Hi Fenton,
I have read this and other pages and still have an uncertainty over whether a final end customer using Acme OEM can load and run a plain text lsp file
eg
ChangeLayer.lsp
(command "_.LAYER" "_COLOR" "1" "0" "")
Could you clarify please
Thanks Adam
Reply
06/20/2013 at 05:10 AM

---
**内容**: Fenton Webb said...
Hey Adam
unfortunately, you can't just load LISP files into OEM : first they must be compiled into .fas, then the fas file must be bound to the OEM product at build time.
Reply
06/20/2013 at 08:07 AM

---
**内容**: Adam Davis said...
Hi Fenton,
Thanks for clearing that one up.
Adam
Reply
06/20/2013 at 10:37 AM

---
**内容**: tivanova@maxfieldjarvis.co.uk said...
Hi. How can we bind the OEM product at build time? Is there a tutorial on this somewhere?
Reply
09/21/2022 at 01:43 AM

---
