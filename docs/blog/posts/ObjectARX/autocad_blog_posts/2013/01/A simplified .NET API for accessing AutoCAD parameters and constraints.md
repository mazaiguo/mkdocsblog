---
title: "A simplified .NET API for accessing AutoCAD parameters and constraints"
date: 2013-01-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
description: "This post is an updated version of Kean's post about the simplified constraint API we developed a while ago. At the time we posted it, this AutoCAD..."
author: Autodesk
---
# A simplified .NET API for accessing AutoCAD parameters and constraints

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/a-simplified-net-api-for-accessing-autocad-parameters-and-constraints.html

## 文章内容

By Philippe Leefsma
This post is an updated version of Kean's post about the simplified constraint API we developed a while ago. At the time we posted it, this AutoCAD DevBlog wasn’t existing yet, so the reason why I’m posting that myself today is because, being the main author of that library, it will be easier to manage comments directly rather than through Kean’s blog.
In the 2010 release, we introduced 2D geometric constraints to AutoCAD. The feature was implemented using AutoCAD’s low-level – and very powerful – Associative Framework, which has subsequently been used to implement features such as parametric surfaces in AutoCAD 2011 (more information on that here). Our initial API implementation for creating and accessing geometric constraints (which you can find out more about via the DevTV session linked to from this previous post) in many ways reflects the low-level nature of the underlying framework: it was unfortunately just a bit too complicated for most mortals to get to grips with.
Gopinath Taget, a colleague from DevTech Americas, and myself have worked with our Engineering team to develop a “high-level” API for constraints inside AutoCAD, which does a great job of abstracting away much of this complexity.
This API distribution
includes VS2008, VS2010 and VS2012 solutions containing projects for the C++ API, the mixed-mode layer exposing this to .NET and a test project for each of these managed and unmanaged APIs.
Beyond that, a custom implementation using that library should be relatively straightforward: I suggest trying out the various commands implemented in the test project to get a feel for what’s possible, as well as taking a look at the compiled help-file provided in the Help folder.
Here are a list of these commands with a brief description of what they do:
MGHLCOIN – creates a coincident constraint
MGHLPAR – creates a parallel constraint
MGHLPERP – creates a perpendicular constraint
MGHLCONC – creates a concentric constraint
MGHLCOLIN – creates a co-linear constraint
MGHLHOR – creates a horizontal constraint
MGHLVERT – creates a vertical constraint
MGHLFIX – creates a fix constraint
MGHLTAN – creates a tangent constraint
MGHLG2SM – creates a smooth constraint
MGHLSYM – creates a symmetric constraint
MGHLEQLN – creates a equal length constraint
MGHLEQRAD – creates a equal radius constraint
MGHLDIMALIGN – creates an aligned dimensional constraint
MGHLPARAM – illustrates several functionalities of AssocUtil Parameter API (query, creation, modification, renaming)
Feel free to post your feedback about the library and report any issue you may encounter while working with it.

## 评论

**内容**: Matthias Mueller said...
Hey Philippe,
thanks - the Util is great. It reduces a lot of complex coding and can be applied to all entities.
One thing I noted when applying a coincidental constraint between two entities: the right-hand entity (x-axis) is always moved. The left-handed keeps its location.
A small improvement would be to determine that the first selected is the "base entity" and the second will than be moved.
Reply
02/01/2013 at 08:06 AM

---
**内容**: Philippe Leefsma said in reply to Matthias Mueller...
Hi Matthias,
It is actually not straightforward to handle this king of behavior. Since the behavior is not considered as a bug, I'm afraid it will remain like this for a while.
Here are some indications provided by the designer of the constraint API in AutoCAD:
The constraints UI code does it by hinting the constraint group to temporarily fix the geometry that should not move and then trying to evaluate. If the evaluation does not work it unfixes the geometry (as fixing it was too much) and evaluates again.
There is a public class AcDbEvalContext that can be used to pass hint about what to fix. The AcDbEvalContextPair that indicates geometry tried to stay fixed has key “TempFixedConsGeoms” and the value is AcDbFullSubentPathArray of the geometries that should be fixed.
The constraint group obtains AcDbEvalContext by calling AcDbAssocEvaluationCallback::getAdditionalData(). You will need to implement your own class derived from AcDbAssocEvaluationCallback, implement its AcDbAssocEvaluationCallback::getAdditionalData() to return AcDbEvalContext that would contain one AcDbEvalContextPair whose key would be “TempFixedConsGeoms” and value would be AcDbFullSubentPathArray of the geometries that should not move. You need to temporarily use your new AcDbAssocEvaluationCallback when evaluating the newly added constraint by calling AcDbAssocManager::addGlobalEvaluationCallback(), and then remove it by calling AcDbAssocManager::removeGlobalEvaluationCallback() after the evaluation is over.
Reply
02/01/2013 at 04:01 PM

---
**内容**: Philippe Leefsma said in reply to Philippe Leefsma...
Hi Matthias, I was implementing the proposed changes, so now the first entity passed to the API methods is considered as the base and should not move. Please give it a try and let me know.
Reply
02/14/2013 at 02:45 AM

---
**内容**: Stefan Dunst said...
Hi Philippe,
I wanted to ask if there is any possibility or workaround to get this API working with the COM API?
I wanted to try to get it simpy working by including the dll, but the Problem then is that the .NET and the COM API use different Types for Object IDs...
Reply
08/07/2013 at 01:07 AM

---
**内容**: Philippe said in reply to Stefan Dunst...
Hi Stefan,
This API will run only in-process with AutoCAD, so I don't get the point of using it with COM.
A COM ObjectId is different than a .Net ObjectId, because every type used by COM has to be COM wrapped. You should however be able to build a .Net ObjectId from the COM object: try ObjectId id = new ObjectId(COM.ObjectId)
Reply
08/07/2013 at 02:49 AM

---
**内容**: Matthias Mueller said...
Hi Philippe, any change that you unify the .dll names for both the x64 and x86 version? Currently the x64 version has an additional "Adsk" prefixed.
I want to use your lib as reference in a shared dev environment with x64 and x86 configurations. Thanks!
Reply
12/03/2013 at 05:02 AM

---
**内容**: Philippe Leefsma said in reply to Matthias Mueller...
Hi Matthias,
It's pretty straightforward to change on your side: go to the project properties in visual studio, then Linker->Output and change the name of the output dll file. I hope it helps.
Reply
12/16/2013 at 01:27 AM

---
**内容**: Alexander Rivilis said in reply to Philippe Leefsma...
Dear Philippe!
File https://adndevblog.typepad.com/adnassocconstraintapi-1.zip is not found. Please re-upload it.
Reply
07/17/2019 at 06:03 AM

---
**内容**: Alexander Rivilis said in reply to Alexander Rivilis...
Oops! Now I can download it. Look like it was a temporary problem.
Reply
07/17/2019 at 06:08 AM

---
**内容**: HT said...
I used MGHLDIMALIGN command .Result not like result of DCALIGNED command with Point & Line option in Autocad .Please explain to me ?
Thanks!
Reply
05/26/2014 at 03:02 AM

---
**内容**: Philippe Leefsma said in reply to HT...
Hi, Can you clarify what you mean by "not like"? That API is not intended to provide a result 100% similar to what you get using the UI commands. It does it job by helping to easily generate the constraints with a minimal effort from third party developers... If you are looking for an identical result to the UI, you will probably have to take a closer look at the implementation and extend it the way you like.
Reply
05/26/2014 at 03:11 AM

---
**内容**: HT said in reply to Philippe Leefsma...
In API,aligned dimensional constraint of MGHLDIMALIGN command used addDistanceConstraint function with AcConstrainedGeometry* pConsGeom1
and AcConstrainedGeometry* pConsGeom2 parameters. pConsGeom1 and pConsGeom2 are AcConstrainedImplicitPoint class ,so pConsGeom1 and pConsGeom2 is star point or end point.Meanwhile with DCALIGNED command ,pConsGeom1 and pConsGeom2 are corresponding xLine1Point and xLine2Point .Not when xLine1Point as well as star point or end point .That is "not like".How from
Acgepoint3d xLine1Point obtained AcConstrainedPoint *pConsGeom1 ?
Thanks !
Reply
05/26/2014 at 05:55 AM

---
**内容**: HT said...
AcConstrainedCurve* pConstrainedCurve = AcConstrainedCurve::cast(pConsGeom1);
AcGraphNode::Id id = pConstrainedCurve->nodeId();
AcConstrainedImplicitPoint* imp = new AcConstrainedImplicitPoint(id,AcDb::kMidImplicit);
AcGePoint3d pt ;
pt = imp->point();
why to appear "Unhandled exception at 0x103fa383 in acad.exe: 0xC0000005: Access violation reading location 0x00000004." when run pt = imp->point(); line
Reply
05/28/2014 at 08:37 AM

---
**内容**: Philippe Leefsma said in reply to HT...
Based on such a tiny code fragment I have no idea... You would need to provide a complete code sample that illustrates what you are doing.
Thank you.
Reply
05/28/2014 at 11:17 PM

---
**内容**: HT said in reply to Philippe Leefsma...
Hi Philippe Leefsma !
I will create distance constraint from one point of a line to line.The one point is midpoint. I have 2 line corresponding 2 AcConstrainedCurve object . Now, i don't how to get midpoint which is AcConstrainedImplicitPoint object of one AcConstrainedCurve object. So, I try used AcConstrainedImplicitPoint Constructor : new AcConstrainedImplicitPoint (id,AcDb::kMidImplici) to get implicit point .
Please help me ! Thank you !
Reply
05/28/2014 at 11:57 PM

---
**内容**: Philippe Leefsma said in reply to HT...
Well you would first need to create a constrained curve from the line, take a look at the internal implementation of the High Level API, it may give you some clue on how to do it. I don't have a sample which creates an AcConstrainedImplicitPoint, so I cannot help you further.
When running the "ArxConstraintTest_hlDimAlign" command, it is possible to select the center of a line and a point on another line, it should create a dim constraint between the closest points on the entity you selected. I wonder why this is not good enough for you.
Reply
05/30/2014 at 12:18 AM

---
**内容**: HT said in reply to Philippe Leefsma...
Thanks for reply from you.
"ArxConstraintTest_hlDimAlign" command just create a dim constraint between the star point or endpoint on this entity with starpoint or endpoint on another entity.That represents in getClosestConstrainedPoint func , when getting ImplicitPoints by getConstrainedImplicitPoints func ,it return the point which i don't want .For example ,
getConstrainedImplicitPoints of a line ,return value just star and endpoint, don't have midpoint ,to i maybe get AcConstrainedImplicitPoint (that midpoint )is input for addDistanceConstraint func . That is hard.
Reply
05/30/2014 at 01:34 AM

---
**内容**: HT said...
Hi Philippe Leefsma .
AcConstrainedImplicitPoint(
AcGraphNode::Id constrCurvId,
AcDb::ImplicitPointType ptype,
int index = -1
);
Can tell me the meaning that Constructor ? What makes it so
Reply
05/30/2014 at 07:17 AM

---
**内容**: HT said...

Hi Philippe Leefsma .
Can you give to me sample for AcConstrainedImplicitPoint Constructor ?
Thanks.
Reply
06/01/2014 at 07:41 PM

---
**内容**: Philippe Leefsma said in reply to HT...
I don't have any. I will check with a colleague in the development team if he can provide a sample or some guidance.
Reply
06/01/2014 at 08:08 PM

---
**内容**: HT said in reply to Philippe Leefsma...
Thanks you so much.I need it!
Reply
06/01/2014 at 08:51 PM

---
**内容**: Philippe Leefsma said...
By the way, what happen if you pass the AcConstrainedCurve::nodeId as first parameter? This seem to be the logical id to use in that constructor
Reply
06/01/2014 at 08:17 PM

---
**内容**: HT said in reply to Philippe Leefsma...
In AcDbAssoc2dConstraintGroup object ,i added 2 AcConstrainedCurve object and construct a AcConstrainedImplicitPoint with NodeId of a that AcConstrainedCurve object and type = AcDb::kMidImplicit.
But when getConstrainedGeometries of that ConstraintGroup ,I just retrieve 6 AcConstrainedGeometry.These are 2 AcConstrainedCurve entry , 2 AcConstrainedPoint ( corresponding starpoint and endpoint ) of each AcConstrainedCurve .This AcConstrainedCurve is corresponding a line in autocad.
That AcConstrainedImplicitPoint ,i added ConstraintGroup ,where it?
Reply
06/01/2014 at 08:47 PM

---
**内容**: HT said in reply to HT...
// add a AcConstrainedCurve in a ConstraintGroup
es = p2dConstrGrp->addConstrainedGeometry(aPaths[i], pConsGeom);
// add a AcConstrainedImplicitPoint is on a AcConstrainedCurve .I think it is in a // ConstraintGroup.
AcGraphNode::Id nodeId = pConsGeom->nodeId();
AcConstrainedImplicitPoint *imp = new AcConstrainedImplicitPoint(nodeId,AcDb::kMidImplicit);
// Test to make sure that AcConstrainedImplicitPoint is on AcConstrainedCurve
AcGraphNode::Id nodeId1 = imp->constrainedCurveId();
AcConstraintGroupNode* pNode = p2dConstrGrp->getGroupNodePtr(nodeId1);
AcConstrainedCurve* pCurve1 = AcConstrainedCurve::cast(pNode);
// test to make sure AcConstrainedCurve is in ConstraintGroup
AcDbObjectId idgroup = pCurve1->owningConstraintGroupId();
Via that 2 test way , AcConstrainedImplicitPoint is on AcConstrainedCurve . AcConstrainedCurve is in ConstraintGroup. But AcConstrainedImplicitPoint not is in ConstraintGroup . Expressed through :
AcDbObjectId idgroup = imp->owningConstraintGroupId();
Result idgroup = NULL.
So , getConstrainedGeometries of that ConstraintGroup ,not retrieve AcConstrainedImplicitPoint .
How to add AcConstrainedImplicitPoint in ConstraintGroup ?
Reply
06/02/2014 at 12:34 AM

---
**内容**: Philippe Leefsma said in reply to HT...
Here should be the solution:
Call AcDbImpAssoc2dConstraintGroup::getConstrainedGeometry(fullSubentPath, pConsGeom, true/*bCreateArcLineMid*/) and pass fullSubentPath of the edge subentity that contains the midpoint. It should then create and return (in pConsGeom) an AcConstrainedCurve and three AcConstrainedImplicitPoints (start, end, mid) connected to the AcConstrainedCurve via AcPointCurveConstraints. You can then obtain the implicit points from the constrained curve by calling AcConstrainedCurve::getConstrainedImplicitPoints().
Reply
06/12/2014 at 04:00 PM

---
