---
title: "Turn off the Automatic Save of dsd files when running the Publish command"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "I have developed an application for one of my clients that uses the PUBLISH command.  Every time I publish drawings I get error messages related to..."
author: Autodesk
---
# Turn off the Automatic Save of dsd files when running the Publish command

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/turn-off-the-automatic-save-of-dsd-files-when-running-the-publish-command.html

## 文章内容

By Wayne Brill
Issue
I have developed an application for one of my clients that uses the PUBLISH command.  Every time I publish drawings I get error messages related to DSD files. How can I stop AutoCAD from saving DSD files automatically?
Solution
There is a setting in Options that will display the dialog that will ask if you want to save the dsd file. To change this do the following: Run the Options command and go to the System Tab. Click the Hidden Messages setting button. There will be a Publish – Save Sheet List  checkbox.  Check it and click Ok all the way out of options.
When you publish you should be prompted to save the current list of sheets. Click “Always perform my current choice” and select No.

## 评论

**内容**: ron said...
Thanks for posting this, was driving me mad!
Reply
07/27/2014 at 05:56 PM

---
**内容**: James Salter said...
Awesome. I've been struggling with this ever since an update changed the setting. Thanks for sharing.
Reply
06/29/2015 at 01:31 PM

---
**内容**: Bruce said...
..excellent post indeed, this was driving me crazy as well. Thank you.
Reply
08/31/2017 at 06:57 PM

---
**内容**: bam@csdavidson.com said...
I accidentally said "yes" the first time it asked me if I wanted to save the .dsd file. Is there a way that I can reverse my decision?
Reply
11/30/2017 at 06:25 AM

---
**内容**: Michael Friedrichs said...
I'm having this issue as well, and the part above in your solution where it says... Save Sheet List checkbox. Check it and click Ok all the way out of options. I don't see that option in the hidden messages. Maybe I'm on the wrong tab. I'm on the system tab under General options is where my hidden message tab appears. Is that correct?
Reply
01/27/2022 at 08:37 AM

---
**内容**: Lily said...
Thank you veeeeeeeery much...TT
Reply
11/14/2022 at 08:44 PM

---
**内容**: Andrei said...
Thank youuu !!!!! for saving me.
Sometime autocad is so stupid.
You can get out of business someone by change one of these stupid system variables.
Reply
03/16/2023 at 08:10 AM

---
**内容**: Albert said...
Thank you!!!
Reply
11/20/2024 at 12:41 AM

---
