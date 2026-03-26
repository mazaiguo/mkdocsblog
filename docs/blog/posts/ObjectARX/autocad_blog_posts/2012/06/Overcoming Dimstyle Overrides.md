---
title: "Overcoming Dimstyle Overrides"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "After using entmod to change a dimstyle, the original settings modified become overrides of the newly modified dimstyle.  Here is a way to avoid th..."
author: Autodesk
---
# Overcoming Dimstyle Overrides

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/overcoming-dimstyle-overrides.html

## 文章内容

By Balaji Ramamoorthy
After using entmod to change a dimstyle, the original settings modified become overrides of the newly modified dimstyle.  Here is a way to avoid the creation of overrides.
Example: If the old extension line color for the dimstyle was 6, and the new one is 2
  - The modified dimstyle has extension lines with color 2
  - The modified dimstyle now has an override DIMCLRE = 6
Assume there is a dimstyle "MyNewStyle" with DIMCLRE = 6.  Executing the following code will modify the dimstyle "MyNewStyle" but will also create a dimstyle override DIMCLRE = 6.
(setq myDS-Info (entget (tblobjname "dimstyle" "MyNewStyle"))
      myDS-Info (subst
                    (cons 177 2)
                    (assoc 177 myDS-Info)
                    myDS-Info
                )
      myDS-Info-New (entmod myDS-Info))
To get rid of the Style Overrides, it is necessary to save them to the dimstyle.  This can be achieved in two ways:
1. The above code should be followed with
(command "-DIMSTYLE" "R" "MyNewStyle")
2. The following example uses ActiveX functions to change the dimension variable and then 'vla-CopyFrom' to update the current dimstyle.
To test it, first create the style "MyNewStyle" with DIMCLRE set to 6, and set the style current.  After running the code, any subsequent dimensions will have color 2 on the extension lines, and DIMCLRE = 6 will no longer list as an override.
(vl-load-com)
  (defun c:modCurDimStyle ()
     ;; Get the current dimstyle
   (setq acadApp (vlax-get-acad-object)
         curDoc  (vla-get-ActiveDocument acadApp)
         curDimStyle (vla-get-ActiveDimstyle curDoc)
   ) ;setq
     ;; Modify the current dimstyle.
   ;; This is done by changing the current dimvars
   ;; and by saving the dimvars in the dimstyle.
   ;; Change a dimvar.
   (vla-SetVariable curDoc "DIMCLRE" 2)
     ;; Save the current dim vars in the current dim style.
   (vla-CopyFrom curDimStyle curDoc)
   (princ)
)
Posted at 10:16 PM in AutoCAD, Balaji Ramamoorthy, LISP | Permalink

## 评论

**内容**: Irné Barnard said...
Could you please localize your variables? It's considered extremely bad practice to use global variables exclusively. Unless you intend for them to be global - in which case the convention is to indicate them as such by prefixing & suffixing asterisks to their names. And in which case (for efficiency) you should check if they're already assigned before simply assigning them again.
And another thing: You set a variable to the acad-object, but only use it once in the routine. This is lisp not C++/VB/VBA, so you don't need to do that - just wastes RAM for no reason.
Other than that you do show a nice short method for updating Dim Styles from overrides!
Reply
06/26/2012 at 02:37 AM

---
**内容**: Irné Barnard said...
Just as an afterthought, you don't need the ActiveX method SetVariable ... you could've simply used the old AutoLisp setvar function instead:
(setvar "DIMCLRE" 2)
Reply
06/26/2012 at 03:57 AM

---
**内容**: Balaji said in reply to Irné Barnard...
Hi Irné,
Thanks for your comments.
Project related "best practices" / naming conventions and error checking are usually very limited in the posts. It is only the core idea that we are trying to communicate and developers using it might need to consider these when including it in their production code.
Reply
06/26/2012 at 06:39 PM

---
