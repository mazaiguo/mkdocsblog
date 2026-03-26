---
title: "How to programmatically create a new text style (with truetype fonts) in lisp"
date: 2012-12-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
  - Unicode
description: "Using Visual LISP, how do you create a new style without using (command "style" new-style full-style-name "" "" "" "" "" "") ?"
author: Autodesk
---
# How to programmatically create a new text style (with truetype fonts) in lisp

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/how-to-programmatically-create-a-new-text-style-with-truetype-fonts-in-lisp.html

## 文章内容

By Gopinath Taget
Using Visual LISP, how do you create a new style without using (command "style" new-style full-style-name "" "" "" "" "" "") ?
There are two lisp approaches to create a new style, without using (command "style"...etc), but you will need the name of the actual .ttf file to do so. Before we get into the two approaches, one important point to note. It seems that with some fonts, mostly Swiss and Dutch, the font name is abbreviated in AutoCAD's STYLE dialog.  Some of the common abbreviations used are:
Bd = Bold
Blk = Black
Cn = Condensed
Ex = Extended
It = Italic
Out = Outline
Rm = Roman
Xbd = Extra Bold
For example:
Swis721 BlkEx BT  would be written as  Swiss 721 Black Extended BT
Swis721 BdCnOut BT  would be written as  Swiss 721 Bold Condensed Outline BT
Dutch801 Rm BT  would be written as  Dutch 801 Roman BT
Dutch801 Xbd BT  would be written as  Dutch 801 Extra Bold BT
Note: Using Windows Explorer, you can see the actual spelling of the font names, in the Fonts directory (ex: C:\Windows\Fonts).
Again, Windows' Fonts directory lists the font names and the related .ttf filename.  For example: Swiss 721 Bold Condensed Outline BT is found in the file swisscbo.ttf.  With this information, we can proceed to entmake a new text style.  First, the old AutoLISP approach, using entmake:
;;Style: myNewStyle
;;Font Name: Swiss 721 Bold Condensed Outline BT
;;Fontfile: swisscbo.ttf
(if (not (tblsearch "STYLE" "myNewStyle"))
    (entmake '((0 . "STYLE")
                     (100 . "AcDbSymbolTableRecord")
                     (100 . "AcDbTextStyleTableRecord")
                     (2 . "myNewStyle") ;style name
                     (3 . "swisscbo.ttf") ;font file
                     (70 . 0)
                     (40 . 0.0)
                     (41 . 1.0)
                     (50 . 0.0)
                     (71 . 0)
                    )
    )
    (princ "\n Style already defined")
)
  The Visual LISP (ActiveX) approach is as follows:
  ;;Style: myNewStyle
;;Font Name: Swiss 721 Bold Condensed Outline BT
;;Fontfile: swisscbo.ttf
(vl-load-com)
(setq acadApp (vlax-get-Acad-object))
(setq acadDoc (vla-get-ActiveDocument acadApp))
(setq styles (vla-get-textstyles acadDoc))
  ;; Add the style named "myNewStyle"
(setq objStyle (vla-add styles "myNewStyle"))

;; Assign fontfile "swisscbo.ttf" to the style
(setq ff "c:\\winnt\\fonts\\swisscbo.ttf") ;your path may be different
(vla-put-fontfile objStyle ff)

;; Optional: Make the new style Active
(vla-put-activetextstyle acadDoc objStyle)
(princ)

## 评论

**内容**: James carr said...
I have been looking for a way to change the font STYLE. I can create the style name and get the ttf font. i do not see how to put the font STYLE(bold, italic, etc). For example, i am trying to get the Cambria to be Cambria Regular. I can use the Cambria Bold (cambriab.ttf). But I have to manually change it in the dialog box to Regualar. I cannot do so with lisp so far.
Using this - (defun c:getfontstyle (/ e ST) (setq ST (getstring "What is the Font Style Name") e tblobjname "STYLE" ST))(entget e '("*")) );end lisp - I see (-3 ("ACAD" (1000 . "Cambria"), but how do i set it to that, the Regular font style? Still looking.
james@fredwilson.com
Reply
01/09/2018 at 07:00 AM

---
**内容**: Chris Schildmeier said in reply to James carr...
Your specific example..I'm not sure I understand. Why wouldn't you just call cambria.ttf? Why are you specifying cambriaB if you don't want bold?
Does this help?
(vl-load-com)
(setq doc (vla-get-activedocument (vlax-get-acad-object)))
(setq styleCol (vla-get-textstyles doc))
(setq myStyle (vla-add styleCol "YourTextStyle"))
(vla-setfont myStyle "Cambria" :vlax-False :vlax-False 0 32)
Reply
01/24/2018 at 10:18 AM

---
