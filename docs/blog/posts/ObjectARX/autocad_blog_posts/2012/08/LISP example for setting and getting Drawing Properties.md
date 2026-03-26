---
title: "LISP example for setting and getting Drawing Properties"
date: 2012-08-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - COM
description: "Is there a lisp example that shows how to access Drawing Properties?"
author: Autodesk
---
# LISP example for setting and getting Drawing Properties

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/lisp-example-for-setting-and-getting-drawing-properties.html

## 文章内容

By Philippe Leefsma
Q:
Is there a lisp example that shows how to access Drawing Properties?
A:
Here is a Visual Lisp example that will update the Drawing Properties for the active drawing.
Note: Values which are changed in the user interface are not immediately reflected in the ActiveX properties. If the drawing is saved and then reopened, the values previously changed in the user interface are returned by the ActiveX properties.  However, values which are set by the ActiveX methods are always immediately reflected in the user interface.
  (defun c:dProps (/ dProps dProp)
(vl-load-com)
(setq acadObject (vlax-get-acad-object))
(setq acadDocument (vla-get-ActiveDocument acadObject))
     ;;Get the SummaryInfo
   (setq dProps (vlax-get-Property acadDocument 'SummaryInfo))
     ;;Edit the SummaryInfo properties
   (vlax-put-Property dProps 'Title "Test Title")
   (vlax-put-Property dProps 'Subject "Test Subject")
   (vlax-put-Property dProps 'Author "Test Author")
   (vlax-put-Property dProps 'Keywords "One Two Three")
   (vlax-put-Property dProps 'Comments "This is a comment")
   (vlax-put-Property dProps 'HyperlinkBase "\\\\www.Autodesk.com")
   (vlax-put-Property dProps 'LastSavedBy "Tester")
   (vlax-put-Property dProps 'RevisionNumber "1")
   ;;Add an entry to the "Custom" tab
   (vla-addcustominfo dProps "test custom" "custom value")
     ;;Access the updated properties and print them to the command window
   (setq dProp (vlax-get-Property dProps 'Title))
   (princ (strcat "Title = " dProp "\n"))
   (setq dProp (vlax-get-Property dProps 'Subject))
   (princ (strcat "Subject = " dProp "\n"))
   (setq dProp (vlax-get-Property dProps 'Author))
   (princ (strcat "Author = " dProp "\n"))
   (setq dProp (vlax-get-Property dProps 'Keywords))
   (princ (strcat "Keywords = " dProp "\n"))
   (setq dProp (vlax-get-Property dProps 'Comments))
   (princ (strcat "Comments = " dProp "\n"))
   (setq dProp (vlax-get-Property dProps 'HyperlinkBase))
   (princ (strcat "HyperlinkBase = " dProp "\n"))
   (setq dProp (vlax-get-Property dProps 'LastSavedBy))
   (princ (strcat "LastSavedBy = " dProp "\n"))
   (setq dProp (vlax-get-Property dProps 'RevisionNumber))
   (princ (strcat "RevisionNumber = " dProp "\n"))
   (princ)
)

## 评论

**内容**: Isaac Harper said...
How do you retrieve the "Text Custom" (custom field) and save that value to a user defined variable? (For example: I want to set the FLOOR_LEVEL in the custom field (example:"02" for the second floor) and then have my routine pull that "string" number as a strcat to add other info in that will be placed as text in the drawing. This routine will be ran several times so I don't want to have to keep typing it in, and in several different drawings so I want the value stored in the file rather that the lisp. Thank you in advance.
Reply
07/21/2014 at 11:58 AM

---
**内容**: domgino said...
THANKS!
This is a very helpful Lisp!
Reply
11/19/2014 at 02:34 AM

---
