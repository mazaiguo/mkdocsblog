---
title: "Configuring 3D Graphics System in AutoCAD OEM"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - OEM
description: "How do I configure the 3D Graphics System in AutoCAD OEM?"
author: Autodesk
---
# Configuring 3D Graphics System in AutoCAD OEM

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/configuring-3d-graphics-system-in-autocad-oem.html

## 文章内容

By Fenton Webb
Issue
How do I configure the 3D Graphics System in AutoCAD OEM?
Solution
In AutoCAD we can configure 3D Graphics System by using the Current 3D Graphics Display sub-option, which is found on Options Dialog.
However, AutoCAD OEM does not support the Current 3D Graphics Display sub-option, which is found on Options Dialog, System tab for standard AutoCAD. This functionality is available to you, the developer, however.
There are two ways to handle setting the values that are available on the 3D Graphics System Configuration dialog under the Properties button.
You can enable the "3DConfig" command to gain direct access to the 3D Configuration screens for the graphics.
Alternately you can change the parameters in the registry to set certain configuration options by setting the following flags. These are found in the registry for your product under:
  HKEY_CURRENT_USER\Software\<company name>\<stamped oem appname>\<Your version>\<prod-key>\3DGS Configuration\GSHEIDI10
These values should be set before your product’s OEM engine initializes. If the values required are fixed for the requirements of you applications you could set these during install one time. Or if you only need a couple to be configurable, you could provide your own UI and set them as necessary, however, note that the OEM engine will need to be restarted in order for them to take affect.
Flags =  0x00240000 - This the default, no options set value.
Add the following flags to enable specific options:
0x00004000 = Render Option checked no others
0x00008000 = Lights
0x00000010 = Materials
0x00020000 = Textures (High quality/Slower)
0x00040000 = Textures (Medium Quality)
0x00080000 = Textures (Low quality/Faster)
0x00002000 = Adaptive Degradation checked no others
0x00000001 = Flat Shaded
0x00000002 = Wireframe
0x00000004 = Bounding Box
0x00000040 = Iso Lines on top
0x00000008 = Discard Back Faces
0x00000200 = Dynamic tessellations
Surface Tessellation = SurfaceTessellationTol value = 0 – 0x64 (0 – 100 decimal)
Curve Tessellation = CurveTessellationTol value = 0 – 0x64 (0 – 100 decimal)
Number of Tessellations to Cache = MaxTessellations
Maintain Speed at n FPS = FramesPerSecond
Some examples:
0x00244000 = Render Option checked no others
0x0024c000 = Render Option + Lights
0x0024c010 = Render Option + Lights + Materials
0x00244010 = Render Option + Materials
0x0026c010 = Render Option + Lights + Materials + Textures (High quality/Slower)
0x002ac010 = Render Option + Lights + Materials + Textures (Medium quality)
0x0032c010 = Render Option + Lights + Materials + Textures (Low quality/Faster)
0x0032e010 = Adaptive Degradation + above
0x00242000 = Adaptive Degradation checked no others
0x00246000 = Adaptive Degradation + Render Option
0x00242001 = Adaptive Degradation + Flat Shaded
0x00242003 = Adaptive Degradation + Flat Shaded + Wire Frame
0x00242007 = Adaptive Degradation + Flat Shaded + Wire Frame + Bounding Box
0x00242040 = IsoLines on top
0x00242008 = Discard Back Faces
0x00242048 = IsoLines on top + Discard Back faces
0x00240200 = Dynamic tessellations

