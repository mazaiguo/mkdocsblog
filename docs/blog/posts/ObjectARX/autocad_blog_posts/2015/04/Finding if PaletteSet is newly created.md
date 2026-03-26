---
title: "Finding if PaletteSet is newly created"
date: 2015-04-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Palette
description: "You may want to know if your PaletteSet is being created for the very first time to set its Docking or for any other purpose. To do this, you can s..."
author: Autodesk
---
# Finding if PaletteSet is newly created

发布日期: 2015-04-01

原始链接: https://adndevblog.typepad.com/autocad/2015/04/finding-if-paletteset-is-newly-created.html

## 文章内容

By Balaji Ramamoorthy
You may want to know if your PaletteSet is being created for the very first time to set its Docking or for any other purpose. To do this, you can save custom data when the PaletteSet gets saved which obviously will not be available at the very first time the PaletteSet is loaded.
Here is a sample code to set the default docking of a PaletteSet to DockSides.Left when it gets created. In subsequent sessions, the docking is not changed and the PaletteSet should retain the position that was set by the user.
 using  Autodesk.AutoCAD.Windows;
   static  bool  _isFirstTime = true ;
 MyUserControl ctrl = null;
 PaletteSet set = null;
   [CommandMethod("Test" )]
 public  void  commandMethodTest()
 {
     if  (set == null)
     {
         set = new  PaletteSet("MyPalette" ,
   new  Guid("{43FFB063-DF0B-474B-9856-7886305CC3E8}" ));
           set.Load += 
    new  PalettePersistEventHandler
    (ps_Load);
           set.Save += 
    new  PalettePersistEventHandler
    (ps_Save);
                           if  (ctrl == null)
         {
             ctrl = new  MyUserControl();
             set.Add("MyPalette" , ctrl);
             set.Style = PaletteSetStyles.ShowCloseButton;
         }
     }
     set.Visible = true ;
       Document doc 
   = Application.DocumentManager.MdiActiveDocument;
     Editor ed = doc.Editor;
                   if  (_isFirstTime)
     {
         ed.WriteMessage("First Time, Set the Dock status" );
         set.Dock = DockSides.Left;
         _isFirstTime = false ;
     }
     else 
     {
         ed.WriteMessage("Not the first time, Do nothing.  
    Leave it to the previous settings"); 
     }
 }
   private  static  void  ps_Load(object sender, 
  PalettePersistEventArgs e)
 {
     String sIsFirstTime = 
   (String)e.ConfigurationSection.ReadProperty
   ("IsFirstTime" , "Yes" );
     if  (sIsFirstTime.Equals("No" ))
     {
         _isFirstTime = false ;
     }
 }
   private  static  void  ps_Save(object sender, 
  PalettePersistEventArgs e)
 {
     e.ConfigurationSection.WriteProperty(
   "IsFirstTime" , "No" );
 }

## 评论

**内容**: Unknown said...
I tryed this code in AutoCAD 2008, and next time when I opened CAD, there came Unknown command "MYPALETTE"。
Reply
05/28/2015 at 11:52 PM

---
**内容**: Balaji said...
Hello,
Does this forum post help ?
http://forums.autodesk.com/t5/net/cutom-palette-save-load-position/td-p/5096382
Regards,
Balaji
Reply
05/29/2015 at 12:05 AM

---
**内容**: Unknown said in reply to Balaji...
Oh,Thank you very much,
It helps a lot, I think this is the best solution, better than the solution I found.
For now, I solved it like this:
When CAD was closed, find 'FixedProfile.aws', and remove '' from 'StartupInfo' node.
It also worked, but now, I think this is a stupid way.
Thank you for your advice.
Reply
05/29/2015 at 01:11 AM

---
