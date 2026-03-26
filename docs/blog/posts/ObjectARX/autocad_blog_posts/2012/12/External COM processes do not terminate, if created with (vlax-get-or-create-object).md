---
title: "External COM processes do not terminate, if created with (vlax-get-or-create-object)"
date: 2012-12-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - COM
description: "It is recommended that developers call (vlax-release-object...) on all external objects after they are done with them. However, it should be noted ..."
author: Autodesk
---
# External COM processes do not terminate, if created with (vlax-get-or-create-object)

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/external-com-processes-do-not-terminate-if-created-with-vlax-get-or-create-object.html

## 文章内容

By Gopinath Taget
It is recommended that developers call (vlax-release-object...) on all external objects after they are done with them. However, it should be noted that calling (vlax-release-object...) does not always release the object at that exact time. The object is not actually released until all LISP symbols referencing the server's COM objects go out of scope or are set to nil AND a garbage-collection (gc) happens. The actual COM call to "release" happens only in a (gc) and only if LISP agrees that the object is no longer referenced.
You can force a garbage-collection with the lisp function (gc). Before you invoke Excel's Quit method, insert the call to (gc) into your code. This should allow (vlax-release-object ...) to remove Excel.exe from the process list. See below:
  (defun Test ()
   (vl-load-com)
   (setq XLAPP (vlax-get-or-create-object "Excel.Application"))
   (vlax-dump-object XLAPP T)
   (gc) ; release temporary com objects
   (vlax-invoke-method XLAPP 'Quit)
   (vlax-release-object XLAPP)
   (setq XLAPP nil)
   (gc)
)
While this technique is generally supported, it should be noted that forcing too many (gc) calls (i.e. within loops that iterate hundreds of times), will have a negative impact on performance.
NOTE: The VLIDE may be attached to many COM objects during a debug session. A COM server like Excel, will not be released until all of the internal VLIDE symbols referencing Excel objects go out of scope. The user/developer has no direct control over when the VLIDE internal symbols go out of scope. Closing the VLIDE does not make them go out of scope. The VLIDE never fully goes away once it has been started in a session. If developers are having trouble seeing the COM server released in a timely fashion, they should try running their application without ever having run the VLIDE in a session.

