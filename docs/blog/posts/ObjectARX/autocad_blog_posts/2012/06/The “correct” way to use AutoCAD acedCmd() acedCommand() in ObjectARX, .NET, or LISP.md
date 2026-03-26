---
title: "The “correct” way to use AutoCAD acedCmd() acedCommand() in ObjectARX, .NET, or LISP"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - AutoLISP
  - C++
  - ObjectARX
description: "I wanted to write an tell you how you should format the command strings and keywords that you pass to these functions,"
author: Autodesk
---
# The “correct” way to use AutoCAD acedCmd() acedCommand() in ObjectARX, .NET, or LISP

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/the-correct-way-to-use-autocad-acedcmd-acedcommand-in-objectarx-net-or-lisp.html

## 文章内容

by Fenton Webb
By now, if you have been following my posts, will have probably realized that I really do like acedCmd and acedCommand (command in LISP).
I wanted to write an tell you how you should format the command strings and keywords that you pass to these functions,
Firstly, let’s talk about the Command strings themselves. AutoCAD comes in many languages, and the Command strings are actually translated for each language. This means that we can never assume the English LINE command will be called the same in the Russian version, for instance. As a programmer, one that uses acedCmd or acedCommand, we don’t really want to worry ourselves about localized Command strings. Thankfully, we can always access the English (non-localized version of any Command string by using the underscore symbol… e.g.
_LINE
Another issue that programmers like us don’t want to worry ourselves with when using acedCmd or acedCommand is whether or not the user has REDEFINE’d one of the Commands that we want to use… If they have, they could cause our lovely program to fail because they have changed the way the command we are using works – costing us support calls!! Thankfully, we can always access the raw Command using …. e.g.
.LINE
You can combine both of these tricks together… e.g.
_.LINE
in roundup, the “correct” way to specify Command Strings using acedCmd and acedCommand is: prefix all Commands with _.
Finally, let’s talk about the keyword strings that you pass to acedCmd or acedCommand. Again, these are localized, again we don’t want to worry about running into keywords that are different on different localized versions of AutoCAD, so we can use the underscore technique... (note you cannot REDEFINE keywords, so there is no dot required)… e.g.
_Startpoint
You’ll notice that I have specified the whole keyword string, not just _S. Why I recommend that you do this is is purely from experience…
1) Commands can change in the future, if you specify _S then later on, we introduce a new keyword called _Separate, then your code is broken. Always use the full keyword, it will save you time and effort in the future.
2) It’s easier to read in your code… You’ll be glad of this years down the line when you are trying to remember what the command is doing.

## 评论

**内容**: Eric Allain said...
I have a french version of AutoCad (2012) with french commands.
Company lisps are with englich commands.....
Is there a simple way allow english commands in the french version without having to reprogramme every lisp?
Reply
08/20/2012 at 11:54 AM

---
**内容**: Tony Tanzillo said in reply to Eric Allain...
As far as I know, All AutoCAD versions recognize English commands, if they are prefixed with an underscore as in "_MOVE", "_COPY", etc.
Reply
03/24/2013 at 10:55 PM

---
**内容**: Madhukar Moogala said in reply to Eric Allain...
Tony is correct. If you're writing any code that you expect to be used in more than one language version of AutoCAD, then you should use the 'global' command names and keywords - which are the English commands prefixed with an underscore. If you find a command where that is not the case, then please report it to us as a bug.
Reply
03/26/2013 at 04:50 PM

---
