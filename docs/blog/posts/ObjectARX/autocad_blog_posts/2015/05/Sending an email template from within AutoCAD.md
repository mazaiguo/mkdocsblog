---
title: "Sending an email template from within AutoCAD"
date: 2015-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - COM Interop
description: "Recently, I received a query from an ADN partner, as part of partner customisation requirement expects users to send feedback about publisher app."
author: Autodesk
---
# Sending an email template from within AutoCAD

发布日期: 2015-05-01

原始链接: https://adndevblog.typepad.com/autocad/2015/05/sending-an-email-template-from-within-autocad.html

## 文章内容

By Madhukar Moogala
Recently, I received a query from an ADN partner, as part of partner customisation requirement expects users to send feedback about publisher app.
The idea is to trigger outlook from a .NET command which is loaded in a macro button.
We can use  Microsoft.Office.Interop.Outlook API to achieve this in our command.
Sample code:
Use assemblyref  Microsoft.Office.Interop.Outlook
  [CommandMethod("SMTP")]
static public void SMTP()
{
try
{
List<string> lstAllRecipients = new List<string>();
//Below is hardcoded - can be replaced with db data
lstAllRecipients.Add("Helpdesk@Publisher.com");
Outlook.Application outlookApp =
    new Outlook.Application();
Outlook._MailItem oMailItem = 
    (Outlook._MailItem)outlookApp.CreateItem(Outlook.OlItemType.olMailItem);
Outlook.Inspector oInspector = oMailItem.GetInspector;
// Recipient
Outlook.Recipients oRecips =
(Outlook.Recipients)oMailItem.Recipients;
foreach (String recipient in lstAllRecipients)
{
Outlook.Recipient oRecip =
(Outlook.Recipient)oRecips.Add(recipient);
oRecip.Resolve();
}
  //Add Subject
oMailItem.Subject = "Test Mail";
// body
oMailItem.Body = " Write your Body ";
  //Display the mailbox
oMailItem.Display(true);
}
catch (SystemException objEx)
{
Application.ShowAlertDialog(objEx.ToString());
}
}
  In the CUI macro button, pass ^C^C_SMTP
      Reference:DisplayMailbox

## 评论

**内容**: Martin said...
Thank you very much for your help. The service you've provided has been excellent. 
Reply
07/06/2017 at 03:56 AM

---
