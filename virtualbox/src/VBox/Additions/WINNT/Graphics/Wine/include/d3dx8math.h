/*
 * Copyright (C) 2007 David Adam
 * Copyright (C) 2007 Tony Wasserka
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA
 */

/*
 * Oracle LGPL Disclaimer: For the avoidance of doubt, except that if any license choice
 * other than GPL or LGPL is available it will apply instead, Oracle elects to use only
 * the Lesser General Public License version 2.1 (LGPLv2) at this time for any software where
 * a choice of LGPL license versions is made available with the language indicating
 * that LGPLv2 or any later version may be used, or where a choice of which version
 * of the LGPL is applied is otherwise unspecified.
 */

#include <d3dx8.h>

#ifndef __D3DX8MATH_H__
#define __D3DX8MATH_H__

#include <math.h>

#define D3DX_PI    ((FLOAT)3.141592654)
#define D3DX_1BYPI ((FLOAT)0.318309886)

#define D3DXToRadian(degree) ((degree) * (D3DX_PI / 180.0f))
#define D3DXToDegree(radian) ((radian) * (180.0f / D3DX_PI))

typedef struct ID3DXMatrixStack *LPD3DXMATRIXSTACK;

DEFINE_GUID(IID_ID3DXMatrixStack,
0xe3357330, 0xcc5e, 0x11d2, 0xa4, 0x34, 0x0, 0xa0, 0xc9, 0x6, 0x29, 0xa8);

typedef struct D3DXVECTOR2
{
#ifdef __cplusplus
    D3DXVECTOR2();
    D3DXVECTOR2(CONST FLOAT *pf);
    D3DXVECTOR2(FLOAT fx, FLOAT fy);

    operator FLOAT* ();
    operator CONST FLOAT* () const;

    D3DXVECTOR2& operator += (CONST D3DXVECTOR2&);
    D3DXVECTOR2& operator -= (CONST D3DXVECTOR2&);
    D3DXVECTOR2& operator *= (FLOAT);
    D3DXVECTOR2& operator /= (FLOAT);

    D3DXVECTOR2 operator + () const;
    D3DXVECTOR2 operator - () const;

    D3DXVECTOR2 operator + (CONST D3DXVECTOR2&) const;
    D3DXVECTOR2 operator - (CONST D3DXVECTOR2&) const;
    D3DXVECTOR2 operator * (FLOAT) const;
    D3DXVECTOR2 operator / (FLOAT) const;

    friend D3DXVECTOR2 operator * (FLOAT, CONST D3DXVECTOR2&);

    BOOL operator == (CONST D3DXVECTOR2&) const;
    BOOL operator != (CONST D3DXVECTOR2&) const;
#endif /* __cplusplus */
    FLOAT x, y;
} D3DXVECTOR2, *LPD3DXVECTOR2;

#ifdef __cplusplus
typedef struct D3DXVECTOR3 : public D3DVECTOR
{
    D3DXVECTOR3();
    D3DXVECTOR3(CONST FLOAT *pf);
    D3DXVECTOR3(CONST D3DVECTOR& v);
    D3DXVECTOR3(FLOAT fx, FLOAT fy, FLOAT fz);

    operator FLOAT* ();
    operator CONST FLOAT* () const;

    D3DXVECTOR3& operator += (CONST D3DXVECTOR3&);
    D3DXVECTOR3& operator -= (CONST D3DXVECTOR3&);
    D3DXVECTOR3& operator *= (FLOAT);
    D3DXVECTOR3& operator /= (FLOAT);

    D3DXVECTOR3 operator + () const;
    D3DXVECTOR3 operator - () const;

    D3DXVECTOR3 operator + (CONST D3DXVECTOR3&) const;
    D3DXVECTOR3 operator - (CONST D3DXVECTOR3&) const;
    D3DXVECTOR3 operator * (FLOAT) const;
    D3DXVECTOR3 operator / (FLOAT) const;

    friend D3DXVECTOR3 operator * (FLOAT, CONST struct D3DXVECTOR3&);

    BOOL operator == (CONST D3DXVECTOR3&) const;
    BOOL operator != (CONST D3DXVECTOR3&) const;
} D3DXVECTOR3, *LPD3DXVECTOR3;
#else /* !__cplusplus */
typedef struct _D3DVECTOR D3DXVECTOR3, *LPD3DXVECTOR3;
#endif /* !__cplusplus */

typedef struct D3DXVECTOR4
{
#ifdef __cplusplus
    D3DXVECTOR4();
    D3DXVECTOR4(CONST FLOAT *pf);
    D3DXVECTOR4(FLOAT fx, FLOAT fy, FLOAT fz, FLOAT fw);

    operator FLOAT* ();
    operator CONST FLOAT* () const;

    D3DXVECTOR4& operator += (CONST D3DXVECTOR4&);
    D3DXVECTOR4& operator -= (CONST D3DXVECTOR4&);
    D3DXVECTOR4& operator *= (FLOAT);
    D3DXVECTOR4& operator /= (FLOAT);

    D3DXVECTOR4 operator + () const;
    D3DXVECTOR4 operator - () const;

    D3DXVECTOR4 operator + (CONST D3DXVECTOR4&) const;
    D3DXVECTOR4 operator - (CONST D3DXVECTOR4&) const;
    D3DXVECTOR4 operator * (FLOAT) const;
    D3DXVECTOR4 operator / (FLOAT) const;

    friend D3DXVECTOR4 operator * (FLOAT, CONST D3DXVECTOR4&);

    BOOL operator == (CONST D3DXVECTOR4&) const;
    BOOL operator != (CONST D3DXVECTOR4&) const;
#endif /* __cplusplus */
    FLOAT x, y, z, w;
} D3DXVECTOR4, *LPD3DXVECTOR4;

#ifdef __cplusplus
typedef struct D3DXMATRIX : public D3DMATRIX
{
    D3DXMATRIX();
    D3DXMATRIX(CONST FLOAT *pf);
    D3DXMATRIX(CONST D3DMATRIX& mat);
    D3DXMATRIX(FLOAT f11, FLOAT f12, FLOAT f13, FLOAT f14,
               FLOAT f21, FLOAT f22, FLOAT f23, FLOAT f24,
               FLOAT f31, FLOAT f32, FLOAT f33, FLOAT f34,
               FLOAT f41, FLOAT f42, FLOAT f43, FLOAT f44);

    FLOAT& operator () (UINT row, UINT col);
    FLOAT operator () (UINT row, UINT col) const;

    operator FLOAT* ();
    operator CONST FLOAT* () const;

    D3DXMATRIX& operator *= (CONST D3DXMATRIX&);
    D3DXMATRIX& operator += (CONST D3DXMATRIX&);
    D3DXMATRIX& operator -= (CONST D3DXMATRIX&);
    D3DXMATRIX& operator *= (FLOAT);
    D3DXMATRIX& operator /= (FLOAT);

    D3DXMATRIX operator + () const;
    D3DXMATRIX operator - () const;

    D3DXMATRIX operator * (CONST D3DXMATRIX&) const;
    D3DXMATRIX operator + (CONST D3DXMATRIX&) const;
    D3DXMATRIX operator - (CONST D3DXMATRIX&) const;
    D3DXMATRIX operator * (FLOAT) const;
    D3DXMATRIX operator / (FLOAT) const;

    friend D3DXMATRIX operator * (FLOAT, CONST D3DXMATRIX&);

    BOOL operator == (CONST D3DXMATRIX&) const;
    BOOL operator != (CONST D3DXMATRIX&) const;
} D3DXMATRIX, *LPD3DXMATRIX;
#else /* !__cplusplus */
typedef struct _D3DMATRIX D3DXMATRIX, *LPD3DXMATRIX;
#endif /* !__cplusplus */

typedef struct D3DXQUATERNION
{
#ifdef __cplusplus
    D3DXQUATERNION();
    D3DXQUATERNION(CONST FLOAT *pf);
    D3DXQUATERNION(FLOAT fx, FLOAT fy, FLOAT fz, FLOAT fw);

    operator FLOAT* ();
    operator CONST FLOAT* () const;

    D3DXQUATERNION& operator += (CONST D3DXQUATERNION&);
    D3DXQUATERNION& operator -= (CONST D3DXQUATERNION&);
    D3DXQUATERNION& operator *= (CONST D3DXQUATERNION&);
    D3DXQUATERNION& operator *= (FLOAT);
    D3DXQUATERNION& operator /= (FLOAT);

    D3DXQUATERNION  operator + () const;
    D3DXQUATERNION  operator - () const;

    D3DXQUATERNION operator + (CONST D3DXQUATERNION&) const;
    D3DXQUATERNION operator - (CONST D3DXQUATERNION&) const;
    D3DXQUATERNION operator * (CONST D3DXQUATERNION&) const;
    D3DXQUATERNION operator * (FLOAT) const;
    D3DXQUATERNION operator / (FLOAT) const;

    friend D3DXQUATERNION operator * (FLOAT, CONST D3DXQUATERNION&);

    BOOL operator == (CONST D3DXQUATERNION&) const;
    BOOL operator != (CONST D3DXQUATERNION&) const;
#endif /* __cplusplus */
    FLOAT x, y, z, w;
} D3DXQUATERNION, *LPD3DXQUATERNION;

typedef struct D3DXPLANE
{
#ifdef __cplusplus
    D3DXPLANE();
    D3DXPLANE(CONST FLOAT *pf);
    D3DXPLANE(FLOAT fa, FLOAT fb, FLOAT fc, FLOAT fd);

    operator FLOAT* ();
    operator CONST FLOAT* () const;

    D3DXPLANE operator + () const;
    D3DXPLANE operator - () const;

    BOOL operator == (CONST D3DXPLANE&) const;
    BOOL operator != (CONST D3DXPLANE&) const;
#endif /* __cplusplus */
    FLOAT a, b, c, d;
} D3DXPLANE, *LPD3DXPLANE;

typedef struct D3DXCOLOR
{
#ifdef __cplusplus
    D3DXCOLOR();
    D3DXCOLOR(DWORD col);
    D3DXCOLOR(CONST FLOAT *pf);
    D3DXCOLOR(CONST D3DCOLORVALUE& col);
    D3DXCOLOR(FLOAT fr, FLOAT fg, FLOAT fb, FLOAT fa);

    operator DWORD () const;

    operator FLOAT* ();
    operator CONST FLOAT* () const;

    operator D3DCOLORVALUE* ();
    operator CONST D3DCOLORVALUE* () const;

    operator D3DCOLORVALUE& ();
    operator CONST D3DCOLORVALUE& () const;

    D3DXCOLOR& operator += (CONST D3DXCOLOR&);
    D3DXCOLOR& operator -= (CONST D3DXCOLOR&);
    D3DXCOLOR& operator *= (FLOAT);
    D3DXCOLOR& operator /= (FLOAT);

    D3DXCOLOR operator + () const;
    D3DXCOLOR operator - () const;

    D3DXCOLOR operator + (CONST D3DXCOLOR&) const;
    D3DXCOLOR operator - (CONST D3DXCOLOR&) const;
    D3DXCOLOR operator * (FLOAT) const;
    D3DXCOLOR operator / (FLOAT) const;

    friend D3DXCOLOR operator * (FLOAT, CONST D3DXCOLOR&);

    BOOL operator == (CONST D3DXCOLOR&) const;
    BOOL operator != (CONST D3DXCOLOR&) const;
#endif /* __cplusplus */
    FLOAT r, g, b, a;
} D3DXCOLOR, *LPD3DXCOLOR;

#ifdef __cplusplus
extern "C" {
#endif

D3DXCOLOR* WINAPI D3DXColorAdjustContrast(D3DXCOLOR *pout, CONST D3DXCOLOR *pc, FLOAT s);
D3DXCOLOR* WINAPI D3DXColorAdjustSaturation(D3DXCOLOR *pout, CONST D3DXCOLOR *pc, FLOAT s);

FLOAT WINAPI D3DXFresnelTerm(FLOAT costheta, FLOAT refractionindex);

D3DXMATRIX* WINAPI D3DXMatrixAffineTransformation(D3DXMATRIX *pout, FLOAT scaling, CONST D3DXVECTOR3 *rotationcenter, CONST D3DXQUATERNION *rotation, CONST D3DXVECTOR3 *translation);
FLOAT WINAPI D3DXMatrixfDeterminant(CONST D3DXMATRIX *pm);
D3DXMATRIX* WINAPI D3DXMatrixInverse(D3DXMATRIX *pout, FLOAT *pdeterminant, CONST D3DXMATRIX *pm);
D3DXMATRIX* WINAPI D3DXMatrixLookAtLH(D3DXMATRIX *pout, CONST D3DXVECTOR3 *peye, CONST D3DXVECTOR3 *pat, CONST D3DXVECTOR3 *pup);
D3DXMATRIX* WINAPI D3DXMatrixLookAtRH(D3DXMATRIX *pout, CONST D3DXVECTOR3 *peye, CONST D3DXVECTOR3 *pat, CONST D3DXVECTOR3 *pup);
D3DXMATRIX* WINAPI D3DXMatrixMultiply(D3DXMATRIX *pout, CONST D3DXMATRIX *pm1, CONST D3DXMATRIX *pm2);
D3DXMATRIX* WINAPI D3DXMatrixMultiplyTranspose(D3DXMATRIX *pout, CONST D3DXMATRIX *pm1, CONST D3DXMATRIX *pm2);
D3DXMATRIX* WINAPI D3DXMatrixOrthoLH(D3DXMATRIX *pout, FLOAT w, FLOAT h, FLOAT zn, FLOAT zf);
D3DXMATRIX* WINAPI D3DXMatrixOrthoOffCenterLH(D3DXMATRIX *pout, FLOAT l, FLOAT r, FLOAT b, FLOAT t, FLOAT zn, FLOAT zf);
D3DXMATRIX* WINAPI D3DXMatrixOrthoOffCenterRH(D3DXMATRIX *pout, FLOAT l, FLOAT r, FLOAT b, FLOAT t, FLOAT zn, FLOAT zf);
D3DXMATRIX* WINAPI D3DXMatrixOrthoLH(D3DXMATRIX *pout, FLOAT w, FLOAT h, FLOAT zn, FLOAT zf);
D3DXMATRIX* WINAPI D3DXMatrixOrthoRH(D3DXMATRIX *pout, FLOAT w, FLOAT h, FLOAT zn, FLOAT zf);
D3DXMATRIX* WINAPI D3DXMatrixPerspectiveFovLH(D3DXMATRIX *pout, FLOAT fovy, FLOAT aspect, FLOAT zn, FLOAT zf);
D3DXMATRIX* WINAPI D3DXMatrixPerspectiveFovRH(D3DXMATRIX *pout, FLOAT fovy, FLOAT aspect, FLOAT zn, FLOAT zf);
D3DXMATRIX* WINAPI D3DXMatrixPerspectiveLH(D3DXMATRIX *pout, FLOAT w, FLOAT h, FLOAT zn, FLOAT zf);
D3DXMATRIX* WINAPI D3DXMatrixPerspectiveOffCenterLH(D3DXMATRIX *pout, FLOAT l, FLOAT r, FLOAT b, FLOAT t, FLOAT zn, FLOAT zf);
D3DXMATRIX* WINAPI D3DXMatrixPerspectiveOffCenterRH(D3DXMATRIX *pout, FLOAT l, FLOAT r, FLOAT b, FLOAT t, FLOAT zn, FLOAT zf);
D3DXMATRIX* WINAPI D3DXMatrixPerspectiveRH(D3DXMATRIX *pout, FLOAT w, FLOAT h, FLOAT zn, FLOAT zf);
D3DXMATRIX* WINAPI D3DXMatrixReflect(D3DXMATRIX *pout, CONST D3DXPLANE *pplane);
D3DXMATRIX* WINAPI D3DXMatrixRotationAxis(D3DXMATRIX *pout, CONST D3DXVECTOR3 *pv, FLOAT angle);
D3DXMATRIX* WINAPI D3DXMatrixRotationQuaternion(D3DXMATRIX *pout, CONST D3DXQUATERNION *pq);
D3DXMATRIX* WINAPI D3DXMatrixRotationX(D3DXMATRIX *pout, FLOAT angle);
D3DXMATRIX* WINAPI D3DXMatrixRotationY(D3DXMATRIX *pout, FLOAT angle);
D3DXMATRIX* WINAPI D3DXMatrixRotationYawPitchRoll(D3DXMATRIX *pout, FLOAT yaw, FLOAT pitch, FLOAT roll);
D3DXMATRIX* WINAPI D3DXMatrixRotationZ(D3DXMATRIX *pout, FLOAT angle);
D3DXMATRIX* WINAPI D3DXMatrixScaling(D3DXMATRIX *pout, FLOAT sx, FLOAT sy, FLOAT sz);
D3DXMATRIX* WINAPI D3DXMatrixShadow(D3DXMATRIX *pout, CONST D3DXVECTOR4 *plight, CONST D3DXPLANE *pPlane);
D3DXMATRIX* WINAPI D3DXMatrixTransformation(D3DXMATRIX *pout, CONST D3DXVECTOR3 *pscalingcenter, CONST D3DXQUATERNION *pscalingrotation, CONST D3DXVECTOR3 *pscaling, CONST D3DXVECTOR3 *protationcenter, CONST D3DXQUATERNION *protation, CONST D3DXVECTOR3 *ptranslation);
D3DXMATRIX* WINAPI D3DXMatrixTranslation(D3DXMATRIX *pout, FLOAT x, FLOAT y, FLOAT z);
D3DXMATRIX* WINAPI D3DXMatrixTranspose(D3DXMATRIX *pout, CONST D3DXMATRIX *pm);

D3DXPLANE* WINAPI D3DXPlaneFromPointNormal(D3DXPLANE *pout, CONST D3DXVECTOR3 *pvpoint, CONST D3DXVECTOR3 *pvnormal);
D3DXPLANE* WINAPI D3DXPlaneFromPoints(D3DXPLANE *pout, CONST D3DXVECTOR3 *pv1, CONST D3DXVECTOR3 *pv2, CONST D3DXVECTOR3 *pv3);
D3DXVECTOR3* WINAPI D3DXPlaneIntersectLine(D3DXVECTOR3 *pout, CONST D3DXPLANE *pp, CONST D3DXVECTOR3 *pv1, CONST D3DXVECTOR3 *pv2);
D3DXPLANE* WINAPI D3DXPlaneNormalize(D3DXPLANE *pout, CONST D3DXPLANE *pp);
D3DXPLANE* WINAPI D3DXPlaneTransform(D3DXPLANE *pout, CONST D3DXPLANE *pplane, CONST D3DXMATRIX *pm);

D3DXQUATERNION* WINAPI D3DXQuaternionBaryCentric(D3DXQUATERNION *pout, CONST D3DXQUATERNION *pq1, CONST D3DXQUATERNION *pq2, CONST D3DXQUATERNION *pq3, FLOAT f, FLOAT g);
D3DXQUATERNION* WINAPI D3DXQuaternionExp(D3DXQUATERNION *pout, CONST D3DXQUATERNION *pq);
D3DXQUATERNION* WINAPI D3DXQuaternionInverse(D3DXQUATERNION *pout, CONST D3DXQUATERNION *pq);
D3DXQUATERNION* WINAPI D3DXQuaternionLn(D3DXQUATERNION *pout, CONST D3DXQUATERNION *pq);
D3DXQUATERNION* WINAPI D3DXQuaternionMultiply(D3DXQUATERNION *pout, CONST D3DXQUATERNION *pq1, CONST D3DXQUATERNION *pq2);
D3DXQUATERNION* WINAPI D3DXQuaternionNormalize(D3DXQUATERNION *pout, CONST D3DXQUATERNION *pq);
D3DXQUATERNION* WINAPI D3DXQuaternionRotationAxis(D3DXQUATERNION *pout, CONST D3DXVECTOR3 *pv, FLOAT angle);
D3DXQUATERNION* WINAPI D3DXQuaternionRotationMatrix(D3DXQUATERNION *pout, CONST D3DXMATRIX *pm);
D3DXQUATERNION* WINAPI D3DXQuaternionRotationYawPitchRoll(D3DXQUATERNION *pout, FLOAT yaw, FLOAT pitch, FLOAT roll);
D3DXQUATERNION* WINAPI D3DXQuaternionSlerp(D3DXQUATERNION *pout, CONST D3DXQUATERNION *pq1, CONST D3DXQUATERNION *pq2, FLOAT t);
D3DXQUATERNION* WINAPI D3DXQuaternionSquad(D3DXQUATERNION *pout, CONST D3DXQUATERNION *pq1, CONST D3DXQUATERNION *pq2, CONST D3DXQUATERNION *pq3, CONST D3DXQUATERNION *pq4, FLOAT t);
void WINAPI D3DXQuaternionToAxisAngle(CONST D3DXQUATERNION *pq, D3DXVECTOR3 *paxis, FLOAT *pangle);

D3DXVECTOR2* WINAPI D3DXVec2BaryCentric(D3DXVECTOR2 *pout, CONST D3DXVECTOR2 *pv1, CONST D3DXVECTOR2 *pv2, CONST D3DXVECTOR2 *pv3, FLOAT f, FLOAT g);
D3DXVECTOR2* WINAPI D3DXVec2CatmullRom(D3DXVECTOR2 *pout, CONST D3DXVECTOR2 *pv0, CONST D3DXVECTOR2 *pv1, CONST D3DXVECTOR2 *pv2, CONST D3DXVECTOR2 *pv3, FLOAT s);
D3DXVECTOR2* WINAPI D3DXVec2Hermite(D3DXVECTOR2 *pout, CONST D3DXVECTOR2 *pv1, CONST D3DXVECTOR2 *pt1, CONST D3DXVECTOR2 *pv2, CONST D3DXVECTOR2 *pt2, FLOAT s);
D3DXVECTOR2* WINAPI D3DXVec2Normalize(D3DXVECTOR2 *pout, CONST D3DXVECTOR2 *pv);
D3DXVECTOR4* WINAPI D3DXVec2Transform(D3DXVECTOR4 *pout, CONST D3DXVECTOR2 *pv, CONST D3DXMATRIX *pm);
D3DXVECTOR2* WINAPI D3DXVec2TransformCoord(D3DXVECTOR2 *pout, CONST D3DXVECTOR2 *pv, CONST D3DXMATRIX *pm);
D3DXVECTOR2* WINAPI D3DXVec2TransformNormal(D3DXVECTOR2 *pout, CONST D3DXVECTOR2 *pv, CONST D3DXMATRIX *pm);

D3DXVECTOR3* WINAPI D3DXVec3BaryCentric(D3DXVECTOR3 *pout, CONST D3DXVECTOR3 *pv1, CONST D3DXVECTOR3 *pv2, CONST D3DXVECTOR3 *pv3, FLOAT f, FLOAT g);
D3DXVECTOR3* WINAPI D3DXVec3CatmullRom( D3DXVECTOR3 *pout, CONST D3DXVECTOR3 *pv0, CONST D3DXVECTOR3 *pv1, CONST D3DXVECTOR3 *pv2, CONST D3DXVECTOR3 *pv3, FLOAT s);
D3DXVECTOR3* WINAPI D3DXVec3Hermite(D3DXVECTOR3 *pout, CONST D3DXVECTOR3 *pv1, CONST D3DXVECTOR3 *pt1, CONST D3DXVECTOR3 *pv2, CONST D3DXVECTOR3 *pt2, FLOAT s);
D3DXVECTOR3* WINAPI D3DXVec3Normalize(D3DXVECTOR3 *pout, CONST D3DXVECTOR3 *pv);
D3DXVECTOR3* WINAPI D3DXVec3Project(D3DXVECTOR3 *pout, CONST D3DXVECTOR3 *pv, CONST D3DVIEWPORT8 *pviewport, CONST D3DXMATRIX *pprojection, CONST D3DXMATRIX *pview, CONST D3DXMATRIX *pworld);
D3DXVECTOR4* WINAPI D3DXVec3Transform(D3DXVECTOR4 *pout, CONST D3DXVECTOR3 *pv, CONST D3DXMATRIX *pm);
D3DXVECTOR3* WINAPI D3DXVec3TransformCoord(D3DXVECTOR3 *pout, CONST D3DXVECTOR3 *pv, CONST D3DXMATRIX *pm);
D3DXVECTOR3* WINAPI D3DXVec3TransformNormal(D3DXVECTOR3 *pout, CONST D3DXVECTOR3 *pv, CONST D3DXMATRIX *pm);
D3DXVECTOR3* WINAPI D3DXVec3Unproject(D3DXVECTOR3 *pout, CONST D3DXVECTOR3 *pv, CONST D3DVIEWPORT8 *pviewport, CONST D3DXMATRIX *pprojection, CONST D3DXMATRIX *pview, CONST D3DXMATRIX *pworld);

D3DXVECTOR4* WINAPI D3DXVec4BaryCentric(D3DXVECTOR4 *pout, CONST D3DXVECTOR4 *pv1, CONST D3DXVECTOR4 *pv2, CONST D3DXVECTOR4 *pv3, FLOAT f, FLOAT g);
D3DXVECTOR4* WINAPI D3DXVec4CatmullRom(D3DXVECTOR4 *pout, CONST D3DXVECTOR4 *pv0, CONST D3DXVECTOR4 *pv1, CONST D3DXVECTOR4 *pv2, CONST D3DXVECTOR4 *pv3, FLOAT s);
D3DXVECTOR4* WINAPI D3DXVec4Cross(D3DXVECTOR4 *pout, CONST D3DXVECTOR4 *pv1, CONST D3DXVECTOR4 *pv2, CONST D3DXVECTOR4 *pv3);
D3DXVECTOR4* WINAPI D3DXVec4Hermite(D3DXVECTOR4 *pout, CONST D3DXVECTOR4 *pv1, CONST D3DXVECTOR4 *pt1, CONST D3DXVECTOR4 *pv2, CONST D3DXVECTOR4 *pt2, FLOAT s);
D3DXVECTOR4* WINAPI D3DXVec4Normalize(D3DXVECTOR4 *pout, CONST D3DXVECTOR4 *pv);
D3DXVECTOR4* WINAPI D3DXVec4Transform(D3DXVECTOR4 *pout, CONST D3DXVECTOR4 *pv, CONST D3DXMATRIX *pm);

#ifdef __cplusplus
}
#endif

#define INTERFACE ID3DXMatrixStack
DECLARE_INTERFACE_(ID3DXMatrixStack, IUnknown)
{
    STDMETHOD_(HRESULT,QueryInterface)(THIS_ REFIID, LPVOID*) PURE;
    STDMETHOD_(ULONG,AddRef)(THIS) PURE;
    STDMETHOD_(ULONG,Release)(THIS) PURE;
    STDMETHOD(Pop)(THIS) PURE;
    STDMETHOD(Push)(THIS) PURE;
    STDMETHOD(LoadIdentity)(THIS) PURE;
    STDMETHOD(LoadMatrix)(THIS_ CONST D3DXMATRIX *) PURE;
    STDMETHOD(MultMatrix)(THIS_ CONST D3DXMATRIX *) PURE;
    STDMETHOD(MultMatrixLocal)(THIS_ CONST D3DXMATRIX *) PURE;
    STDMETHOD(RotateAxis)(THIS_ CONST D3DXVECTOR3 *, FLOAT) PURE;
    STDMETHOD(RotateAxisLocal)(THIS_ CONST D3DXVECTOR3 *, FLOAT) PURE;
    STDMETHOD(RotateYawPitchRoll)(THIS_ FLOAT, FLOAT, FLOAT) PURE;
    STDMETHOD(RotateYawPitchRollLocal)(THIS_ FLOAT, FLOAT, FLOAT) PURE;
    STDMETHOD(Scale)(THIS_ FLOAT, FLOAT, FLOAT) PURE;
    STDMETHOD(ScaleLocal)(THIS_ FLOAT, FLOAT, FLOAT) PURE;
    STDMETHOD(Translate)(THIS_ FLOAT, FLOAT, FLOAT) PURE;
    STDMETHOD(TranslateLocal)(THIS_ FLOAT, FLOAT, FLOAT) PURE;
    STDMETHOD_(LPD3DXMATRIX, GetTop)(THIS) PURE;
};

#undef INTERFACE

#if !defined(__cplusplus) || defined(CINTERFACE)

#define ID3DXMatrixStack_QueryInterface(p,a,b)            (p)->lpVtbl->QueryInterface(p,a,b)
#define ID3DXMatrixStack_AddRef(p)                        (p)->lpVtbl->AddRef(p)
#define ID3DXMatrixStack_Release(p)                       (p)->lpVtbl->Release(p)
#define ID3DXMatrixStack_Pop(p)                           (p)->lpVtbl->Pop(p)
#define ID3DXMatrixStack_Push(p)                          (p)->lpVtbl->Push(p)
#define ID3DXMatrixStack_LoadIdentity(p)                  (p)->lpVtbl->LoadIdentity(p)
#define ID3DXMatrixStack_LoadMatrix(p,a)                  (p)->lpVtbl->LoadMatrix(p,a)
#define ID3DXMatrixStack_MultMatrix(p,a)                  (p)->lpVtbl->MultMatrix(p,a)
#define ID3DXMatrixStack_MultMatrixLocal(p,a)             (p)->lpVtbl->MultMatrixLocal(p,a)
#define ID3DXMatrixStack_RotateAxis(p,a,b)                (p)->lpVtbl->RotateAxis(p,a,b)
#define ID3DXMatrixStack_RotateAxisLocal(p,a,b)           (p)->lpVtbl->RotateAxisLocal(p,a,b)
#define ID3DXMatrixStack_RotateYawPitchRoll(p,a,b,c)      (p)->lpVtbl->RotateYawPitchRoll(p,a,b,c)
#define ID3DXMatrixStack_RotateYawPitchRollLocal(p,a,b,c) (p)->lpVtbl->RotateYawPitchRollLocal(p,a,b,c)
#define ID3DXMatrixStack_Scale(p,a,b,c)                   (p)->lpVtbl->Scale(p,a,b,c)
#define ID3DXMatrixStack_ScaleLocal(p,a,b,c)              (p)->lpVtbl->ScaleLocal(p,a,b,c)
#define ID3DXMatrixStack_Translate(p,a,b,c)               (p)->lpVtbl->Translate(p,a,b,c)
#define ID3DXMatrixStack_TranslateLocal(p,a,b,c)          (p)->lpVtbl->TranslateLocal(p,a,b,c)
#define ID3DXMatrixStack_GetTop(p)                        (p)->lpVtbl->GetTop(p)

#endif

#ifdef __cplusplus
extern "C" {
#endif

HRESULT WINAPI D3DXCreateMatrixStack(DWORD flags, LPD3DXMATRIXSTACK* ppstack);

#ifdef __cplusplus
}
#endif

#include <d3dx8math.inl>

#endif /* __D3DX8MATH_H__ */