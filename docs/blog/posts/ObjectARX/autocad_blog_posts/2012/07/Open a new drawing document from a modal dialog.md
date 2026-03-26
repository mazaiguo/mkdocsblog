---
title: "Open a new drawing document from a modal dialog"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "I use a modal dialog to enable the user to select a template for a new drawing and then I try to open it in the OnOkClicked message. It does not ma..."
author: Autodesk
---
# Open a new drawing document from a modal dialog

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/open-a-new-drawing-document-from-a-modal-dialog.html

## 文章内容

By Adam Nagy
I use a modal dialog to enable the user to select a template for a new drawing and then I try to open it in the OnOkClicked message. It does not matter if I call Form.ShowDialog() or Application.ShowModalDialog() (ShowModalWindow() for WPF windows), DocumentManager.Add() does not succeed.
[CommandMethod("ShowMyDialog")]
public void ShowMyDialog()
{
  MyForm mf = new MyForm();
  Application.ShowModalDialog(mf);
}
Calling DocumentManager.Add() from here
public partial class MyForm : Form
{
  // ...
    string docTemplatePath;
    private void OnOkClicked(object sender, EventArgs e)
  {
    Document doc =
      Application.DocumentManager.Add(docTemplatePath);
      this.Close();
  }
}
Solution
You cannot manipulate (create/remove/switch) documents from a modal dialog. This is as designed.
You could easily modify your code so that you create the new drawing once the dialog is closed.
Also, though DocumentManager.Add() may succeed from a command running in document context, we'd suggest that you do it from session context.
public partial class MyForm : Form
{
  // ...
    public string docTemplatePath;
    private void OnOkClicked(object sender, EventArgs e)
  {
    this.DialogResult = DialogResult.OK;
    this.Close();
  }
}
Showing the dialog and calling DocumentManager.Add() from here
[CommandMethod("ShowMyDialog", CommandFlags.Session)]
public void ShowMyDialog()
{
  MyForm mf = new MyForm();
  if (Application.ShowModalDialog(mf) ==
    System.Windows.Forms.DialogResult.OK)
  {
    Document doc =
      Application.DocumentManager.Add(mf.docTemplatePath);
  }
}

## 评论

**内容**: Account Deleted said...
Is it possible to open new drawing from a button in custom palette set?
Reply
07/14/2012 at 11:54 PM

---
**内容**: Adam Nagy said...
Hi Vyacheslav,
That is like opening a drawing from a modeless dialog, so that is OK.
One thing to also think about is placing the application logic inside a command instead of inside a modeless dialog/palette set's button click handler and then just calling the command from there using SendStringToExecute() - as mentioned above the command should be registered with the Session flag.
Cheers,
Adam
Reply
07/15/2012 at 06:34 AM

---
**内容**: Account Deleted said...
Hi, Adam.
I create custom palette with one button on which pressing I cause the following code
DocumentCollection dm = Platform.ApplicationServices.Application.DocumentManager;
acDoc = dm.Open(fName);
If I previously close all drawing and press this button I recieve AccessViolation inside CRT after opening this file.
Could you help me to anderstand this situation.
Cheers,
Vyacheslav
Reply
07/15/2012 at 10:51 PM

---
**内容**: Adam Nagy said...
Hi Vyacheslav,
I tried it in AutoCAD 2011 and it seemed to work fine. I wonder what is causing the difference on your system.
Maybe you could post a question about it on the forums with a small sample project that reproduces the issue?
Also providing the exact error message you get?
Someone might have run into the same behaviour and could comment on that there.
Cheers,
Adam
Reply
07/19/2012 at 03:19 AM

---
