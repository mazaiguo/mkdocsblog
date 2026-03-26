---
title: "Waiting for (command) to finish in AutoLISP"
date: 2012-05-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Selection
description: "If you need to wait for a certain command to finish before continuing (in this case SELECT), use the following code to pause for user input as long..."
author: Autodesk
---
# Waiting for (command) to finish in AutoLISP

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/waiting-for-command-to-finish-in-autolisp.html

## 文章内容

By Balaji Ramamoorthy
If you need to wait for a certain command to finish before continuing (in this case SELECT), use the following code to pause for user input as long as is required:
(defun c:MySelect ()
    (Command "SELECT" "w") 
    (while (= (getvar "CMDNAMES") "SELECT")
        (command pause)
    ) 
    (setq ss (ssget "P")) 
    (print
        (strcat "Number of entities selected: "
                (itoa (sslength ss))
        ) 
    ) 
    setq ss nil
    (princ)
)

## 评论

**内容**: Account Deleted said...
Hi, Balaji!
You forgot to remind that in this form, this code will only work in AutoCAD English, but not in localized versions of AutoCAD.
Reply
05/06/2012 at 08:44 AM

---
**内容**: Balaji said...
Thank you Alexander.
You are right, this code will only work in the English version of AutoCAD. I only have English version installed in my system, so I can't test the changes that might be required for it to work in other language versions, but I guess it will work if we use the global names such as "_.SELECT", "_.CMDNAMES" and "_P". Any additional inputs that you can provide will surely help readers of this blog who will want to use this code in localized versions of AutoCAD. Thank you.
Reply
05/06/2012 at 11:11 AM

---
**内容**: Account Deleted said...
Universal code must look like this:
(defun c:MySelect ( / ss)
(Command "_.SELECT" "_w")
(while (= (getvar "CMDNAMES") "SELECT")
(command pause)
)
(setq ss (ssget "_P"))
(print
(strcat "Number of entities selected: "
(itoa (sslength ss))
)
)
(princ)
)
Reply
05/06/2012 at 01:02 PM

---
**内容**: Account Deleted said...
Also yours code has a mistaken line:
setq ss nil
Have you a small practice in AutoLisp? :-D
Reply
05/06/2012 at 01:06 PM

---
