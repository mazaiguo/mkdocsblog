---
title: "Custom Python Scripts for AutoCAD Plant 3D – Part 2"
date: 2015-06-01
categories:
  - Plant 3D
tags:
  - AutoCAD
  - PDF
  - Plant 3D
  - Python
description: "Check here the Part 1 of this series."
author: Autodesk
---
# Custom Python Scripts for AutoCAD Plant 3D – Part 2

发布日期: 2015-06-01

原始链接: https://adndevblog.typepad.com/autocad/2015/06/custom-python-scripts-for-autocad-plant-3d-part-2.html

## 文章内容

By David Wolfe (Contributor)
Check here the Part 1 of this series.
The first example script is taken from an older Autodesk University class (AU Python PDF). The pdf is available here. Beginning on page 44, the pdf creates a sample script. The script should look like this:
from aqa.math import *
from varmain.primitiv import *
from varmain.custom import *
 
@activate(Group="Support",
 TooltipShort="Test script",
 TooltipLong="This is a custom Testscript", 
 LengthUnit="in",
 Ports=1)
@group("MainDimensions")
@param(D=LENGTH, TooltipShort="Cylinder Diameter", Ask4Dist=True)
@param(L=LENGTH, TooltipLong="Length of the Cylinder")
@param(OF=LENGTH0)
@group(Name="meaningless enum")
@param(K=ENUM)
@enum(1, "align X")
@enum(2, "align Y")
@enum(3, "align Z")
#--------------------------------------------------------
#(arxload "PnP3dACPAdapter")
#(testacpscript "TESTSCRIPT" "D" "4.5" "L" "12")
def TESTSCRIPT(s, D=80.0, L=150.0, OF=-1, K=1, **kw):
    CYLINDER(s, R=D/2, H=L, O=0.0).rotateY(90)
Scripts Parts
There are three sections to this script, the imports section, the metadata section, and the actual shape script.  In addition, you may create functions as needed for your shape generation.
Imports
The imports section lists other python classes and functions that may be used by the current script. In order to avoid having to tell Plant 3D what a cylinder is and how to draw it, we can simpler reference a function (CYLINDER) and use that in our scripts.  The imports section is resolved by the AutoCAD Plant 3D Python interpreter, and as such, doesn’t load into other IDE’s.  The imports shown here are basic ones, but others available in the actual product scripts. Some of the scripts used by Plant 3D are available upon request through ADN.
Metadata
The metadata section instructs the PLANTREGISTERCUSTOMSCRIPTS command how to treat the script being registered. One of the key pieces not shown in the original Python script sample is the number of Ports.  In order for the script to be used in the Spec Editor, the number of ports must be included in the metadata section.
Some of the other parameters referenced in the AU python documentation aren’t used. The image options will be explained in future posts.
Shape Scripts
Before getting into the script portion, notice the comments above the line that starts with def.  In Python, comment rows start with pound signs (#). It’s easier to test your script if you can copy the lines minus the comments to the command line to load the testing adapter, and then call the script with values.
In any case, the def line defines our shape function that will be called to create a script. The registration command looks for the function that matches the script file name.  If you create additional functions to use within your shape script, you must locate them above the script so the script will compile. For example, to use a function called FlangeSizeCalc, you would have to define it first and then reference it lower in the script file.
Shape scripts can get complicated, so you should contact ADN to view samples that work.  In addition the AU Python PDF gives more details on how to move objects and use Boolean operations to get the shape needed.
Finished Script
At the beginning you saw the finished script.  Here is a screenshot of the final product with images being used in the spec editor.
Figure 1: script thumbnail
Figure 2: dimension images and tool tips

Figure 3: register custom script files

## 评论

**内容**: vahap sungur said...
hello, when I trying to run this codes it gives me error "import error , magic number......"
can you help me to solve this error?
best regatds
vahap sungur
vsungur@yahoo.com
Reply
05/09/2018 at 03:04 PM

---
