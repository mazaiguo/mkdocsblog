---
title: "LISP: atof does not return the complete number of the input string"
date: 2013-01-01
categories:
  - AutoLISP
tags:
  - AutoLISP
description: "Consider this: You are trying to convert a string in lisp to a real number using atof and the number appears truncated. Is there a way to get the c..."
author: Autodesk
---
# LISP: atof does not return the complete number of the input string

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/lisp-atof-does-not-return-the-complete-number-of-the-input-string.html

## 文章内容

By Gopinath Taget
Consider this: You are trying to convert a string in lisp to a real number using atof and the number appears truncated. Is there a way to get the complete number:
Command: ﻿(atof "1234.34456"﻿)
1234.34
The number is not rounded off internally. The number displayed on the command line is however. You can use the rtos function to get the complete number when all the digits need to be seen by the user.
Command: (setq test (atof "0.4732223983"))
0.473222
Command: (rtos test 2 10)
"0.4732223983"

## 评论

**内容**: maycol said...
Hi, I have the trouble too. I need convert the string complete in number.
Example ﻿(atof "123456789.344") ---> 123456789.34, but atof not is command good for this. the result is
(atof "123456789.344") --->1.23457e+008 (I not need this).
I need the next.
(xxxx "123456789.344"﻿) ---> 123456789.344, I dont know that is xxxx for convert to number complete 1234.34456
Reply
01/07/2014 at 07:49 PM

---
**内容**: maycol said...
I need the next.
(xxxx "123456789.344"﻿) ---> 123456789.344, I dont know that is xxxx for convert to number complete 123456789.344
Reply
01/07/2014 at 07:50 PM

---
