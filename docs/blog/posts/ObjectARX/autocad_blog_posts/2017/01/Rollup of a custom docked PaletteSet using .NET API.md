---
title: "Rollup of a custom docked PaletteSet using .NET API"
date: 2017-01-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - Palette
description: "This is my first post of 2017 and here is wishing you all a "Happy New Year" :-)"
author: Autodesk
---
# Rollup of a custom docked PaletteSet using .NET API

发布日期: 2017-01-01

原始链接: https://adndevblog.typepad.com/autocad/2017/01/rollup-of-a-custom-docked-paletteset-using-net-api-.html

## 文章内容

By Deepak Nadig
This is my first post of 2017 and here is wishing you all a "Happy New Year" :-)
Recently, we had a query from an ADN partner:
How to roll up a docked and hidden custom PaletteSet using.NET  API ?
The behaviour the ADN partner is expecting to be accomplished using .NET API can be seen in the below screencast:  
With the help of my colleague Madhu, we figured out the answer is to set PaletteSet.RolledUp to false.
In the below code, command MyPalette launches a docked palette and command ExpandPalette rolls up the palette. Subsequently, screencast shows the testing of the code.
public class MyCommands
{
    static System.Windows.Forms.Timer Clock;
    public static PaletteSet m_ps = null;
    [CommandMethod("MyPalette")]
    public void MyPalette()
    {
        if (m_ps == null)
        {
            m_ps = new PaletteSet("My Palette 1",
            new Guid("170B0084-7B01-487E-9CBC-C7018588F26F"));
            m_ps.SetLocation(new System.Drawing.Point(312, 763));
            m_ps.SetSize(new System.Drawing.Size(909, 40));
            m_ps.DockEnabled = DockSides.Bottom;
            if (m_ps.Dock == DockSides.None)
            {
                m_ps.AutoRollUp = true;
                m_ps.Visible = false;
                m_ps.Visible = true;
            }
            // If the palette is docked,
            // we need to undock it first.
            else
            {
                m_ps.Visible = false;
                m_ps.Visible = true;
                CreateTimer();
            }
        }
        m_ps.Visible = true;
    }
    public static void CreateTimer()
    {
        Clock = new System.Windows.Forms.Timer();
        Clock.Interval = 500;
        Clock.Start();
        Clock.Tick += new EventHandler(Timer_Tick);
    }
    static public void Timer_Tick(object sender,
    EventArgs eArgs)
    {
        if (sender == Clock)
        {
            m_ps.Dock = DockSides.None;
            m_ps.AutoRollUp = true;
            m_ps.Dock = DockSides.Left;
            // Note: we need to update the palette
            // window. I found turning it off and
            // on is the most robust way.
            m_ps.Visible = false;
            m_ps.Visible = true;
            // Stop the clock and destroy it.
            Clock.Stop();
            Clock.Dispose();
        }
    }
    [CommandMethod("ExpandPalette")]
    public static void CheckPaletteSetState()
    {
        if (m_ps != null)
        {
            m_ps.RolledUp = false;
        }
    }
}
  Screencast :

## 评论

**内容**: James Maeding said...
Just a note - you really should make that first param of new palletset like:
ps = new AcWn.PaletteSet("", new Gu....
as that string is the command to open the palette, not the name. Then you add the name like:
ps.Name = "My Cool Palette";
The trouble with not doing that is if a palette was open last session, it tries to open in next and the command has spaces in it. "My Palette 1" will confuse the heck out of acad on startup.
Reply
01/17/2017 at 08:13 AM

---
**内容**: mapquest directions said...
MapQuest Directions is an online platform that provides users with maps, driving directions, and other navigation features. It is one of the most popular and trusted navigation services in the world, with millions of users every day.
Reply
10/22/2023 at 09:08 PM

---
