---
title: "Using PhysiJS for collision detection in AutoCAD"
date: 2015-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Solid
description: "AutoCAD solids when imported in a Three.js scene can be used for some interesting physics simulations. Collision detection of certain solids with o..."
author: Autodesk
---
# Using PhysiJS for collision detection in AutoCAD

发布日期: 2015-01-01

原始链接: https://adndevblog.typepad.com/autocad/2015/01/using-physijs-for-collision-detection-in-autocad.html

## 文章内容

By Balaji Ramamoorthy
AutoCAD solids when imported in a Three.js scene can be used for some interesting physics simulations. Collision detection of certain solids with other solids in the scene can be one of them. In this blog post, we will look at using PhysiJS to identify the minimum and maximum swing angle of a rotating arm as it collides with two other solids that act as stoppers.
Here is a video recording : 
  In this PhysiJS scene, we create three types of meshes.
1) The mesh that will be rotated. In our case, the rotating swing arm.
2) The solids that will be grounded. In our case, the stoppers with which the swing arm will collide but the stoppers will not be affected by the collision.
3) Any other AutoCAD solids that may not be of interest in the collision detection and can safely be imported as Three.JS meshes. PhysiJS will not compute collision with such meshes as they are not PhysiJS mesh. An example of such mesh in our case is the solid that supports the rotating swing arm.
To classify the solids in the drawings under one of the above categories, an XData has been added to the driven and grounded solids with a reg appname set to "PHYSIMESHTYPE". 
A few points to note about the implementation :
- At present, the driven solid is always assumed to be rotating at origin and along the Z axis.
- The force applied by the motor on the driven solid is fixed at 100 units. Depending on the mass of the solid being driven, this may be required to be changed. Too less force would result in no rotation of the swing arm while too much force will swing it too fast.
- The restitution value of the material is intentionally set to zero to ensure that the swing arm does not bounce back on impact with the stopper.
- The accuracy with which the angle of the swing arm after it collides with the stopper seems to be dependent on the mesh type and also due to the computational errors introduced by PhysiJS's collision detection algorithm. In my tests using a test drawing, while the exact value at which the swing arm should be stopping was 13 degrees, the value obtained by using PhysiJS was at 12.53 degrees. 
To try it, 
1) please download the files from Kean's blog on integrating AutoCAD with Three.js.
Connecting Three.js to an AutoCAD model Part II
2) Download PhysiJS from here : PhysiJS
3) Replace the following files that includes the changes mentioned in this blog post :
Download Utils.cs
Download Threesolids2.js
Download Threesolids2.html
Download Acadext2.js
Here is the sample drawing with XData attached to the solids to identify driven, grounded and other solids which do not participate in collision detection.
Download Swing.dwg

## 评论

**内容**: SUBIR DUTTA said...
https://www.youtube.com/watch?v=ALRbjoS5FMc&list=UUUr2BV073IhpBOQ41Phzd6w
Reply
01/06/2015 at 10:22 PM

---
**内容**: Balaji said...
Hi Subir,
That's a nice one !
Thanks for sharing
Cheers,
Balaji

Reply
01/06/2015 at 10:27 PM

---
