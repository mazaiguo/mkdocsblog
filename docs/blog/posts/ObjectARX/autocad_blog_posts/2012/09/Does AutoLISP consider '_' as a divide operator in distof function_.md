---
title: "Does AutoLISP consider '/' as a divide operator in distof function?"
date: 2012-09-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Unicode
description: "Does the distof function interpret the / divide operator and not any other arithmetic operator?"
author: Autodesk
---
# Does AutoLISP consider '/' as a divide operator in distof function?

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/does-autolisp-consider-as-a-divide-operator-in-distof-function.html

## 文章内容

By Xiaodong Liang
Issue
Does the distof function interpret the / divide operator and not any other arithmetic operator?
Solution
In this context, / is not interpreted as a divide operator.  It actually
represents the separator for the fraction.  The manner in which the distof function uses the divide operator in this situation is as designed.  For example:
Command: (distof "100/2" 2)
50.0
The distof function in this case will not return nil, and the value the function returns is correct because "100/2" is a valid fraction.
Command: (distof "100 100/2" 4)
nil
In this case, because "100 100/2" is not a valid architectural fraction, the distof function returns nil.
Command: (distof "100 2/100" 4)
100.02
Because "100 2/100" is a valid fraction, the distof function returns 100.02.

## 评论

**内容**: masterhe3000 said...
英文不好，请教个子实体的问题：如何在属性框中显示子实体的属性。SDK自带示例：SubEntity，虽然说："Property Palette will display the properties of the sub-entity selected. For example, if the piston sub-entity is selected the size and the skirt-length of the piston will be displayed.",但运行该示例时当选中了子实体，在属性框却不显示子实体的属性。
请问如何解决此问题，谢谢！
Reply
09/10/2012 at 07:57 PM

---
**内容**: Xiaodong Liang said in reply to masterhe3000...
hi，
As I remember，AsdkSliderCrankDb.dbx implemented the relevant COM wrapper。Please check if the registry info is correct. Typically, it would locate at:
HKEY_LOCAL_MACHINE>SOFTWARE>Autodesk>ObjectDBX>R**>ActiveXCLSID
Where ** is the version number such as 18.0, 19.0…
This blog site supports English only. If you are an ADN, please log case with the normal process. If you are not, I would suggest you post question on the local forums of China which talks about AutoCAD APIs.
Regards,
Xiaodong
Reply
09/21/2012 at 12:20 AM

---
