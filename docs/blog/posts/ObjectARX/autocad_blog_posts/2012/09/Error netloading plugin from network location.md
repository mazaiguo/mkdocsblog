---
title: "Error netloading plugin from network location"
date: 2012-09-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Plugin
description: "Iam trying to netload a plugin from a network location. But it gives me an error indicating "Please enable the loadFromRemoteSources" switch. How d..."
author: Autodesk
---
# Error netloading plugin from network location

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/error-netloading-plugin-from-network-location.html

## 文章内容

By Balaji Ramamoorthy
Issue
Iam trying to netload a plugin from a network location. But it gives me an error indicating "Please enable the loadFromRemoteSources" switch. How do I resolve this ?
Solution
This message is due to a change related to administering CAS policy in the .Net Framework 4.0 as compared to .Net Framework 3.5.
More information on this is available in the following links :
http://blogs.msdn.com/b/shawnfa/archive/2009/06/08/more-implicit-uses-of-cas-policy-loadfromremotesources.aspx
http://msdn.microsoft.com/en-us/library/dd409252(VS.100).aspx
To fix this problem, you can modify the "acad.exe.config" by inserting the following line in it.
The "acad.exe.config" can be found in the AutoCAD installation folder.
<runtime>
<loadFromRemoteSources enabled="true"/>
</runtime>
The <loadFromRemoteSources> element lets you specify that the assemblies that run partially trusted in earlier versions of the .NET Framework should be run fully trusted in the .NET Framework 4.

## 评论

**内容**: Parisa said...
I used it but didn't work :(
Reply
01/03/2013 at 07:12 AM

---
**内容**: neyton luiz dalle molle said...
Need to restart autocad after changes
Reply
06/20/2014 at 11:27 AM

---
