---
title: "Filtering does not work for MoveGripPointsAt"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - Database
description: "We are using several overrules and we found that MoveGripPointsAt is not being called continuously as the grip point is being dragged. It turned ou..."
author: Autodesk
---
# Filtering does not work for MoveGripPointsAt

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/filtering-does-not-work-for-movegrippointsat.html

## 文章内容

By Adam Nagy
We are using several overrules and we found that MoveGripPointsAt is not being called continuously as the grip point is being dragged. It turned out to happen only when we have two overrules using MoveGripPointsAt but filtering for different entities. It seems that filtering does not work for this event and the last registered overrule's MoveGripPointsAt is being called instead of the one that should be called based on the filtering. However, filtering works fine with GetGripPoints.
Solution
MoveGripPointsAt does not honor filtering as that only works on database resident entities and the instance being used by MoveGripPointsAt is an in-memory shallow copy of the entity whose grip point is being dragged. On the other hand GetGripPoints works with database resident entities so filtering works fine with it.
The solution is to do the filtering yourself inside the MoveGripPointsAt function. Since you already add XData to the entities you want to filter on - and XData is copied with the entity even in case of a shallow copy like the one being used by MoveGripPointsAt - therefore you can use that.
public class TestingOverrule : GripOverrule
{
  public const string kAppName = "TestProject";
    public static TestingOverrule theOverrule =
      new TestingOverrule();
    public override void MoveGripPointsAt
      (Entity entity,
        GripDataCollection grips,
        Vector3d offset,
        MoveGripPointsFlags bitFlags)
  {
    using (ResultBuffer rb = entity.GetXDataForApplication(kAppName))
    {
      // If it does not have the XData, then just
      // call base class and return
      if (rb == null)
      {
        base.MoveGripPointsAt(entity, grips, offset, bitFlags);
        return;
      }
    }
      // ...
  }
}

## 评论

**内容**: David said...
Hello Adam,
Is ther any way in grip overrule, not to show, a dynamic block insertion point grip ?
Regards,
David.
Reply
11/06/2012 at 10:03 PM

---
**内容**: Adam Nagy said...
Hi David,
Might be possible if you override the GetGripPoints function and then call the base class' function first then remove the point added by the dynamic block.
The question might be how to identify the insertion point.
I think you should be able to get that information from the dynamic block then iterate through the points and compare their value to the point you want to remove.
I hope this helps.
Cheers,
Adam
Reply
11/12/2012 at 04:34 AM

---
**内容**: David said in reply to Adam Nagy...
Adam,
Thanks for getting back to me.
I don't even know how to start that. A little bit more help/sample code would be a great help, if you don't mind.
I really need to hide the insertion point(Grip) of dynamic blocks because it interferes with other dynamic block grips.
Regards,
David.
Reply
11/21/2012 at 12:05 PM

---
**内容**: Adam Nagy said...
Hi David,
Here you are: http://adndevblog.typepad.com/autocad/2012/11/remove-insertion-grip-point-using-overrule.html
I hope this helps.
Cheers,
Adam
Reply
11/23/2012 at 09:17 AM

---
**内容**: David said in reply to Adam Nagy...
Adam,
Thanks a Lot, I struggled for about 2 months.
Autodesk should be proud to have you there.
Reply
11/28/2012 at 05:31 AM

---
**内容**: dba said...
Hello Adam,
I use Grippointoverrule for adding custom Grips to my blockrefs (filtered by name prefix). It works fine, the only thing I experienced is, that attributreferences will not be dragged and moved by MoveGripPointsAt. Am I missing something?
Thanks in advance,
Daniel
Reply
08/13/2013 at 12:11 AM

---
**内容**: Balaji said in reply to dba...
Hi Daniel,
Sorry for the delay.
I tried using a grip overrule on a block reference that had attribute references in it. Unfortunately I could not reproduce the behavior that you mentioned. When moving using the overruled grip, the attribute references moved along with the block reference. Here is the code that I used :
https://www.dropbox.com/s/9pmgdw5mqze6thi/Class1.cs
Can you please share a non-confidential code sample for me to reproduce the behavior ?
Thanks.
Regards,
Balaji
Reply
09/09/2013 at 06:40 AM

---
**内容**: dba said in reply to Balaji...
Hello Balaji,
thanks for the reply. I will compare your code with mine to see if I'm wrong somewhere. I'll try to share some content of mine, but that will be a bit tricky because of the surrounding it works in :-)
BR,
Daniel
Reply
09/10/2013 at 03:21 AM

---
