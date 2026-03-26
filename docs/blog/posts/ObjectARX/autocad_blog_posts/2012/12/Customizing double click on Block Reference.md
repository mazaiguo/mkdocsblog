---
title: "Customizing double click on Block Reference"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Block
  - CUI
  - Selection
description: "This topic came up recently in the discussion forum. The developer wanted to display a custom form on double clicking of block reference that were ..."
author: Autodesk
---
# Customizing double click on Block Reference

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/customizing-double-click-on-block-reference.html

## 文章内容

By Balaji Ramamoorthy
This topic came up recently in the discussion forum. The developer wanted to display a custom form on double clicking of block reference that were created by his application but let AutoCAD perform the usual block editing for other block references.
Here is a sample code that modifies the macro for the block double click using the CUI API and makes it invoke a custom command called "mybedit". From the "mybedit" custom command, we can check if the block reference is the one that we are interested in. If yes, we do our custom action such as showing our custom form. If not, we set the pick first selection and then invoke the AutoCAD "bedit".
// Requires reference to AcCui.dll
using Autodesk.AutoCAD.Customization;
  [CommandMethod("ChangeMacroCUI")]
static public void ChangeMacroCUI()
{
    Document activeDoc
            = Application.DocumentManager.MdiActiveDocument;
    Editor ed = activeDoc.Editor;
      // Retrieve the location of, and open the ACAD Main CUI File
    string mainCuiFile =
            (string)Application.GetSystemVariable("MENUNAME");
    mainCuiFile += ".cuix";
    CustomizationSection cs = new CustomizationSection(mainCuiFile);
      DoubleClickAction blockDoubleClickAction = null;
    foreach (DoubleClickAction dca in
                                cs.MenuGroup.DoubleClickActions)
    {
        if (dca.Name.Equals("Block"))
        {
            blockDoubleClickAction = dca;
            break;
        }
    }
      if (blockDoubleClickAction != null)
    {
        // Change the double click macro to call our command
        blockDoubleClickAction.DoubleClickCmd.MenuMacroReference.macro.Command
            = "$M=$(if,$(and,$(>,$(getvar,blockeditlock),0)),^C^C_properties,^C^C_MyBEdit)";
          // Save our changes
        if (cs.IsModified)
            cs.Save();
    }
}
  [CommandMethod("MyBEdit", CommandFlags.UsePickSet)]
static public void MyBeditCommand()
{
    Document activeDoc
        = Application.DocumentManager.MdiActiveDocument;
    Editor ed = activeDoc.Editor;
      String RegAppName = "MyApp";
      PromptSelectionResult result = ed.GetSelection();
      if (result.Status == PromptStatus.OK)
    {
        SelectionSet ss = result.Value;
        foreach (SelectedObject so in ss)
        {
            bool isMyBlockRef = false;
              Database db = activeDoc.Database;
            using (Transaction tr
                    = db.TransactionManager.StartTransaction())
            {
                Entity ent
                    = tr.GetObject(
                                    so.ObjectId,
                                    OpenMode.ForRead
                                  ) as Entity;
                  // Lets check for XData to identify if we need
                // to show our dialog
                if (ent.GetXDataForApplication(RegAppName) != null)
                {
                    isMyBlockRef = true;
                }
                tr.Commit();
            }
              if(isMyBlockRef)
            {
                // Custom action such as showing our form.
                // Just as a demo we use the alert dialog
                Application.ShowAlertDialog
                    ("Custom action such as showing our form.");
            }
            else
            {
                // Let AutoCAD do the block edit.
                  ObjectId[] ids = ss.GetObjectIds();
                  // Set the implied selection to what it was
                // before our command was called
                ed.SetImpliedSelection(ids);
                  // call "bedit" command
                activeDoc.SendStringToExecute
                                (
                                    "_BEDIT ",
                                    false,
                                    false,
                                    false
                                );
            }
        }
    }
}

## 评论

**内容**: Ben said...
This code doesn't seem to work - it doesn't seem to saving the customisationSection object.
any ideas?
Reply
10/23/2017 at 11:06 PM

---
**内容**: BKSpurgeon said...
Here is a refactored version of the above, hopefully it will be easier to read:
https://gist.github.com/BKSpurgeon/d5c7edd4a0454fc09549217e098a8b61
I hope it helps someone.
Reply
01/28/2018 at 04:59 PM

---
**内容**: wsp said...
hi!
There is a bug,after call "_bedit" command,the block name is not selected in the Pop-up Form.
Change to below:
var buffer = new ResultBuffer
{
new TypedValue(5005, "-bedit"),
new TypedValue(5005, blkName),
new TypedValue(5005, "")
};
acedCmd(buffer.UnmanagedObject);
Reply
09/15/2018 at 07:38 PM

---
