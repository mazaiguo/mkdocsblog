---
title: "Custom Python Scripts for AutoCAD Plant 3D – Part 1"
date: 2015-06-01
categories:
  - Plant 3D
tags:
  - AutoCAD
  - Plant 3D
  - Python
description: "In this series of posts, we will cover developing custom python scripts for AutoCAD Plant 3D."
author: Autodesk
---
# Custom Python Scripts for AutoCAD Plant 3D – Part 1

发布日期: 2015-06-01

原始链接: https://adndevblog.typepad.com/autocad/2015/06/custom-python-scripts-for-autocad-plant-3d-part-1.html

## 文章内容

By David Wolfe (Contributor)
In this series of posts, we will cover developing custom python scripts for AutoCAD Plant 3D.
Along with learning about the development environment, we will cover troubleshooting, template scripts, and deployment. The original AU course covering scripts and Plant 3D is available here.
This blog article is going to assume some familiarity with Python.  There are a lot of great resources for learning python on the internet. To get started learning the language syntax I suggest using Code Academy.
This introductory article will start off by covering the basics of:
Description of the development process
Programs are necessary for development
Description of script types
Development Process
Unlike typical development done with .Net languages or even normal Python scripts, there is no integrated IDE for compiling, testing, and debugging.  The compiling is done by running a special command in Plant 3D, and then the scripts are loaded into memory for the AutoCAD session. Since the only way to test changes is to start a new AutoCAD session, the process of troubleshooting
The steps in the development process are:
Define function(s) for modeling the custom part
Define the metadata header
Test the script
Create the snapshots
Build a script package (if necessary)
Deploy the content
Through the rest of the articles, we’ll break down these steps even further so that you have an accurate understanding of the entire process. Along the way we will also develop a few custom scripts to help get you started.
Development Programs
Due to the prevalence of Python, there are many good free editors. Since we are not looking for an IDE (Integrated Development Environment), any of the text editors that highlight the Python syntax will work well.  I’ve used Komodo Edit, but my preference for text editors is TotalEdit Pro (now free).  Again, the main job here is just to color the text. All of the testing of the code will be done in AutoCAD Plant, and there is no debugger to step through.
When building scripts for Equipment, you will need to have a zip program. My personal favorite is 7-zip, as it integrates well with the Windows Explorer right-click menu.
With xml files, you can use Foxe which offers a customizable tree view of the xml beside the xml content with syntax highlighting. Here’s a quick article showing how to customize the tree.
Script Types
Plant 3D uses scripts in a couple different ways, for equipment and also for catalog content.  The scripts get stored in special folders inside the shared content folder.  The two special folders for scripts are:
C:\AutoCAD Plant 3D 20XX Content\CPak Common\equipment
C:\AutoCAD Plant 3D 20XX Content\CPak Common\CustomScripts
The paths are above are the default locations. If you are using a shared network location, these folder should be located there. You may have to create the CustomScripts folder as it is not present by default.
If you are going to create an object that will connect to piping, and show as an end connection on the isometric (and is not a nozzle), you should create an equipment script.  Any other type of script will be created as a custom script.
    Equipment Scripts
These basic shapes (primitives) are hard coded into the program, and you cannot add your own routines to this list.

Another type of script is for generating a complete equipment item. For example, the Centrifugal Pump script generates the entire pump, and the user inputs values for the parameters.
Scripts of this type generate the entire equipment item without removable parts.
Synopsis
In this article you learned some high-level information about developing Python scripts for Plant 3D. You learned which program will be used to modify equipment packages and script files, as well as the key locations for developing and testing those files. The next article will describe the parts of a custom script and the custom equipment packages in more detail.

## 评论

**内容**: Roberto Tsuri said...
Hi David!
¿Can these still work for 2018 Plant version?
Thanks!
Reply
11/01/2017 at 11:04 AM

---
