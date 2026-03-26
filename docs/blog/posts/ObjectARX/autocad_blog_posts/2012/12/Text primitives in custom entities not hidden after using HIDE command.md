---
title: "Text primitives in custom entities not hidden after using HIDE command"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Unicode
description: "Consider this: You have created a Custom Entity and among other primitives in the worldDraw, you draw a text (mode->geometry().text). After placing..."
author: Autodesk
---
# Text primitives in custom entities not hidden after using HIDE command

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/text-primitives-in-custom-entities-not-hidden-after-using-hide-command.html

## 文章内容

By Gopinath Taget
Consider this: You have created a Custom Entity and among other primitives in the worldDraw, you draw a text (mode->geometry().text). After placing the custom entity, When you run the HIDE command in 2D wireframe mode, the text in the custom entity is not hidden. Furthermore, when the text is drawn as a part of the custom entity, some of the other primitives may not be hidden correctly. This problem does not occur when the custom entity  does not have any text primitives.
You might have also noticed that the standard AcDbText entities are not hidden some times. So what is the problem?
You could first try setting the "HIDETEXT" system variable to ON (if it is OFF) at the AutoCAD command prompt. If this does not work, you could try setting thickness to the text. This is because Text objects such as those created by the TEXT, DTEXT, or MTEXT commands are in some cases not affected by the HIDE command. In such cases, for text to be hidden, you need to assign a thickness to the text. The value set for the thickness only needs to be a non-zero value, such as .0001. The programmatic equivalent of this is:
double thickOld = mode->subEntityTraits().thickness();       
mode->subEntityTraits().setThickness(0.001);  
mode->geometry().text( ... );  
mode->subEntityTraits().setThickness(thickOld);
Of course, for standard AcDb(M)Text, setThickness() should be used directly on the objects.

## 评论

**内容**: Abhay Joshi said...
Hello,
I have reverse situation, I need to draw Filled area in hide mode.
Currently I am using mesh. Can you suggest some way to do that?
Abhay
Reply
12/23/2015 at 12:17 AM

---
