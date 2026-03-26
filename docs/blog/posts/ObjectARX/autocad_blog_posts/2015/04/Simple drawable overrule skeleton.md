---
title: "Simple drawable overrule skeleton"
date: 2015-04-01
categories:
  - AutoCAD
tags:
  - Unicode
description: "We have a few samples of our blog showing how create drawable overrule. But what’s the skeleton to set up? This is actually a recurrent question on..."
author: Autodesk
---
# Simple drawable overrule skeleton

发布日期: 2015-04-01

原始链接: https://adndevblog.typepad.com/autocad/2015/04/simple-drawable-overrule-skeleton.html

## 文章内容

By Augusto Goncalves
We have a few samples of our blog showing how create drawable overrule. But what’s the skeleton to set up? This is actually a recurrent question on our support, so I decided to share what is my recommendation.
To make it work you’ll need a class that implements the DrawableOverrule class and the WorldDraw method (and the ViewportDraw is more specific). I prefer have a command to active/deactivate the overrule and make it as startup command (using bundle format). The command will check the variable and Add or Remove the overrule. Finally, remember to call Regen(), otherwise the new geometry will not appear.
The sample below should work for MText (for other types, just replace the class name).
[CommandMethod("simpleOverrule")]
public void CmdSimpleOverrule()
{
  if (_overrule == null)
  {
    _overrule = new TextOverrule();
    Overrule.AddOverrule(
      RXClass.GetClass(typeof(MText)),
      _overrule, false);
  }
  else
  {
    Overrule.RemoveOverrule(
      RXClass.GetClass(typeof(MText)),
      _overrule);
    _overrule = null;
  }
  Application.DocumentManager.MdiActiveDocument.Editor.Regen();
}
 
private static TextOverrule _overrule = null;
 
public class TextOverrule : DrawableOverrule
{
  public override bool WorldDraw(Drawable drawable, WorldDraw wd)
  {
    // draw the base class
    bool ret = base.WorldDraw(drawable, wd);
 
    // your custom code here
    //
    //
 
    // return the base
    return ret;
  }
}

## 评论

**内容**: JeffH said...
This is what I use.

public abstract class DrawableOverrule : DrawableOverrule where T : Entity
{
private readonly RXClass _targetClass = RXObject.GetClass(typeof(T));
OverruleStatus _status = OverruleStatus.Off;
public OverruleStatus Status
{
get
{
return _status;
}
set
{
if (value == OverruleStatus.On && _status == OverruleStatus.Off)
{
AddOverrule(_targetClass, this, true);
_status = OverruleStatus.On;
}
else if (value == OverruleStatus.Off && _status == OverruleStatus.On)
{
RemoveOverrule(_targetClass, this);
_status = OverruleStatus.Off;
}
}
}
protected DrawableOverrule(OverruleStatus status = OverruleStatus.On)
{
Status = status;
}
}
public enum OverruleStatus
{
Off= 0,
On = 1
}
Reply
04/22/2015 at 03:33 PM

---
**内容**: Augusto Goncalves said in reply to JeffH...
Thanks for sharing Jeff, nice implementation too :-)
Cheers,
Augusto Goncalves
Reply
04/22/2015 at 03:53 PM

---
**内容**: JeffH said in reply to Augusto Goncalves...
Thanks and sorry but angle brackets do not show up in comments missing T in some places for a generic class
Reply
04/22/2015 at 05:09 PM

---
**内容**: Alexander Rivilis said...
Hi Augusto!
You did the simple typo in your's post. Instead of DBText have to be MText.
Reply
04/23/2015 at 03:42 AM

---
**内容**: Augusto Goncalves said in reply to Alexander Rivilis...
Thanks Alexander, I have fixed it.
Reply
04/23/2015 at 04:36 AM

---
