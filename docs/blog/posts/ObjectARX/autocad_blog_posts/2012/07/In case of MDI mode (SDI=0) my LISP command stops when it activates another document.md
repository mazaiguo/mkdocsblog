---
title: "In case of MDI mode (SDI=0) my LISP command stops when it activates another document"
date: 2012-07-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - DWG
description: "I have the below code. When the vla-activate part is executed then my LISP code stops and none of the code parts after that is reached."
author: Autodesk
---
# In case of MDI mode (SDI=0) my LISP command stops when it activates another document

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/in-case-of-mdi-mode-sdi0-my-lisp-command-stops-when-it-activates-another-document.html

## 文章内容

By Adam Nagy
I have the below code. When the vla-activate part is executed then my LISP code stops and none of the code parts after that is reached.
(command "_sdi" "0") ; the problem is with MDI mode / SDI=0
(vl-load-com)
(setq acadApp (vlax-get-acad-object))
(setq acadActiveDoc (vla-get-ActiveDocument acadApp))
(setq acadDocs (vla-get-documents acadApp))
(setq newDrawing "C:\\test.dwg")
(if
  (= 0 (getvar "SDI"))
    ; if sdi = 0
    (vla-activate (vla-open acadDocs newDrawing))    
    ; if sdi = 1                            
    (vla-sendcommand acadActiveDoc (
      strcat "(command \"_open\")\n" newDrawing "\n"
    )
  ) 
)
(print "this part is not reached")
Solution
There are two main contexts in AutoCAD:
Document context – only works within the boundaries of a document 
Session/Application context – best suited for opening/closing/activating documents 
You can find further information about contexts in the Object ARX Reference Guide, <Object ARX SDK>\docs\arxdoc.chm
LISP can only work in Document context – the command or function is bound to the Document that it was started from.
When you activate another document, then the running code's execution stops and only continues once the document it was running in becomes active again.
Also, for similar reasons you cannot close the document that the code is running in.
However, you can open documents in the background and use the API to interact with them - i.e. you open them the same way you're doing it now, but simply do not activate them.
You could also use ARX or .NET instead, which can create commands that run in session context.

## 评论

**内容**: Anon said...
"However, you can open documents in the background and use the API to interact with them - i.e. you open them the same way you're doing it now, but simply do not activate them."
How would one do this? Here is my issue: 1) I am trying to copybase objects in the modelspace of my current drawing (a.dwg) which I can do with a lisp; 2) The trouble I am having is getting the lisp to open a template file (dwt), paste 0,0,0 the objects from a.dwg, and saveas b.dwg to the folder directory of a.dwg. The cause of the issue is SDI=0. The only way I can get the lisp to do what I want is by setting SDI=1.
Reply
01/04/2024 at 05:16 PM

---
