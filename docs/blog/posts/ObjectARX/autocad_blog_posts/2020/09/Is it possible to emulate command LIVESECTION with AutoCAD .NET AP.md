---
title: "Is it possible to emulate command LIVESECTION with AutoCAD .NET AP"
date: 2020-09-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
description: "This question is coming from one of our beloved Forum contributor and Mentor Alexander Rivilis"
author: Autodesk
---
# Is it possible to emulate command LIVESECTION with AutoCAD .NET AP

发布日期: 2020-09-01

原始链接: https://adndevblog.typepad.com/autocad/2020/09/is-it-possible-to-emulate-command-livesection-with-autocad-net-ap.html

## 文章内容

By Madhukar Moogala
This question is coming from one of our beloved Forum contributor and Mentor Alexander Rivilis
I am working with code which change color of Intersection Fill of Live Section. But although the color is changed, but this is not visible on the screen until I turn off and turn LIVESECTION:
I made slight changes to have this working
Note: To work this make sure LIVESECTION is not turned on
This code will change color of SECTION which converted to LIVESECTION
    public void SetSectionColor()
       {
          Document doc = Application.DocumentManager.MdiActiveDocument;
          if (doc == null) return;
          Editor ed = doc.Editor;

          PromptEntityOptions peo = 
                new PromptEntityOptions("\nSelect section: ");
          peo.SetRejectMessage("\nIt is not a section!");
          peo.AddAllowedClass(typeof(Section), true);
          PromptEntityResult per = ed.GetEntity(peo);
          if (per.Status != PromptStatus.OK) return;
          ObjectId idSecSets = ObjectId.Null;
          using (Transaction tr =
          doc.TransactionManager.StartOpenCloseTransaction())
          {
              Section sec =
              tr.GetObject(per.ObjectId,
                           OpenMode.ForWrite) as Section;
              sec.IsLiveSectionEnabled = true;                
              idSecSets = sec.Settings;
              tr.Commit();
          }
        using (Transaction tr = doc.TransactionManager
                                     .StartOpenCloseTransaction())
        {
          SectionSettings secset = tr.GetObject(idSecSets, 
                                   OpenMode.ForWrite) as SectionSettings;
          secset.CurrentSectionType = SectionType.LiveSection;
          Color clr = secset.Color(SectionType.LiveSection,
                                   SectionGeometry.IntersectionFill);
          ColorDialog cd = new ColorDialog
          {
              Color = clr
          };
          System.Windows.Forms.DialogResult dr = cd.ShowDialog();
          if (dr != System.Windows.Forms.DialogResult.OK) return;
          ed.WriteMessage("\nSelected Color: " + cd.Color.ToString());
          clr = cd.Color;
          // Define that color we change
          secset.SetColor(SectionType.LiveSection,
          SectionGeometry.IntersectionFill, clr);
          tr.Commit();
        }  
    }
Gif

## 评论

**内容**: Alexander Rivilis said...
And what about LIVESECTION was turned on and I need only change color of Intersection Fill?
Reply
09/26/2020 at 12:21 PM

---
**内容**: wordle hint said...
This code will change the color of the changed section to LIVESECTION. I never do it before.
Reply
09/19/2022 at 06:45 PM

---
