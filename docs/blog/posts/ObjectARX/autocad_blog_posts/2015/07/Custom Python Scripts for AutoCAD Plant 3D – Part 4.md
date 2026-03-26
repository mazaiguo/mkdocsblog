---
title: "Custom Python Scripts for AutoCAD Plant 3D – Part 4"
date: 2015-07-01
categories:
  - Plant 3D
tags:
  - AutoCAD
  - Plant 3D
  - Python
description: "Get start with Part 1, Part 2 and Part 3 of this series."
author: Autodesk
---
# Custom Python Scripts for AutoCAD Plant 3D – Part 4

发布日期: 2015-07-01

原始链接: https://adndevblog.typepad.com/autocad/2015/07/custom-python-scripts-for-autocad-plant-3d-part-4.html

## 文章内容

By David Wolfe (Contributor)
Get start with Part 1, Part 2 and Part 3 of this series.
Packaging and Deploying Custom Scripts
This article will demonstrate how to package and deploy your custom scripts. This process will follow these steps:
Create images
Build a catalog
Build an installer (or zip)
In addition, your users will have to follow some installation steps.
Extract to content folder (C:\AutoCAD Plant 3D 2016 Content\CPak Common\CustomScripts)
Creating Images
In order for users to have a relatively seamless experience, you should provide images that match the existing scripts as closely as possible.  Along with using similar parameter names, good images can boost the user experience by making the images blend with the OOTB content.
You should create 4 images:
32x32
64x64
240x240
640x 640 (Dimensions)
By default your AutoCAD environment may look like this:
If it does, you should turn UCSICON off, and then use F7 to turn the grid off.
Use the PLANTSNAPSHOT command to create images at 32,64, 200 px square.  Unfortunately, these images won’t exactly match the OOTB content, as the graphic engine has changed. Your images will be stored in the CustomScripts folder, and should have a file name that matches the script file name with the size appended. Shown below is our script (EXPJOINT1.py) with matching image files EXPJOINT1_32.png, EXPJOINT1_64.png, EXPJOINT1_200.png.
The program will automatically load them and use them as appropriate.
In order to provide dimension feedback, you also need to provide a 640x640 image. You can use a program like Jing, or SnagIt to create a screen clipping that is the correct dimensions.
To setup the dimension image, you’ll need to set your viewport to Hidden, create the dimensions, and override their text values and size.
You should turn your background white, by modifying your AutoCAD options.
Once the images are in place and you have run PLANTREGISTERCUSTOMSCRIPTS on your most recent version, you are ready to package the files.
Deploying the Scripts
Once you have everything ready, you can build your installer. One full-featured free installer is Inno Setup. When building your installer, you should handle the following:
Multiple versions of Plant
Custom Content Paths
Previously loaded content
Multiple versions of Plant
The api for creating scripts hasn’t changed significantly since Plant was first released. Technically, you could deploy scripts for all version 2011 and higher.  However, Autodesk maintains support for the last 3 releases, so that may be a factor for your consideration as well.
Custom Content Paths
While C:\AutoCAD Plant 3D 2016 Content is the default content location, some users may have custom paths set. You can find these paths by checking the registry key for its default value.
HKEY_LOCAL_MACHINE\SOFTWARE\Autodesk\AutoCAD\R20.1\ACAD-F017\Variables\PLANTCONTENTFOLDER
The value R20.1 here is for 2016, and F017 is for Plant. See this page for more information on version identifiers.
You will need to check this registry value for any version of Plant that you want to install your scripts for.
Previous Content
Most users do not use CustomScripts, so unless they do, you will be able to put files at the CustomScripts folder location without worry. However, if a user does have custom scripts present, they will need to run PLANTREGISTERCUSTOMSCRIPTS after installation in order for your new scripts to be recognized along with existing scripts.
In addition, you should use file names that are not likely to be used by other developers. Every plant developer will have to use the same folder, so prepending your script names with a company abbreviation is a good idea (i.e. ABC_EXPJOINT1.py).
Resources
The scripts are available from an installer here:
http://www.pdoteam.com/download/sample-script-installer/
The installer script is available here:
http://www.pdoteam.com/download/custom-script-installer/

## 评论

**内容**: William Jefferson Rañada said...
Hi,
I've tried following in this blog, tested the python script inside Plant 3d. I made a catalog containing only the custom script and inserted it into my spec, the problem is Plant 3d won't show the custom part even though I added it in my spec. Can you help me?
Reply
09/25/2020 at 05:44 PM

---
**内容**: Samir Joshi said...
Hi,
Is there a way to get the Parent Pipe OD on selecting pipe for Custom Support placement. The challenge is, if we give Parent Pipe Diameter as one of the Parameter in the script, there are chances that User changes it and it will create a non-matching geometry.
Reply
06/28/2023 at 12:55 AM

---
