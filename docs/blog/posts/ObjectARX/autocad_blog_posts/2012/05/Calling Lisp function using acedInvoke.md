---
title: "Calling Lisp function using acedInvoke"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoLISP
description: "Calling a Lisp function using acedInvoke from your .Net code, can return RTERROR (5001). To overcome this, you simply need to implement your Lisp f..."
author: Autodesk
---
# Calling Lisp function using acedInvoke

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/calling-lisp-function-using-acedinvoke.html

## 文章内容

By Balaji Ramamoorthy
Calling a Lisp function using acedInvoke from your .Net code, can return RTERROR (5001). To overcome this, you simply need to implement your Lisp function as a command as shown here :
;(defun DoIt()
  ;Define the Lisp function as a command using c:
(defun c:DoIt()
      (setq    pntA (getpoint "\nPick A")
            pntB (getpoint pntA "\nPick B")
    )
    (grdraw pntA pntB 1 2)
  )

## 评论

**内容**: BJHuffine said...
Just curious if you could show an actual example of acedInvoke being used with .NET. How do you declare it? Does it work like acedCmd with a Resbuf argument? What's it's signature and overloads?
Reply
12/29/2014 at 01:57 PM

---
**内容**: Balaji said in reply to BJHuffine...
Sorry, I missed your post.
Here is a sample code snippet.
[CommandMethod("DoIt", CommandFlags.Session)]
public void DoItMethod()
{
DocumentCollection acDocMgr = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager;
Document acDoc = acDocMgr.Open(@"C:\SampleDrawings\Lights.dwg", false);
using (DocumentLock dl = acDoc.LockDocument())
{
Editor ed = acDoc.Editor;
using (ResultBuffer rb = new ResultBuffer())
{
rb.Add(new TypedValue((int)LispDataType.Text, "c:DoIt"));
ResultBuffer rbRes = Application.Invoke(rb);
if (rbRes != null)
{
TypedValue[] tvalues = rbRes.AsArray();
foreach (TypedValue tv in tvalues)
ed.WriteMessage("\n" + tv.ToString());
rbRes.Dispose();
}
else
ed.WriteMessage("\n Result buffer is null.");
}
}
}
Regards,
Balaji
Reply
01/05/2015 at 09:41 PM

---
**内容**: Alexander Rivlis said...
https://sites.google.com/site/acadhowtodo/net/command-line/run-lisp-functions
Reply
01/05/2015 at 02:06 PM

---
**内容**: Balaji said in reply to Alexander Rivlis...
Thanks Alex
Reply
01/05/2015 at 09:41 PM

---
