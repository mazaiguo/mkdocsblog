---
title: "Making your Custom Entity worldDraw or viewportDraw fast"
date: 2013-04-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "My Custom Entity is rather complex, whenever my users call the Rotate or Move command or basically do something which requires continual updating o..."
author: Autodesk
---
# Making your Custom Entity worldDraw or viewportDraw fast

发布日期: 2013-04-01

原始链接: https://adndevblog.typepad.com/autocad/2013/04/making-your-custom-entity-worlddraw-or-viewportdraw-fast.html

## 文章内容

by Fenton Webb
Issue
My Custom Entity is rather complex, whenever my users call the Rotate or Move command or basically do something which requires continual updating of the graphics it becomes very jerky and slow. How can I improve this?
Solution
All of the Graphics Primitive functions housed in the AcGiGeometry class return an Adesk::Boolean. It is this return value that must be checked for a value of True so that AutoCAD can efficiently allow degradation of the graphics redraw in order to maintain UI performance.
If the return value comes back as True it is because the Graphic system calculated that the Minimum Frames Per Second (FPS) setting in the Graphics Configuration is being reached *and* that there is a Mouse interaction already in the input queue waiting to be utilized. A condition of True requires that your worldDraw/viewportDraw returns as quickly as possible back to AutoCAD.
Here is an example:
Adesk::Boolean MyEntity::worldDraw(AcGiWorldDraw *wd)
{
    assertReadEnabled();
    // do some enormous amount of work
    for (int i=0; i<1000000; ++i)
    {
        // check if AutoCAD is telling you that the user has input pending
        if (wd->geometry().circle(.., .., ..))
            return (false); // abort the work, because a new draw is required
    }
}

## 评论

**内容**: Loic said...
hi,
Is this even true for AcGiGeometry::draw calls?
Thank you
Reply
04/15/2013 at 04:43 AM

---
**内容**: Fenton Webb said...
Hi Loic
yes, it's true!!
You can also check inputPending() for AutoCAD side user interaction checking.
Reply
04/15/2013 at 08:20 AM

---
**内容**: Loic said...
god, I've never noticed that before, I've yet developed many (sometimes complex) subWorldDraw overrides, shame on me, thanks to you!
Reply
04/15/2013 at 11:23 PM

---
**内容**: Fenton Webb said...
Hi Loic
no problem. One last thing, if you use DrawJigs, then the same rule applies. If you use AcEdJig, then you should check inputPending() for long iterations in your code - otherwise it's handled by AutoCAD automatically.
Reply
04/16/2013 at 09:04 AM

---
**内容**: Loic Jourdan said in reply to Fenton Webb...
good tip indeed, I'll double check but I'm pretty sure it applies once in my code
thanks
Reply
04/16/2013 at 10:53 PM

---
**内容**: Loic said...
Hi Fenton,
One last question, can we test AcGiCommonDraw::regenAbort return as well?
i.e. would these pseudo-code equivalent? (sorry for indent)
----
for each (ent in ents){
if (mode->geometry().draw(ent)) //your tip
break;
}
----
for each (ent in ents){
mode->geometry().draw(ent);
if (mode->regenAbort())
break;
}
----
this question because, somewhere in my code, I have a custom acgiworlddraw/acgigeometry with draw(AcGiDrawable*) overrided and I wonder if this method has to return the result of AcGiCommonDraw::regenAbort in order to behave correctly.
Thank you
Reply
04/26/2013 at 04:27 AM

---
**内容**: Fenton Webb said...
Hey Loic!
you are absolutely right, regenAbort() informs you when you should not waste anymore time creating your geometry.
Thanks for the reminder, it seems you got a lot out of this one which is nice to hear
Reply
04/26/2013 at 08:50 AM

---
