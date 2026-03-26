---
title: "Passing list of values to an ObjectARX function using Lisp returns error"
date: 2012-09-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - AutoLISP
  - C++
  - DXF
  - ObjectARX
description: "Passing list of values to an ObjectARX function using Lisp throws error when certain numbers (For ex : 5011, 25111) are part of the list. Why and h..."
author: Autodesk
---
# Passing list of values to an ObjectARX function using Lisp returns error

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/passing-list-of-values-to-an-objectarx-function-using-lisp-returns-error.html

## 文章内容

By Balaji Ramamoorthy
Issue
Passing list of values to an ObjectARX function using Lisp throws error when certain numbers (For ex : 5011, 25111) are part of the list. Why and how to overcome this ?
Solution
Certain numbers are interpreted as DXF codes which causes AutoCAD to throw an exception.
The simple workaround for this is to send the values as real numbers as shown here :
For ex :  (myLispCallableTestFunc '(5011.0 2 3 4))
The other workaround is to send the values as independent lists. These list may have to be joined together inside the ObjectARX function that is called from LISP.
For ex : (myLispCallableTestFunc '((5011) (2) (3) (4)))

## 评论

**内容**: James Maeding said...
those workarounds sound easy, but are actually a major problem. How do you tell on the arx/.net end what was an integer, and what was a real? It seems like a trivial matter, but not when you start passing nested lists. You then have to have some function convert all the sublists, then unconvert on the arx/.net end. But the information is degraded on the arx/.net end because the fact that a number was an integer or real matters sometimes. I have routines that return a value (real) or error flag as an integer. You start thinking through how this could affect things, and I switched over to serializing my lists, then sending as string, then deserialize on .net end and serialize to send back to lisp. No more issues to think about. Its a shame autodesk does not do something to eliminate the reinterpreting of integers as dxf codes to eliminate the workarounds.
Reply
09/04/2012 at 01:28 PM

---
