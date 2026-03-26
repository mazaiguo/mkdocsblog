---
title: "The STARTUP system variable and the StartUpType environment variable"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "With the value of the STARTUP system variable set to 0, the user is only given the option of using a template.  If it was set to 1, this would enab..."
author: Autodesk
---
# The STARTUP system variable and the StartUpType environment variable

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/the-startup-system-variable-and-the-startuptype-environment-variable.html

## 文章内容

By Gopinath Taget
With the value of the STARTUP system variable set to 0, the user is only given the option of using a template.  If it was set to 1, this would enable a user to 1) start a drawing from scratch, 2) use a template, or 3) use a wizard.  You can of course control this programatically.
(defun-q MyStartup ( / app doc)
   (vl-load-com)
   (setq app (vlax-get-acad-object)
           doc (vla-get-activedocument app)
   ) ;setq 
   (if (= (substr (vlax-variant-value
   (vla-getvariable doc "ACADVER")) 1 2) "17")
      (vla-setvariable doc "STARTUP"
       (vlax-make-variant 1 vlax-vbInteger))
   )
   (princ)
)
(setq S::STARTUP (append S::STARTUP MYSTARTUP))
You can change the default option for the dialog by setting the StartUpType variable as shown below:
;To start from Scratch
(setenv "StartUpType" "Scratch")
  ;To use a Template
(setenv "StartUpType" "T?emplate")
  ;To use a Wizard
(setenv "StartUpType" "Wizard")

