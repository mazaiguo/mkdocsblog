---
title: "Custom Python Scripts for AutoCAD Plant 3D – Part 5"
date: 2016-01-01
categories:
  - Plant 3D
tags:
  - AutoCAD
  - Plant 3D
  - Python
description: "Get start with Part 1, Part 2, Part 3 and Part 4 of this series."
author: Autodesk
---
# Custom Python Scripts for AutoCAD Plant 3D – Part 5

发布日期: 2016-01-01

原始链接: https://adndevblog.typepad.com/autocad/2016/01/custom-python-scripts-for-autocad-plant-3d-part-5.html

## 文章内容

By David Wolfe (Contributor)
Get start with Part 1, Part 2, Part 3 and Part 4 of this series.
Python Script Nozzles in AutoCAD Plant 3D
This article will look at creating a nozzle to use in the nozzles catalog which AutoCAD Plant 3D equipment loads when putting nozzles on equipment.
The full sample is available at this link. The script should look like this:
# Embedded file name: varmain\pipesub\cpp_f_f_.pyc
from aqa.math import *
from varmain.flangesub.cpfwo import *
from varmain.pipesub.cpp_util import *
from varmain.primitiv import *
from varmain.var_basic import *
from varmain.custom import *

@activate(Group="StraightNozzle,Nozzle", TooltipShort="Long Weld Neck", TooltipLong="Long Weld Neck", LengthUnit="in", Ports="2")
@group("MainDimensions")
@param(D10=LENGTH, TooltipShort="Nominal Outside Diameter",TooltipLong="Nominal Outside Diameter")
@param(L1=LENGTH, TooltipShort="Overall Length.", TooltipLong="Overall Length")
@param(L2=LENGTH, TooltipShort="Hub Length", TooltipLong="Length of flange with weld neck.")
@param(OF=LENGTH, TooltipLong="Length between connection points.")
@param(B1=LENGTH, TooltipLong="Flange Thickness")
@param(D12=LENGTH, TooltipLong="Flange OD Width")
@param(D13=LENGTH, TooltipLong="OD of Weld neck")

def nozflange(s, D10 = 4.5, L1 = 9, L2 = 3, B1 = 0.94, D12 = 9, D13 = 5.31, OF = -1.0,**kw):
    xH1 = D12 + OF * 2.0
    if D12 < xH1:
        D12 = xH1
    W1 = D12
    DI = .25
    DO = .25
    #create the nozzle extension
    if L1 > 0:
        oTH = CYLINDER(s, R=D10 / 2.0, H=L1, O=D10 - (DO / 2.0)).rotateY(90.0)
    else:
        oTH = None
        L1 = -L1
    oF1 = CPFWO(s, L=L2, B=B1, D1=D12, D2=D10, D3=D13, W=W1, OF=OF)
    if oTH:
        oTH.uniteWith(oF1)
        oF1.erase()
    if W1 <= D12:
        WA1 = 0.0
    else:
        WA1 = 90.0
#set port points
    s.setPoint((0.0, 0.0, 0.0), (-1.0, 0.0, 0.0), WA1, 0.0, L2)
    s.setPoint((L1, 0.0, 0.0), (1.0, 0.0, 0.0), 0, 0.0, L2)
    return
Metadata
First we have the includes, this script the includes section is particular important because we are using some of the stock flange scripts (flangesub, pipesub).
# Embedded file name: varmain\pipesub\cpp_f_f_.pyc
from aqa.math import *
from varmain.flangesub.cpfwo import *
from varmain.pipesub.cpp_util import *
from varmain.primitiv import *
from varmain.var_basic import *
from varmain.custom import *
Second is the section declaring our tooltips and parameters.  One the first line here, because we want the script listed under the StraightNozzle and Nozzle categories, we include both.
@activate(Group="StraightNozzle,Nozzle", TooltipShort="Long Weld Neck", TooltipLong="Long Weld Neck", LengthUnit="in", Ports="2")
@group("MainDimensions")
@param(D10=LENGTH, TooltipShort="Nominal Outside Diameter",TooltipLong="Nominal Outside Diameter")
@param(L1=LENGTH, TooltipShort="Overall Length.", TooltipLong="Overall Length")
@param(L2=LENGTH, TooltipShort="Hub Length", TooltipLong="Length of flange with weld neck.")
@param(OF=LENGTH, TooltipLong="Length between connection points.")
@param(B1=LENGTH, TooltipLong="Flange Thickness")
@param(D12=LENGTH, TooltipLong="Flange OD Width")
@param(D13=LENGTH, TooltipLong="OD of Weld neck")
 
StraightNozzles
 
Nozzle class shown by clicking advanced shape options and selecting nozzle.
Testing
To test the script, I made a tool palette icon with this in the macro portion:
^C^CPLANTREGISTERCUSTOMSCRIPTS;^C^C(command "arx" "l" "Pnp3dacpadapter");(testacpscript "nozflange");
Once the script is tested, we need to be able to test it in a catalog.  For Plant 3D, all of the nozzles are read from a shared content folder path. You can find the path by running the spec editor as administrator, and then going to Tools > Modify Shared Content folder.
The default path is C:\AutoCAD Plant 3D 2016 Content\.
The default path for the nozzle catalog is "C:\AutoCAD Plant 3D 2016 Content\CPak Common\NOZZLE Catalog.acat"
To open the nozzle catalog, switch to the Catalogs tab, and go to open, and then browse to it.  Once in the catalog you can click create new component and select your script. Fill in some sample data and save your catalog component and the catalog. Note that for flanged nozzles, your end type and pressure class must be set.
In a project drawing, create a piece of equipment, and then pick your nozzle.
You can change the nozzle orientation in the Change location tab.
Note that if you want the user to override the nozzle length, you should use the L parameter in your script. In this case (using L1), for a long weld neck, the catalog data will drive the length, and the user won’t be able to change it.
Deployment
Because you can’t directly modify the nozzle catalog on a user’s computer without overwriting it, you should deploy a folder (eg CPak Custom Nozzles) with your nozzle catalog. The user then will be responsible to add the nozzles. Another option would be to deploy two catalogs, one with the stock nozzles + your custom nozzles, and one with just your custom nozzles.  You could write an installer that lets the user pick which of the two installs they want.  In either case, you should use a property like Design Pressure Factor to include unique information so that they can quickly filter to locate your nozzles.

## 评论

**内容**: Reza said...
Dear David,
I want to create equipment in plant 3d from predefined shape. (1 Torispheric Head, 2 Cylinder, ...)
I want to implement it in C# program.
Best Regards
Reply
02/23/2016 at 12:10 AM

---
**内容**: _davewolfe said...
Did you look at the samples in the 2016 Plant 3d SDK? They added an equipment api in 2016. http://usa.autodesk.com/adsk/servlet/index?siteID=123112&id=15460551
Reply
02/24/2016 at 06:05 AM

---
**内容**: Reza said...
Thank you for your comment. In sample code, equipment created from predefined template (Create from package). I want to create equipment from predefined shape like torispheric Head + cylinder + ..)
Actually I want to import PVELITE model in autocad plant 3d. I can extract equipment shape from SQLite database of PVELITE file.
CADWorx impliment import of PVELITE in his software.
Any comment will be depreciated.
Reply
02/28/2016 at 06:23 AM

---
**内容**: Ajay said in reply to Reza...
send your code on ajay1579@gmail.com, i will develope it further
Reply
10/20/2021 at 04:50 AM

---
**内容**: _davewolfe said...
I think you'll have to build your own model using AutoCAD 3d solids and then convert that to an equipment block. PV Elite can add more types with dimensional data that doesn't correlate to the Plant 3d equipment drawing methods.
Reply
03/07/2016 at 07:34 AM

---
**内容**: Florin R said...
Dear David
I made python compiled files and script group with PLANTREGISTERCUSTOMSCRIPTS .. how to assemble that in .peqx
Reply
07/16/2018 at 05:56 AM

---
**内容**: Niels van den Belt said...
Good afternoon,
What code can be used in Python to get a grabpoint for changing the length?
in example the pipe support lenght sliding parameter.
Is it the Ask4Dist=True command?

Niels
Reply
02/26/2021 at 03:44 AM

---
**内容**: Jose Manuel Arce said...
Hello dear Dave
I am working generating supports for pipes in autocad plant 3d with the Python program and I have the following problem when trying to compile the source file:
ModuleNotFoundError: No module named 'aqa'
Could you help me, I'm going to thank you very much.
Greetings
Reply
04/23/2021 at 05:25 PM

---
**内容**: rakesh said...
Hi david,
could you share the python script to import spec from excel or csv file?
i want to create new spec in plant 3d using excel file or csv file data? How this can be achieved pls help.
Reply
05/15/2022 at 06:12 AM

---
