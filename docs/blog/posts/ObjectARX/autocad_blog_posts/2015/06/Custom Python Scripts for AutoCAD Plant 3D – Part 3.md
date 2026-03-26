---
title: "Custom Python Scripts for AutoCAD Plant 3D – Part 3"
date: 2015-06-01
categories:
  - Plant 3D
tags:
  - AutoCAD
  - Plant 3D
  - Python
description: "Get start with Part 1 and Part 2 of this series."
author: Autodesk
---
# Custom Python Scripts for AutoCAD Plant 3D – Part 3

发布日期: 2015-06-01

原始链接: https://adndevblog.typepad.com/autocad/2015/06/custom-python-scripts-for-autocad-plant-3d-part-3.html

## 文章内容

By David Wolfe (Contributor)
Get start with Part 1 and Part 2 of this series.
Expansion Joint Script
This article will look at creating a completely new script, an expansion joint.
The script should look like this:
from varmain.primitiv import *
from varmain.custom import *
 
@activate(Group="Sleeve", TooltipShort="Expansion Joint", TooltipLong="Expansion Joint with Bellows", FirstPortEndtypes="FL", LengthUnit="in",  Ports="2")
@group("MainDimensions")
@param(D=LENGTH, TooltipShort="Pipe OD", TooltipLong="Pipe OD")
@param(D1=LENGTH, TooltipShort="Flange OD", TooltipLong="Flange OD")
@param(D31=LENGTH, TooltipShort="Bellows OD", TooltipLong="Bellows OD")
@param(L=LENGTH, TooltipShort="Length of the ExpansionJoint", TooltipLong="Overall Length of Expansion Joint")
@param(L31=LENGTH, TooltipShort="Flange Thickness", TooltipLong="Flange Thickness")
@param(T=LENGTH, TooltipShort="Bellows thickness", TooltipLong="Thickness of a bellow")
@param(B=LENGTH, TooltipShort="Number of Bolts", TooltipLong="Number of bolts")
@param(B1=LENGTH, TooltipShort="Bolt Size", TooltipLong="Bolt Thickness")
@param(B2=LENGTH, TooltipShort="Bolt Length (greater than L)", TooltipLong="Bolt Length")
@param(OF=LENGTH0)
 
 
#(arxload "PnP3dACPAdapter")
#(testacpscript "EXPJOINT1")
def EXPJOINT1(s, D=4.5, D31=5.5,D1 = 9.0, B=4, B1=0.75, B2=9.5, L=9.0, L31=0.25, T=0.5, K=1, OF=0, **kw ):
    NumOfBellow=round(((L - (2*L31))/ T)/2)-1
    #set a default hole size
    fhole = .95*D   
    #create a hole in the flange
    if OF > 0:
        fhole = (D-OF)
    #create our first flange
    Flange1=CYLINDER(s,R=D1/2, H=L31,O=0).rotateY(90)
    bellowlength = (T*2*NumOfBellow)-1
    nb = 0
    #overall length - belows length / 2 plus 1/4 the width of the bellow
    offset= ((L - bellowlength - (2*L31))/2)+L31
    expBody = CYLINDER(s,R=D31/2,H=L-L31,O=D).rotateY(90).translate((L31,0,0))
    #union the first flange and main body
    Flange1.uniteWith(expBody)
    expBody.erase()
    while (nb < NumOfBellow):       
        #create and offset our torus
        b=TORUS(s,R1=D31/2,R2=T/2).rotateY(90).translate((offset,0,0))
        #increment our offset distance
        offset = offset + T*2
        #union as we go
        Flange1.uniteWith(b)
        b.erase()
        nb = nb +1
    #create our end flange and offset it
    Flange2=CYLINDER(s,R=D1/2, H=L31,O=0).rotateY(90).translate((L - L31,0,0))
    Flange1.uniteWith(Flange2)
    Flange2.erase()
    #see if we need to create bolts, if there is a bolt cound and it's greater than 0
    if B > 1 and B1 > 0 and B2 > L:
        anglesplit = 360/B
        startangle = 0
    if B%2!=0:       
        startangle = anglesplit/2
    intbolt=0
    incangle=startangle
    platewidth=3*B1
    platelength=4*B1
    plateheight= 0.75*L31
    #make the bolts the length of the object + 2 flange thickness
    boltlength = L + 4*L31
    #calculate our offsets
    #plate on flg one offset
    pof1 = (L31 - plateheight/2,D1/2+platewidth/2,0)
    #translate the bolts
    bof1 = (-(B2-L),D1/2+platewidth/2,0)
    #translate the second plate
    pof2 = (L - (L31 - plateheight/2),D1/2+platewidth/2,0)
    #create a cylinder to subtract for the opening
    boreCy = CYLINDER(s,R=fhole/2, H=L,O=0).rotateY(90)
    Flange1.subtractFrom(boreCy)
    boreCy.erase()
    while (intbolt < B):
        #create a plate for the bolt, rotate it, and then move it to the edge and back to face of flange 1
        p = BOX(s,L=platewidth,W=platelength,H=plateheight).rotateX(90).translate(pof1).rotateX(incangle)
        #unite with flange 1 so we have a single body
        Flange1.uniteWith(p)
        p.erase()
        #create the bolt
        b = CYLINDER(s, R=B1/2, H=boltlength,O=0).rotateY(90).translate(bof1).rotateX(incangle)
        #join the flange and bolt
        Flange1.uniteWith(b)
        b.erase()
        #create our plate on flange 2
        p2 = BOX(s,L=platewidth,W=platelength,H=plateheight).rotateX(90).translate(pof2).rotateX(incangle)
        #merge the last plate
        Flange1.uniteWith(p2)
        p2.erase()
        incangle = incangle + anglesplit
        intbolt = intbolt + 1
    return
  Metadata
The most interesting part of this script, other than the geometry, is the metadata.
  Note that the group defines where the script shows up in the spec editor.
The tooltips show when the dimensions are hovered over in the editor as well.
Script Testing
While creating the script, you must be able to test it to see if your geometry can be generated.  Because these scripts are designed to be processed within AutoCAD, currently there is no IDE that you can use to debug the shapes. The process of testing the script looks like this.
Create your script file at C:\AutoCAD Plant 3D 2016 Content\CPak Common\CustomScripts (or wherever your Shared Content folder is for plant (MODIFYSHAREDCONTENTFOLDER).
Create your geometry functions, and metadata sections.
Start Plant 3D
Use PLANTREGISTERCUSTOMSCRIPTS. If there is an error in the script, you will get a warning at the command line with the line number. For most errors line of the script with the error will be listed.  If no errors are shown, the script compiled.
Load the PnP3dACPAdapter.arx. You can do this by pasting this at the command line (arxload "PnP3dACPAdapter")
Test the script. You can test with the default parameters by pasting this at the command line: (testacpscript "EXPJOINT1"). Fill in your script function where EXPJOINT1 is.
You can also test the script from one of the other following options:
    (TESTACPSCRIPT "CPFLR")
    (TESTACPSCRIPT "CPFLR" "D1" "300.5")
    (TESTACPSCRIPT "CPFLR" "L" "40" "D1" "300.5" "D2" "88.9")
Or
    (TESTACPSCRIPT1 "CPFLR")
    (TESTACPSCRIPT1 "CPFLR" "D1=300.5")
    (TESTACPSCRIPT1 "CPFLR" "L=40,D1=300.5,D2=88.9")
If you need to make changes, make them before closing Plant. That was you can try to register the script again to see if you still have breaking code.
If the script has been changed and registered, you must close Plant 3D in order to test the geometry again. Once the script is registered or run, the Python processor stores that script in memory until Plant 3D is closed, so starting a new session is the only way test new script changes.

## 评论

**内容**: Wane said...
Thanks for posting about Python scripts its been an interesting demo so far! Where do I find the .py files for the prebuilt equipment? in the .peqx files? all I can see is the .xmls and the images.
I was hoping to use some of the existing equipment to see how custom ones should be built.
Reply
11/24/2015 at 08:21 AM

---
**内容**: _davewolfe said...
Equipment scripts are defined as part of the deployed product scripts in
"C:\AutoCAD Plant 3D 2016 Content\CPak Common\variants.zip"

The EquipmentType > Name attribute is where the xml in the peqx references the stock script.
Reply
12/08/2015 at 07:08 AM

---
**内容**: vahap sungur said...
after writing codes it gives me error like "magic number...", do you know why?
Reply
05/22/2018 at 01:47 PM

---
**内容**: Milan Blom said...
Nice script, I was looking for a decent expansion joint model. I have gotten it to work up to the point I can add the component to a Plant3D model, but the componentn does not seem to have any ports.
Is there something wrong with the catalog definition, or is something missing from the script?
Reply
04/30/2021 at 03:07 AM

---
**内容**: Ahmed Ali said...
how can i add more sizes to the same expansion joint in this script
Reply
05/27/2021 at 02:37 PM

---
**内容**: Malcolm H said...
I am having a hard time with getting the figure to show up?
When I run testacpscript "EXPJOINT1" plant 3D returns nil.
What would cause this?
Reply
11/13/2023 at 05:22 AM

---
