---
title: "Saving a file with password (Lisp)"
date: 2012-12-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
  - COM
description: "First we need to create a AcadSecurityParams ActiveX object with some required properties, then call the SaveAs passing this parameter. The followi..."
author: Autodesk
---
# Saving a file with password (Lisp)

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/saving-a-file-with-password-lisp.html

## 文章内容

By Augusto Goncalves
First we need to create a AcadSecurityParams ActiveX object with some required properties, then call the SaveAs passing this parameter. The following code sample demonstrate it using AutoCAD default values.
(setq secparam 
(vla-getinterfaceobject (vlax-get-acad-object)
(strcat "autocad.securityparams.19")))

(vla-put-Action secparam 1) ;; ACADSECURITYPARAMS_ENCRYPT_DATA
(vla-put-Algorithm secparam 26625) ;; ACADSECURITYPARAMS_ALGID_RC4
(vla-put-KeyLength secparam 40) ;; default
(vla-put-password secparam "MyPass") ;; specify here...
(vla-put-ProviderName secparam 
"Microsoft Base Cryptographic Provider v1.0") ;; default
(vla-put-ProviderType secparam 1) ;; default

(setq activedoc (vla-get-ActiveDocument (vlax-get-Acad-Object)))
(setq fileName "c:\\temp\\passwordFile.dwg")
(setq version 60) ;; 2013 DWG
(vlax-invoke-method activedoc 'SaveAs fileName version secparam)

## 评论

**内容**: Leo said...
I used a similar approach saving a file with password.
But opening it using:
(vla-open activedoc fileName :vlax-false "MyPass")
returns an error:
; error: Automation Error. Error Decrypting Data
Any idea?
Thanks in advance
Reply
01/30/2013 at 01:29 AM

---
**内容**: Augusto Goncalves said in reply to Leo...
Hi Leo,
I tried with the code below and worked fine. Are you sure the password is correct?
(setq filename "c:/temp/password.dwg")
(setq password "MyPass")
(setq docs (vla-get-documents (vlax-get-acad-object)))
(vla-open docs filename :vlax-false password)
Reply
01/30/2013 at 03:30 AM

---
**内容**: Leo said...
(defun c:lock ()
(setq secparam
(vla-getinterfaceobject (vlax-get-acad-object)
(strcat "autocad.securityparams.19")))
(vla-put-Action secparam 1)
(vla-put-Algorithm secparam 26625)
(vla-put-KeyLength secparam 40)
(vla-put-password secparam "MyPass")
(vla-put-ProviderName secparam
"Microsoft Base Cryptographic Provider v1.0")
(vla-put-ProviderType secparam 1
(setq activedoc (vla-get-ActiveDocument (vlax-get-Acad-Object)))
(setq fileName "c:\\temp\\passwordFile.dwg")
(setq version 60
(vlax-invoke-method activedoc 'SaveAs fileName version secparam)
(alert "You successfully locked this drawing.")
(princ)
)
(defun c:un_lock ()
(setq filename "c:/temp/passwordFile.dwg")
(setq password "MyPass")
(setq docs (vla-get-documents (vlax-get-acad-object)))
(vla-open docs filename :vlax-false password)
(princ)
)
(princ)
Sir,
This is what I have so far.
I changed "c:/temp/password.dwg" to "c:/temp/passwordFile.dwg"
lock - should lock the drawing (OK)
un_lock - should open the drawing without password popup (Not OK, still popup the password, if cancel then error)
I also tried different values of "dwgcheck" variable but still not OK
Thank you very much for the time sir.
Reply
01/30/2013 at 06:34 PM

---
**内容**: Leo said...
Got it to work only for insert.
(vla-InsertBlock obj pnt filName 1 1 1 0 "MyPass")

Thank you sir,
Reply
02/12/2013 at 06:15 PM

---
**内容**: nath said...
it doesn't work.
;errors: Automation Error. Invalid argument
so i replace the first line as below to work with another version.
(setq secparam (vla-getinterfaceobject (vlax-get-acad-object) (strcat
"autocad.securityparams." (rtos (fix (atof (getvar "ACADVER"))) 2 0))))
then got error
; error: Automation Error. Error saving the document
and i tried to change version to 61, it saves as DXF without error.
Please help.
thanks.
Reply
10/04/2016 at 11:53 PM

---
**内容**: Zakaria said in reply to nath...
Dear Nath,
In AutoCAD 2016 and up, this feature is not supported.
Reply
11/16/2016 at 02:04 AM

---
