---
title: "Event for PaletteSet Close"
date: 2012-04-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Palette
description: "PaletteSet in AutoCAD is hidden when its close button is clicked. To know when the palette is being closed, the "StateChanged" event can be used. H..."
author: Autodesk
---
# Event for PaletteSet Close

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/event-for-paletteset-close.html

## 文章内容

By Balaji Ramamoorthy
PaletteSet in AutoCAD is hidden when its close button is clicked. To know when the palette is being closed, the "StateChanged" event can be used. Here is a sample code :
using Autodesk.AutoCAD.Windows;
  static PaletteSet m_PalSet = null;
  [CommandMethod (
                 "ShowMyPalette",
                 CommandFlags.Modal | CommandFlags.Session
                )]
static public void Test1Method()
{
    Document doc
            = Application.DocumentManager.MdiActiveDocument;
      Database db = doc.Database;
    Editor ed = doc.Editor;
      if (m_PalSet == null)
    {
        m_PalSet = new PaletteSet("WPF Palette", new Guid());
          m_PalSet.Size = new Size(400, 600);
        m_PalSet.DockEnabled =
            (DockSides)((int)DockSides.Left
                        + (int)DockSides.Right);
          // For a WPF user control
        MyWPFUserControl uc = new MyWPFUserControl();
        m_PalSet.AddVisual("AddEnt", uc);
          // For a WinForm user control
        //MyWinFormUserControl uc = new MyWinFormUserControl();
        //m_PalSet.Add("Test", uc);
          m_PalSet.StateChanged += new PaletteSetStateEventHandler
                                    (
                                        PaletteSet_StateChanged
                                    );
          // Display our palette set
        m_PalSet.EnableTransparency(true);
        m_PalSet.KeepFocus = true;
    }
    m_PalSet.Visible = true;
 }
  static void PaletteSet_StateChanged(
                                    object sender,
                                    PaletteSetStateEventArgs e
                                 )
{
    Editor ed
        = Application.DocumentManager.MdiActiveDocument.Editor;
      ed.WriteMessage (
                        "\nPalette StateChanged ! New State is : "
                        + e.NewState.ToString()
                    );
}

## 评论

**内容**: Artvegas said...
A quote from Kean...
"The StateChanged event tells you when a palette set is hidden or shown, but it reports that the dialog has been hidden even when closed (basically as we don’t really close the palette set when the user hits the “X”, we just hide it)."
To know when the palette is actually closed check these posts:
http://through-the-interface.typepad.com/through_the_interface/2011/12/finding-out-when-a-custom-paletteset-is-closed-in-autocad-using-net.html
http://through-the-interface.typepad.com/through_the_interface/2011/12/creating-a-custom-paletteset-class-exposing-a-close-event-inside-autocad-using-net.html
http://through-the-interface.typepad.com/through_the_interface/2011/12/creating-a-custom-paletteset-class-exposing-a-close-event-inside-autocad-using-net-take-2.html
Reply
05/19/2012 at 06:03 AM

---
**内容**: joan said...
I use the inherited class of Tony Tanzillo (TT) and it really works nice:
http://www.theswamp.org/index.php?topic=42179.msg476706#msg476706
Reply
02/20/2015 at 11:59 AM

---
**内容**: garfield said in reply to joan...
perfect
Reply
06/28/2023 at 05:33 AM

---
