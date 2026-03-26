---
title: "Taking mouse inputs from a modal dialog box"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
description: "You need to use “EditorUserInteraction” class to take mouse inputs from AutoCAD while showing a modal dialog box. “EditorUserInteraction” takes car..."
author: Autodesk
---
# Taking mouse inputs from a modal dialog box

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/taking-mouse-inputs-from-a-modal-dialog-box.html

## 文章内容

By Virupaksha Aithal
You need to use “EditorUserInteraction” class to take mouse inputs from AutoCAD while showing a modal dialog box. “EditorUserInteraction” takes care of hiding and showing of the modal dialog box. Use editor API “StartUserInteraction” to create the instance of “EditorUserInteraction” class as shown in below code.
The code shown below is of a button click callback inside a dialog box.  Dialog box is currently displaying in AutoCAD as modal dialog.
//a button click call back event...
private void getEntity_Click(object sender, EventArgs e)
{
    Document doc = Autodesk.AutoCAD.ApplicationServices.
                Application.DocumentManager.MdiActiveDocument;
    Editor ed = doc.Editor;
    Database db = doc.Database;
      //this - is the modal dialog box.
    using (EditorUserInteraction UI =
                                ed.StartUserInteraction(this))
    {
        PromptEntityResult entResult =
                                ed.GetEntity("\nSelect entity");
          if (entResult.Status != PromptStatus.OK)
            return;
          using (Transaction Tx =
                  db.TransactionManager.StartTransaction())
        {
            DBObject obj = Tx.GetObject(entResult.ObjectId,
                                              OpenMode.ForRead);
            ed.WriteMessage(obj.GetType().Name);
              Tx.Commit();
        }
    }
}

## 评论

**内容**: Juan said...
How convert the modal dialog "this" to System.IntPtr for use with editor staruserinteraction.
I'm trying with "Me", the error is:
Value of type 'App-namespace.Dialog1'cannot be converted to 'System.IntPtr'.
Using forms instead of dialogues generates the same error.
Reply
04/03/2014 at 10:02 AM

---
**内容**: HG said...
Hello,
I am very new to ObjectArx and trying to learn by example.
Could you possibly explain how can I make a modal dialog disappear (as in the example above), then click in the desired location in the Editor (which may or may not contain an entity) and return the clicked coordinates back to my C# app. I intend to use it to simplify entering the coordinates into the external database by snapping to points chosen by the user.
Thanks!
Reply
05/27/2014 at 03:23 AM

---
**内容**: Virupaksha Aithal said in reply to HG...
Hi,
You need to use editor function GetPoint instead of GetEntity(). But as you said you are new to programming, I will suggest you to go through the AutoCAD.NET training material in our Devblog. Please go through lesson 1 to lesson 8 http://adndevblog.typepad.com/autocad/2012/10/autocadnet-lesson-8-user-interface-elements.html .
Thanks
Viru
Reply
05/27/2014 at 03:32 AM

---
**内容**: Neyton Luiz Dalle Molle said...
Hello, I'm having problem with ED.StartUserInteraction.
When WindowsForm (modal form) is maximized and I click the button that requires data on the command line, the WindowsForms closes unexpectedly.
I tried to work around the problem with the event below, but it still fails:
Private Sub me_FormClosing (sd As Object, evt The FormClosingEventArgs) Handles Me.FormClosing
If evt.CloseReason = CloseReason.None Then
MsgBox ("FormClosing User Intercation Error ...")
evt.Cancel = True 'try to cancel "close"
end If
end Sub
Reply
06/29/2016 at 07:49 AM

---
