---
title: "Show AutoCAD color dialog"
date: 2012-09-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "You can use “Autodesk.AutoCAD.Windows.ColorDialog” class to show the color dialog box in AutoCAD. Below code shows the procedure to show and proces..."
author: Autodesk
---
# Show AutoCAD color dialog

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/show-autocad-color-dialog.html

## 文章内容

By Virupaksha Aithal
You can use “Autodesk.AutoCAD.Windows.ColorDialog” class to show the color dialog box in AutoCAD. Below code shows the procedure to show and process the input of color dialog in AutoCAD.
[CommandMethod("showColorDlg")]
public void showColorDlg()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Editor ed = doc.Editor;
      Autodesk.AutoCAD.Windows.ColorDialog dlg
                     = new Autodesk.AutoCAD.Windows.ColorDialog();
      if (dlg.ShowDialog() !=
                              System.Windows.Forms.DialogResult.OK)
    {
        return;
    }
      if (!dlg.Color.IsByAci)
    {
        if (dlg.Color.IsByLayer)
        {
            //by layer
            ed.WriteMessage("By Layer\n");
        }
        else if (dlg.Color.IsByBlock)
        {
            //by block
            ed.WriteMessage("By block\n");
        }
        else
        {
            ed.WriteMessage(dlg.Color.Red.ToString()
                + "--" + dlg.Color.Green.ToString() +
                            "--" + dlg.Color.Blue.ToString() + "\n");
        }
    }
    else
    {
        short colIndex = dlg.Color.ColorIndex;
        System.Byte byt = System.Convert.ToByte(colIndex);
          int rgb = Autodesk.AutoCAD.Colors.EntityColor.LookUpRgb(byt);
        long b = (rgb & 0xffL);
        long g = (rgb & 0xff00L) >> 8;
        long r = rgb >> 16; ;
          ed.WriteMessage(r.ToString() + "--" +
                          g.ToString() + "--" + b.ToString() + "\n");
    }
  }

## 评论

**内容**: Tony Tanzillo said...
short colIndex = dlg.Color.ColorIndex;
System.Byte byt = System.Convert.ToByte(colIndex);

int rgb = Autodesk.AutoCAD.Colors.EntityColor.LookUpRgb(byt);
long b = (rgb & 0xffL);
long g = (rgb & 0xff00L) >> 8;
long r = rgb >> 16; ;

ed.WriteMessage(r.ToString() + "--" +
g.ToString() + "--" + b.ToString() + "\n");

Perhaps you might want to have a look at the Autodesk.AutoCAD.Colors.Color class, and it's EntityColor property, which returns an EntityColor whose Red/Green/Blue properties hold the R/G/B values for the color.
Reply
09/25/2012 at 02:59 PM

---
**内容**: Greg said...
This will disable the True Color and Color Book tabs and disable ByLayer and ByBlock
dlg.SetColorTabls(Autodesk.AutoCAD.Windows.ColorDialog.ColorTabs.ACITab);
dlg.IncludeByBlockByLayer = False;
Reply
08/04/2016 at 01:26 PM

---
