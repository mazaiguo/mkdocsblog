---
title: "AutoCAD 2014 and Security"
date: 2013-03-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
description: "Have you downloaded and installed AutoCAD 2014 yet? If you did, you will notice a new set of security features in AutoCAD that will not let you loa..."
author: Autodesk
---
# AutoCAD 2014 and Security

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/autocad-2014-and-security.html

## 文章内容

By Gopinath Taget
Have you downloaded and installed AutoCAD 2014 yet? If you did, you will notice a new set of security features in AutoCAD that will not let you load custom applications that are not in a secure, trusted path. This behavior is controlled with SECURELOAD and TRUSTEDPATHS settings.
The easiest and best way to deploy your apps is to install your applications as Application bundles as the bundle paths are automatically treated as trusted paths. Check out this Autodesk Autoloader white paper for detailed information on its technology.
If this is not an option for you, you could try digitally signing your application. For this you will need a digital certificate from a well know certificate authority. AutoCAD 2014 will load digitally signed applications even if they are not in a trusted path.
One note for .NET developers. Digitally signing your application is different from strong naming your applications. Here is a very informative FAQ on the differences.

## 评论

**内容**: BlackBox said...
Autodesk Employee: "When the question of SCR files first came up, we wanted to treat them like any other executable files. Our plan would be that all SCR files no matter where they are located (if not trusted) would trigger the alert. Wouldn’t that make more sense?"

BlackBox: "Loaded question.
Doesn’t that inherently apply to Autodesk’s own ScriptPro? Or is that too being modified to adhere to one’s own trusted path specification (rhetorically, if you like)?
I understand the logic behind introducing a mechanism to allow users to ’know’ when something is being loaded, but unfortunately there is no one-size fits all scenario... A lesser example might be LayerEval, LayerNotify, and LayerEvalCtrl System Variables.
Firstly, this assumes that all users know how to properly configure trusted paths, let alone a working Profile. Now introduce the complexity of customization(s), and you’re in for one heck of a game of Battleship.
If Autodesk implements such a protocol that all executable files (outside of trusted) fire a notification, then what about self-replicating code, or even code that generates other executable files? A very simple AutoLISP routine can create a VBScript file without even using Visual LISP’s ActiveX COM API... Does this mechanism ’track’ and ’notify’ of this behavior too? I doubt it.
Several popular routines, will also self-create temporary dependent files, such as DCL, etc. in order to not intrude on one’s enterprise setup, nor litter one’s project directories, are these too going to be monitored?
Now, one I really would like a solid answer on, is how about Autoloader... Are the two local ..\\ApplicationPlugins\\ folders monitored by this mechanism, or are they automagically safe because Autoloader uses them? Obviously AppAutoLoad System Variable allows for automatic loading of plug-ins OOTB, and can be changed, but I’d still be interested to know how behavior could / should be impacted.
Again, I am merely trying to point out that this mechanism, if implemented to a fire a notification for all non-trusted executable files, then users will simply disable the notification as is commonly done with the Layer* System Variables noted above (albeit, perhaps at the risk of inviting trouble later on, but they will disable it when it’s become annoying, and then it helps nobody).
Coming back full circle, to the statement about network locations being riskier than local... I stand by my earlier sentiment, that to suggest that the network (something setup by corporate IT / CAD Management / multiple qualified individuals, etc.) is somehow viewed as more unsafe than the local disk, where any user with an internet connection can download an Autoloader *.bundle from any blog, forum, etc. outside of Autodesk Exchange and simply drop it into ..\\ApplicationPlugins\\ is not well thought out."
Many thanks for your time, and consideration.
Cheers
Reply
03/28/2013 at 09:52 PM

---
**内容**: Kerry Brown said...
Gopinath,
What is the situation with ScriptPro support files ?
We use .SCR files that in some cases load specific .LSP files.
The pathing for the .scr and .lsp files depends on the project.

Reply
03/30/2013 at 06:25 PM

---
**内容**: CADBully said...
This whole security scheme makes no sense. if I've got malicious code on my server that just happens to have the same filename as my "trusted" code, I've got bigger problems than SECURELOAD and TRUSTEDPATHS can handle. Once again we get to see Autodesk misfire yet again...
Reply
07/17/2013 at 07:54 AM

---
**内容**: Davor said...
SECURELOAD... yeah, thanks Autodesk.
Some people would rather see them putting an effort into optimizing performance and fiksing blatant issues lingering around for a decade than worrying about 0.01% possibility of malicious code from third party vendors.
Reply
10/07/2013 at 06:09 AM

---
**内容**: what is a digital signature said...
A special thanks for this informative post. I definitely learned a few new things here.
Reply
04/26/2014 at 01:49 AM

---
