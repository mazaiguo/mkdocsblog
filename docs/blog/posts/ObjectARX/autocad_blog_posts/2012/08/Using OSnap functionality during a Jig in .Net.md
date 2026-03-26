---
title: "Using OSnap functionality during a Jig in .Net"
date: 2012-08-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Selection
description: "I would like to take advantage of my OSNAP settings while jigging my entity, so it looks like it sticks to the closest snapped point while user is ..."
author: Autodesk
---
# Using OSnap functionality during a Jig in .Net

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/using-osnap-functionality-during-a-jig-in-net.html

## 文章内容

By Philippe Leefsma
Q:
I would like to take advantage of my OSNAP settings while jigging my entity, so it looks like it sticks to the closest snapped point while user is still moving the cursor.
I was trying to use some of the Editor selection methods, but it doesn't seem to work.
A:
The Editor functionalities such as selections cannot be performed while the jig is running.
A solution to implement this requirement is to set the osnap options before starting the jig, to “End Point” for example. That can be done programmatically as well using the OSMODE system variable. Then inside your jig use a PointMonitor to get the snapped point.
Here is an example of my Jig class that illustrates that. A full sample is available as attachment:
class CoSnapJig : EntityJig
{
    private Point3d _previousPos;
    private Point3d _position;
    private Editor _ed;
      public CoSnapJig(): base(new DBText())
    {
        _ed = Application.DocumentManager.MdiActiveDocument.Editor;
          DBText dbTxt = (DBText)Entity;
        dbTxt.TextString = "Jigged DBText";
          _ed.PointMonitor +=
            new PointMonitorEventHandler(ed_PointMonitor);
    }
      void ed_PointMonitor(object sender, PointMonitorEventArgs e)
    {
        _position = e.Context.ComputedPoint;
    }
      public new Entity Entity
    {
        get
        {
            return base.Entity;
        }
    }
      protected override SamplerStatus Sampler(JigPrompts prompts)
    {
        JigPromptPointOptions options =
            new JigPromptPointOptions("\nSpecify position: ");
          options.UserInputControls = UserInputControls.NoZeroResponseAccepted;
        options.Cursor = CursorType.Crosshair;
          PromptPointResult promptRes = prompts.AcquirePoint(options);
          if (_previousPos == promptRes.Value)
            return SamplerStatus.NoChange;
          _previousPos = promptRes.Value;
          return SamplerStatus.OK;
    }
      protected override bool Update()
    {
        DBText oTxt = (DBText)Entity;
        oTxt.Position = _position;
        return true;
    }
      public PromptStatus Run()
    {
        PromptResult promptResult =
            Application.DocumentManager.MdiActiveDocument.Editor.Drag(this);
          return promptResult.Status;
    }
}
OSnapJig.zip

## 评论

**内容**: Chuck said...
Wow, that was timely. I needed this just now, and this article is all of 4 days old. Glad you posted it when you did. Thanks.
Reply
08/14/2012 at 03:43 PM

---
**内容**: Smith said...
Hi. how can i get the Point1 on the circle after select the circle.
i need determine this point1 to move circle to exactly the point2
i cannot using osnap while select object.
Reply
11/06/2019 at 12:43 AM

---
**内容**: Wess Wesselink said...
Is there a jig for the following?
If you draw a line with the LINE command and you select an arc with object snap tangent as start point AutoCAD moves the line along the tangent of the selected arc until you pick an end point.
Reply
03/22/2022 at 02:46 PM

---
**内容**: Norman Yuan said...
I was wandering this blog and accidently saw your question. I do not know if THERE IS already a jig available for you to use, created by someone; but it is certainly can be done if you do ACAD .NET API programming. Based on your description, as long as you can find the tangent point of an intended line to an arc, the jig's task would be to simply draw a line from the mouse point to the calculated tangent point. I happened to have posted an article on this topic:

Reply
03/27/2022 at 05:56 AM

---
**内容**: Norman Yuan said...
Well, the link was cut off for some reason. Here is it again:
https://drive-cad-with-code.blogspot.com/2022/02/where-tangent-point-is-show-it-when.html
Reply
03/27/2022 at 05:57 AM

---
