---
title: "Autoloader and the registry"
date: 2012-09-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Plugin
description: "An Exchange store publisher emailed us today after he’d been surprised by some ‘as designed’ Autoloader behavior, so I’m publicizing it here to pre..."
author: Autodesk
---
# Autoloader and the registry

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/autoloader-and-the-registry.html

## 文章内容

By Stephen Preston
An Exchange store publisher emailed us today after he’d been surprised by some ‘as designed’ Autoloader behavior, so I’m publicizing it here to prevent others having the same surprise.
When Autoloader detects a new bundle, it adds the demand load settings inferred from the PackageContents.xml file to the registry. After your bundle has loaded, your registry will look something like this:
Which is the same as you’d expect if you’d added the entries via your custom installer or through some setup code that is invoked when your app first runs.
However, the demand load entries added by Autoloader are deleted when AutoCAD exits.
This means that you shouldn’t use your plug-in’s demand load registry entries to store additional data if you’re using Autoloader. Store it somewhere else in the registry instead (if you must use the registry), or in a config file. You can find the registry location for your running AutoCAD instance with the HostApplicationServices.UserRegistryProductRootKey and UserRegistryProductRootKey properties.
As an aside, there are some settings persisted by Autoloader so it knows not to show a balloon notification for a plug-in every time AutoCAD starts:
The GUIDs shown in the screenshot come from the ProductCode parameter in PackageContents.xml.

## 评论

**内容**: Andrey Bushman (@AndreyBushman) said...
Hi Stephen.
You specified the wrong properties. Correct properties such:
- HostApplicationServices.Current.MachineRegistryProductRootKey
- HostApplicationServices.Current.UserRegistryProductRootKey
Regards
Reply
09/13/2012 at 09:51 PM

---
**内容**: Madhukar Moogala said in reply to Andrey Bushman (@AndreyBushman)...
Hi Andrey. Thanks for pointing that out. These are properties of the HostApplicationServices class, but you're right that they are accessed in an AutoCAD plug-in via the HostApplicationServices.Current property (which returns the current HostApplicationServices instance being used).
Reply
09/14/2012 at 07:51 AM

---
**内容**: Vladimir Michl said...
Thanks Stephen, lesson learned. This one was hard to debug.
Reply
09/13/2012 at 10:46 PM

---
**内容**: Madhukar Moogala said in reply to Vladimir Michl...
Thanks for reporting it Vladimir. And sorry for the time you spent debugging because of it :(.
Reply
09/14/2012 at 07:52 AM

---
