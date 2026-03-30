"""人脸识别接口模块 - 简洁版本"""
import os
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field

from app.db.session import get_db
from app.api.auth.dependencies import get_current_user
from app.models.users import User
from app.models.face_data import FaceData
from app.api.face_recognition.service import get_face_recognition_service

# 创建人脸识别路由
router = APIRouter()


class FaceDataResponse(BaseModel):
    """人脸数据响应模型"""
    id: int
    user_id: int
    face_encoding: List[float]
    face_image_path: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class FaceUploadResponse(BaseModel):
    """人脸上传响应模型"""
    id: int
    user_id: int
    message: str
    face_image_path: str
    face_encoding_length: int


@router.post("/register", response_model=FaceUploadResponse, status_code=status.HTTP_200_OK)
async def register_face(
    file: UploadFile = File(..., description="人脸图片文件 (JPG/PNG, 最大5MB)"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """注册人脸
    
    用户上传人脸图片，系统提取人脸特征并保存到数据库
    
    流程：
    1. 读取并验证上传的图片
    2. 使用 InsightFace 检测人脸
    3. 提取人脸特征向量（embedding）
    4. 保存人脸图片到服务器
    5. 更新数据库中的用户人脸数据
    
    Args:
        file: 上传的人脸图片文件
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        FaceUploadResponse: 人脸注册响应
        
    Raises:
        HTTPException: 认证失败、文件无效、人脸检测失败等
    """
    # 检查文件类型
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请上传图片文件（支持 JPG、PNG 格式）"
        )
    
    # 检查文件大小（限制为 5MB）
    max_size = 5 * 1024 * 1024  # 5MB
    file.file.seek(0, 2)  # 移动到文件末尾
    file_size = file.file.tell()
    file.file.seek(0)  # 重置文件指针
    
    if file_size > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"图片文件大小不能超过 5MB，当前大小为 {file_size // 1024}KB"
        )
    
    # 读取文件内容
    try:
        contents = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"读取文件失败: {str(e)}"
        )
    
    # 获取人脸识别服务
    try:
        face_service = get_face_recognition_service()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"人脸识别服务初始化失败: {str(e)}"
        )
    
    try:
        # 验证并转换图片
        image = face_service.verify_face_image(contents)
        
        # 检测并提取人脸特征
        embedding_list, bbox, landmarks = face_service.detect_and_extract_face(image)
        
        # 裁剪并保存人脸图片
        face_image_path = face_service.crop_and_save_face_image(image, current_user.id, bbox)
        
        # 验证特征向量
        if not face_service.validate_embedding(embedding_list):
            raise ValueError("提取的人脸特征向量无效")
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"人脸处理失败: {str(e)}"
        )
    
    # 查询用户是否已有人脸数据
    result = await db.execute(
        select(FaceData).where(FaceData.user_id == current_user.id)
    )
    face_data = result.scalar()
    
    try:
        if face_data:
            # 更新现有记录
            face_data.face_encoding = embedding_list
            face_data.face_image_path = face_image_path
            face_data.updated_at = datetime.utcnow()
        else:
            # 创建新记录
            face_data = FaceData(
                user_id=current_user.id,
                face_encoding=embedding_list,
                face_image_path=face_image_path,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(face_data)
        
        await db.commit()
        await db.refresh(face_data)
        
        return FaceUploadResponse(
            id=face_data.id,
            user_id=face_data.user_id,
            message="人脸注册成功",
            face_image_path=face_image_path or "",
            face_encoding_length=len(embedding_list)
        )
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"保存人脸数据失败: {str(e)}"
        )


@router.get("/data", response_model=FaceDataResponse, status_code=status.HTTP_200_OK)
async def get_face_data(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取当前用户的人脸数据
    
    Args:
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        FaceDataResponse: 人脸数据响应
        
    Raises:
        HTTPException: 认证失败、未找到人脸数据等
    """
    result = await db.execute(
        select(FaceData).where(FaceData.user_id == current_user.id)
    )
    face_data = result.scalar()
    
    if not face_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="未找到人脸数据，请先注册人脸"
        )
    
    return face_data


@router.delete("/data", status_code=status.HTTP_200_OK)
async def delete_face_data(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除当前用户的人脸数据
    
    Args:
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        dict: 删除成功消息
        
    Raises:
        HTTPException: 认证失败、未找到人脸数据等
    """
    result = await db.execute(
        select(FaceData).where(FaceData.user_id == current_user.id)
    )
    face_data = result.scalar()
    
    if not face_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="未找到人脸数据"
        )
    
    try:
        # 删除人脸图片文件（如果存在）
        if face_data.face_image_path:
            # 移除开头的斜杠（如果有）
            img_path = face_data.face_image_path
            if img_path.startswith('/'):
                img_path = img_path[1:]
            
            # 构建完整路径
            full_path = os.path.join("app", img_path) if not img_path.startswith("app/") else img_path
            
            if os.path.exists(full_path):
                try:
                    os.remove(full_path)
                except Exception:
                    # 如果删除文件失败，继续执行数据库删除
                    pass
        
        # 删除数据库记录
        await db.delete(face_data)
        await db.commit()
        
        return {"message": "人脸数据删除成功"}
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除人脸数据失败: {str(e)}"
        )


@router.get("/verify", status_code=status.HTTP_200_OK)
async def verify_face_available():
    """验证人脸识别服务是否可用
    
    Returns:
        dict: 服务状态信息
    """
    try:
        face_service = get_face_recognition_service()
        return {
            "status": "available",
            "message": "人脸识别服务正常运行"
        }
    except Exception as e:
        return {
            "status": "unavailable",
            "message": f"人脸识别服务不可用: {str(e)}"
        }