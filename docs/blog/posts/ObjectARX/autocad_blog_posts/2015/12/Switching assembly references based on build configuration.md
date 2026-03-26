---
title: "Switching assembly references based on build configuration"
date: 2015-12-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - COM Interop
  - Plugin
  - Unicode
description: "Recently, a developer came up with this query :"
author: Autodesk
---
# Switching assembly references based on build configuration

发布日期: 2015-12-01

原始链接: https://adndevblog.typepad.com/autocad/2015/12/switching-assembly-references-based-on-build-configuration.html

## 文章内容

By Balaji Ramamoorthy
Recently, a developer came up with this query :
Is there a simple way to have a single copy of my code configured to compile to different folders with different references based on the desired version of AutoCAD to be run ?
This is not strictly an AutoCAD API related query but it is very relevant to how we build plugins for AutoCAD. It is a common requirement that we add references from different paths based on the AutoCAD version for which we are building the plugin.
A simple way to get this working is to create separate build configurations in your Visual Studio solution.
Now, open the .csproj in a text editor and manually include the "Condition" for each of the references.
As an example, here is the change to include different versions of the interop assembly for Sheetset manager for each build configuration.
<Reference Include="Interop.ACSMCOMPONENTS20Lib" Condition="'$(Configuration)'=='Debug2015'">
<HintPath>..\..\..\..\ObjectARX 2015\inc-x64\ACSMCOMPONENTS20Lib.dll</HintPath>
<EmbedInteropTypes>True</EmbedInteropTypes>
</Reference>
<Reference Include="Interop.ACSMCOMPONENTS20Lib" Condition="'$(Configuration)'=='Debug2016'">
<HintPath>..\..\..\..\ObjectARX 2016\inc-x64\ACSMCOMPONENTS20Lib.dll</HintPath>
<EmbedInteropTypes>True</EmbedInteropTypes>
</Reference>
If you are using any other technique to achieve this already, please do share by posting your comments. I am sure that will help many other developers. Thank you.

## 评论

**内容**: CAD bloke said...
This has been discussed a lot at The Swamp. See http://www.theswamp.org/index.php?topic=50202.0 and have a look at the other threads linked in the first post for a variety of approaches.
I wrote Code Linker (it's on that Swamp link) because the housekeeping got too unwieldy with a lot of build configurations and phantom project references (see http://www.theswamp.org/index.php?topic=49039.msg541744#msg541744) but I think different approaches will work for different people in different situations.
Reply
12/18/2015 at 01:18 AM

---
**内容**: Balaji said...

Thanks for sharing the Code Linker and that detailed discussion.
There is a treasure of information in that post.
Regards,
Balaji
Reply
12/18/2015 at 02:11 AM

---
