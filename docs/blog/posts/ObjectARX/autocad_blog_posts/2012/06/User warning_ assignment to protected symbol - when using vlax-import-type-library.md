---
title: "User warning: assignment to protected symbol - when using vlax-import-type-library"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "When I load my dll then I get this warning:"
author: Autodesk
---
# User warning: assignment to protected symbol - when using vlax-import-type-library

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/user-warning-assignment-to-protected-symbol-when-using-vlax-import-type-library.html

## 文章内容

By Adam Nagy
When I load my dll then I get this warning:
; User warning: assignment to protected symbol: CLOSE <- #
Also, when loading the dll for the second time, I get similar warnings for all the functions the dll contains.
Shall I just ignore these warnings?
Solution
You can and should avoid these warnings by using prefixes for the imported dll methods/properties/constants.
The best things is to use your registered developer symbol plus m/p/c depending on if it's for methods, properties or constants.
Also you can find out if the dll has already been loaded by checking if any of the methods/properties/constants are available (i.e. does not equal nil), and if they are not, only then load your dll.
Here is a sample code using my registered developer symbol, AEN1:
(defun c:loadmydll ( )
 (vl-load-com)
 ; Check if a specific function that is part of the dll
 ; if not, then the dll is not yet loaded
 ; so we load it now 
 ; This specific dll contains a function called close, 
 ; so I'm checking for that 
 (if (equal nil aen1m-close)
  (vlax-import-type-library
   :tlb-filename "C:/Test/lispCOM.dll"
   :methods-prefix "aen1m-"
   :properties-prefix "aen1p-"
   :constants-prefix "aen1c-"
  )
 )   
)

## 评论

**内容**: Irné Barnard said...
Yes you can, but no you shouldn't ignore them. E.g. the warning you posted means that the import redefined the close function. Thus there's no more way to close a file after you've opened it, and any code calling the close function might error - because it's now using the close method from your DLL instead of AutoLisp's built-in close defun.
Reply
06/26/2012 at 07:17 AM

---
**内容**: Adam Nagy said...
Thank you for the comment. I agree. Maybe there is a misunderstanding here? I said you "should avoid", which is sort of the opposite of "should ignore" :)
Reply
06/26/2012 at 07:58 AM

---
**内容**: stemfixer said...
The code you provided seems to be on the right track. Just make sure to adjust the paths and filenames according to your setup, and you should be good to go! Happy coding!
Reply
07/27/2023 at 06:13 AM

---
