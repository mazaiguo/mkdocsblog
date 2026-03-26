---
title: "About AUTOSAVE and notifications/events"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "When AutoCAD does an AUTOSAVE, it saves the drawing at the OS Temp folder with the name "DrawingNameNumbers.sv$", as specified on the OPTIONS dialo..."
author: Autodesk
---
# About AUTOSAVE and notifications/events

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/about-autosave-and-notificationsevents.html

## 文章内容

By Augusto Goncalves
When AutoCAD does an AUTOSAVE, it saves the drawing at the OS Temp folder with the name "DrawingName_Numbers.sv$", as specified on the OPTIONS dialog, and it sends a kSaveMsg message to all applications.
However, this kSaveMsg message may trigger some custom action on applications that are listening to this notification/event, but in the case of an AUTOSAVE, this is not the correct thing to do.
Because an AUTOSAVE does not trigger a CommandWillStart() notification, if we set a global flag from the CommandWillStart() notification tracking commands with “SAVE” on the command name, then we can detect if is an AUTOSAVE or a normal save called by the user.

## 评论

**内容**: Tony Tanzillo said...
Hi.
What if someone calls AcDbDatabase::saveAs() or the AcadDocument.Save()/SaveAs() methods in ActiveX ?
I think this may not be a good way to detect if a save is an Autosave or not.
Is there something wrong with just examining the file extension?
Reply
09/07/2012 at 08:38 AM

---
**内容**: Augusto Goncalves said in reply to Tony Tanzillo...
Hi Tony,
The file extension can be renamed, so a user can change it to .DWG and then cause this examination to fail. Yes if the call to save the drawing come from an API call, then will not work either, but at least this type of call is under your control.
Thanks for the comment.
Regards,
Augusto Goncalves
Reply
09/10/2012 at 06:39 AM

---
**内容**: Stuart Elvers said...
Autgusto,
Sorry for dredging up older post's. We have tapped into the DocumentManager.DocumentLockModeChanged event to see various things and prevent commands from running during certain times in our application.
The DocumentLockModeChangedEventArgs parameter has a .GlobalCommandName property that shows us when "AUTO_SAVE" is being called during one of our routines. This is easy to prevent as there is also a Veto() function to cancel the "AUTO_SAVE". We also set a flag when the "AUTO_SAVE" has been Veto()'d so we can trigger a QSAVE as soon as our command has completed.
My question is, using .Net, is there an way to trigger a call to "AUTO_SAVE" directly. QSAVE does not seem to be the same thing and takes longer in some cases. Is there something we can maybe dll import from arx? I have tried the typical ways to call "AUTO_SAVE" as a command and it is not recognized as a command. Again the GlobalCommandName property shows its name is "AUTO_SAVE" but I believe that is just a false name that does not correlate to an actual registered command name.
Thank you,
Stuart Elvers
Reply
07/30/2013 at 06:38 AM

---
**内容**: Augusto Goncalves said in reply to Stuart Elvers...
Stuart,
Sorry I didn't receive a notification about this...
Indeed AutoCAD has several "internal" commands that appear only during DockLock event (and some other events), and we cannot invoke most of them.
Regards,
Augusto Goncalves
Reply
07/30/2015 at 04:38 AM

---
**内容**: alvior said...
Hi,
Sorry to bother you, I want to ask a question.
How can I have a fixed time of AUTOSAVE and users can not change it by themselves?
Thanks
Reply
07/30/2015 at 02:20 AM

---
**内容**: Augusto Goncalves said in reply to alvior...
Alvior,
You can track if this sysvar change (by the user), if so, change back to the original value. As this is a setting (under OPTIONS), you cannot avoid it being changed, but you can change it back.
Regards,
Augusto Goncalves
Reply
07/30/2015 at 04:36 AM

---
**内容**: joantopo said...
So, what is finally the best way to catch the AUTO_SAVE "event"?
As Stuart Elvers said and I have tried it, CommandWillStart event doesn´t work with e.GlobalCommandName="AUTO_SAVE"
I would prefer not to use DockLock event because there is a huge amount of scenarios when that event is fired.
Thanks.
Reply
08/19/2016 at 06:09 PM

---
