---
title: "Default Dock location for Palette Sets"
date: 2015-02-01
categories:
  - AutoCAD
tags:
  - Palette
description: "I’ve received a query from a ADN partner on how to set default dock location for Paletteset for the first time when palette is activated and user s..."
author: Autodesk
---
# Default Dock location for Palette Sets

发布日期: 2015-02-01

原始链接: https://adndevblog.typepad.com/autocad/2015/02/default-dock-location-for-palette-sets.html

## 文章内容

By Madhukar Moogala
I’ve received a query from a ADN partner on how to set default dock location for Paletteset for the first time when palette is activated and user should be able to dock Paletteset in all directions : Bottom,Left,Top,Right later on.
Here is the simple code to illustrate the same.
public static PaletteSet ps = null;
[CommandMethod("MyPalette")]
public void MyPalette()
{     
  if (ps == null)
{
ps = new PaletteSet("My Palette 1",
new Guid("229E43DB-E76F-48F9-849A-CC8D726DF257"));
ps.SetLocation(new System.Drawing.Point(312, 763));
ps.SetSize(new System.Drawing.Size(909, 40));
/*For the first time we 'll enable on Bottom*/
ps.DockEnabled = DockSides.Bottom;
  }
ps.Visible = true;
/*Add Handler*/
ps.PaletteSetMoved += ps_PaletteSetMoved;
}
  void ps_PaletteSetMoved(object sender, PaletteSetMoveEventArgs e)
{
PaletteSet pt = sender as PaletteSet;
/*Remove Handler*/
pt.PaletteSetMoved -= ps_PaletteSetMoved;
pt.DockEnabled = DockSides.Bottom | DockSides.Left | DockSides.Top | DockSides.Right;
  }
Sample Video :

## 评论

**内容**: joan said...
Hi.
I don´t want a dockable palette, I have this:
ps.Dock = DockSides.None;
ps.DockEnabled = DockSides.None;
But it always appear under the ribbon. (Top side).
How can I fix it?
Thanks.
Reply
02/20/2015 at 10:11 AM

---
**内容**: Madhukar Moogala said in reply to joan...
Can you try renaming profile.aws and check this problem persists.
Reply
02/23/2015 at 11:14 PM

---
**内容**: joan said...
This is important:
Note that if you add a GUID to your call that creates the Palette set, Autocad will remember the location and size of the palette, even when you shut down and restart Autocad.
Reply
02/20/2015 at 11:23 AM

---
**内容**: Madhukar Moogala said in reply to joan...
Thanks your comment Joan!, sorry it took so long to get back at you.
Yes if you add GUID, it get collected in profile.aws and application remembers loc and size, once you rename profile.aws, application no more recollects your palette pos & size.
Reply
02/23/2015 at 11:14 PM

---
**内容**: Lucano Deskovic said...
I'm interested to know if there's an interface option that implements autocad "theme" to the Palette Set.
ATTM, it used the default colors I set in the VS - buttons are gray, background white,etc...etc..
is there a way for dark theme to be applied automatically to my objects.
Reply
07/08/2015 at 02:11 PM

---
