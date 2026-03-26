---
title: "Identifying the user who has opened the drawing file"
date: 2012-09-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - DWG
description: "You can use API “Autodesk.AutoCAD.ApplicationServices. Application.GetWhoHasInfo” API to identify the user who has opened the specified drawing fil..."
author: Autodesk
---
# Identifying the user who has opened the drawing file

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/identifying-the-user-who-has-opened-the-drawing-file.html

## 文章内容

By Virupaksha Aithal
You can use API “Autodesk.AutoCAD.ApplicationServices. Application.GetWhoHasInfo” API to identify the user who has opened the specified drawing file. The WhoHasInfo object returned contains the same information that is displayed by the WHOHAS command.
[CommandMethod("WhoHasInfoTest")]
public static void WhoHasInfoTest()
{
    WhoHasInfo info = Application.GetWhoHasInfo("c:\\dwg\\test.dwg");
      Document doc = Application.DocumentManager.MdiActiveDocument;
    Editor ed = doc.Editor;
      if (info.IsFileLocked)
    {
        ed.WriteMessage(info.ComputerName + " "
                                            + info.UserName + "\n");
    }
    else
    {
        ed.WriteMessage("File is not locked for edit\n");
    }
  }

## 评论

**内容**: This comment has been deleted.
09/04/2012 at 08:45 AM

---
**内容**: Andrey said...
Hi Virupaksha.
It's interesting information.
Thank you.
Reply
09/04/2012 at 11:04 AM

---
**内容**: James Maeding said...
this is the info in the dwl file right?
I'd prefer to have a non-adesk based routine, similar to ours that gets dwg version by reading first 6 chars of the dwg in ascii. still a good tip though.
Reply
09/04/2012 at 01:21 PM

---
**内容**: Andrey said in reply to James Maeding...
Oh, yes. Thank you James!
DWL and DWL2 are contains the equal information, but in different formats. DWL - usual text and DWL2 - XML text.
I never tried to open such files before. :)
Reply
09/04/2012 at 06:42 PM

---
**内容**: Madhukar Moogala said...
Andrey and Owen - Yes this was spam comment. I had to delete your comments to remove it.
Owen - Not sure why you say we're 'letting' this spammer post comments. I'm flagging each one as spam when it comes in, but the spammers keep creating new accounts. Not sure what else I can do other than flag them as spam. (Maybe its better to say TypePad are 'letting' them keep posting). Maybe you know a better way - do tell :-)
Reply
09/04/2012 at 05:29 PM

---
**内容**: Owen Wengerd said in reply to Madhukar Moogala...
This one is always the same name and same URL, which should be easy to block. I'm not familiar with the TypePad platform, but on Wordpress I can block specific comments or commenters by adding keywords to a comment blacklist.
Reply
09/04/2012 at 07:09 PM

---
**内容**: Madhukar Moogala said in reply to Owen Wengerd...
What can I say - I mark as spam, they keep coming back, I mark as spam ...
:-(
Reply
09/04/2012 at 07:11 PM

---
**内容**: Owen Wengerd said in reply to Madhukar Moogala...
They are persistent buggers. Irritating, too. :-\
Reply
09/04/2012 at 07:17 PM

---
