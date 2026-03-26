---
title: "Get the Rotation Angle and Axis from AcGeMatrix3d"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "The AcGeMatrix3d::rotation method returns a new matrix with the specified rotation angle, but how can we extract the angle from an existing matrix?..."
author: Autodesk
---
# Get the Rotation Angle and Axis from AcGeMatrix3d

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/get-the-rotation-angle-and-axis-from-acgematrix3d.html

## 文章内容

By Augusto Goncalves
The AcGeMatrix3d::rotation method returns a new matrix with the specified rotation angle, but how can we extract the angle from an existing matrix? The following code does this.
#define TWOPI 6.28318530718
void getAngleAndAxis(
           double& theta,
           AcGeVector3d& axis,
           const AcGeMatrix3d& m)
{
  // Contract:  The matrix `m' must NOT contain any scaling,
  // shearing or mirroring effects (i.e., m.det() must be 1.0).
  // See AcGeScale3d::removeScale( m ) to meet this contract
  // requirement. If axis is passed in such that it is non-zero,
  // then this method will attempt to orient the returned
  // axis in the same direction as the passed in axis,
  // i.e., the returned axis will be in the same half-space
  // as the original axis. (Note, the passed in axis will
  // be overwritten).
  //
  // Note that if the matrix has a mirror component,
  // ( ie the determinant = -1 ),  then its not possible to
  // construct a rotation that performs the transformation.
  // If you need convincing, then imagine how difficult it
  // would be rotate your left shoe, to be identical to your
  // right shoe ( its mirror image ).
    double trace, s;
  int i, j, k;
  double quat[4];
    assert(fabs(m.det() -1.0) <= AcGeContext::gTol.equalVector());
    trace = m(0, 0) + m(1, 1) + m(2, 2);
    if (trace > 0.0) {
    s = sqrt(trace + 1.0);
    quat[0] = s * 0.5;
    s = 0.5 / s;
    quat[1] = s * (m(2, 1) - m(1, 2));
    quat[2] = s * (m(0, 2) - m(2, 0));
    quat[3] = s * (m(1, 0) - m(0, 1));
    } else {
    i = 0;
    if (m(1, 1) > m(0, 0))
      i = 1;
    if (m(2, 2) > m(i, i))
      i = 2;
    j = (i + 1)%3;
    k = (i + 2)%3;
      s = sqrt(m(i, i) - (m(j, j) + m(k, k)) + 1.0);
    quat[i+1] = s * 0.5;
    s = 0.5 / s;
    quat[0] = s * (m(k, j) - m(j, k));
    quat[j+1] = s * (m(j, i) + m(i, j));
    quat[k+1] = s * (m(k, i) + m(i, k));
  }
    theta = 2.0 * acos(quat[0]);
  AcGeVector3d tempAxis;
    if (fabs(theta) >= AcGeContext::gTol.equalVector()) {
    double factor = 1.0 / sin(theta * 0.5);
    tempAxis.x = quat[1] * factor;
    tempAxis.y = quat[2] * factor;
    tempAxis.z = quat[3] * factor;
      // Flip direction and adjust angle if need be.
    //
    if (tempAxis.dotProduct(axis) < 0) {
      tempAxis *= -1;
      theta = TWOPI - theta;
    }
    axis = tempAxis;
  } else {
    theta = 0.0;
  }
}

## 评论

**内容**: andrea said...
Hi,
I have a blockreference, position -95,0,0 and rotation 180 degrees. (block is created on 0,0,0 and then reference is insert at -95,0,0 and then rotate by 180 degress).
If I use its Matrix with your code : axis returned is 0,0,1 and angle PI.
I expected that the values returned were axis -1,0,0 and rotation 0.
Thank you
Reply
10/20/2014 at 08:44 AM

---
**内容**: WolframKuss said...
I don't understand why you expect a zero angle when you did rotate the block by 180 degrees.
Normally rotations in ACAD are around z, so why do you expect x or -x as axis?
Please show us the matrix and it will be easy to see whether you rotated around (-)x or around(-)z.
What I would expect to be another, aequivalent, valid result besides the one returned by the code would be axis 0,0,-1 and angle -pi.
Reply
10/23/2014 at 07:05 AM

---
