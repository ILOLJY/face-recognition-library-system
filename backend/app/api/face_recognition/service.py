"""人脸识别服务模块"""
import os
import cv2
import numpy as np
from typing import List, Optional, Tuple
from datetime import datetime

try:
    import insightface
    from insightface.app import FaceAnalysis
    HAS_INSIGHTFACE = True
except ImportError:
    HAS_INSIGHTFACE = False
    FaceAnalysis = None


class FaceRecognitionService:
    """人脸识别服务"""
    
    _instance = None
    _face_analyzer = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FaceRecognitionService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if HAS_INSIGHTFACE and self._face_analyzer is None:
            self._initialize_analyzer()
    
    def _initialize_analyzer(self):
        """初始化 InsightFace 分析器"""
        try:
            # 使用 Buffalo_L 模型，提供更准确的人脸检测和识别
            self._face_analyzer = FaceAnalysis(name='buffalo_l')
            # 准备模型，ctx_id=-1 表示使用 CPU，det_size=(640, 640) 提高检测分辨率
            self._face_analyzer.prepare(ctx_id=-1, det_size=(640, 640))
        except Exception as e:
            print(f"初始化 InsightFace 失败: {e}")
            self._face_analyzer = None
    
    def get_face_analyzer(self) -> FaceAnalysis:
        """获取人脸分析器"""
        if not HAS_INSIGHTFACE:
            raise RuntimeError("InsightFace 库未安装")
        
        if self._face_analyzer is None:
            self._initialize_analyzer()
            if self._face_analyzer is None:
                raise RuntimeError("人脸分析器初始化失败")
        
        return self._face_analyzer
    
    def verify_face_image(self, image_data: bytes) -> np.ndarray:
        """验证并转换图片数据为 OpenCV 格式
        
        Args:
            image_data: 图片字节数据
            
        Returns:
            np.ndarray: OpenCV 格式的图片
            
        Raises:
            ValueError: 图片验证失败
        """
        try:
            # 将字节数据转换为 numpy 数组
            nparr = np.frombuffer(image_data, np.uint8)
            # 使用 OpenCV 解码图片
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image is None:
                raise ValueError("无法解码图片，请检查文件格式")
            
            return image
        except Exception as e:
            raise ValueError(f"图片处理失败: {str(e)}")
    
    def detect_and_extract_face(self, image: np.ndarray) -> Tuple[List[float], List, Optional[List]]:
        """检测并提取人脸特征
        
        Args:
            image: OpenCV 格式的图片
            
        Returns:
            Tuple[List[float], List, Optional[List]]: 
                人脸特征向量、边界框、关键点
                
        Raises:
            ValueError: 未检测到人脸或检测失败
        """
        analyzer = self.get_face_analyzer()
        
        try:
            # 检测人脸
            faces = analyzer.get(image)
            
            if len(faces) == 0:
                raise ValueError("未检测到人脸，请确保图片中包含清晰的人脸")
            
            # 如果检测到多个人脸，选择最大的人脸（通常为主要人脸）
            if len(faces) > 1:
                # 按人脸区域大小排序（正确计算面积：width * height）
                faces.sort(
                    key=lambda x: (x.bbox[2] - x.bbox[0]) * (x.bbox[3] - x.bbox[1]),
                    reverse=True
                )
            
            # 获取主要人脸
            main_face = faces[0]
            
            # 获取人脸特征向量（embedding）
            embedding = main_face.embedding
            
            # 归一化特征向量（确保相似度计算更稳定）
            embedding_norm = np.linalg.norm(embedding)
            if embedding_norm > 0:
                embedding = embedding / embedding_norm
            
            # 转换为一维列表
            embedding_list = embedding.tolist()
            
            # 获取人脸边界框 [x1, y1, x2, y2]
            bbox = main_face.bbox.tolist() if hasattr(main_face.bbox, 'tolist') else main_face.bbox
            
            # 获取人脸关键点（5个点，每点[x, y]）
            landmarks = None
            if hasattr(main_face, 'kps') and main_face.kps is not None:
                landmarks = main_face.kps.tolist() if hasattr(main_face.kps, 'tolist') else main_face.kps
            
            return embedding_list, bbox, landmarks
            
        except ValueError:
            raise
        except Exception as e:
            raise ValueError(f"人脸特征提取失败: {str(e)}")
    
    def crop_and_save_face_image(self, image: np.ndarray, user_id: int, 
                               bbox: Optional[List] = None) -> Optional[str]:
        """裁剪并保存人脸图片
        
        Args:
            image: 原始图片
            user_id: 用户ID
            bbox: 人脸边界框 [x1, y1, x2, y2]
            
        Returns:
            Optional[str]: 保存的图片路径，失败时返回 None
        """
        try:
            # 确保上传目录存在
            upload_dir = "app/static/faces"
            os.makedirs(upload_dir, exist_ok=True)
            
            # 生成文件名（使用utcnow避免时区问题）
            timestamp = int(datetime.utcnow().timestamp())
            filename = f"face_{user_id}_{timestamp}.jpg"
            file_path = os.path.join(upload_dir, filename)
            
            save_image = image
            
            # 如果有边界框，裁剪人脸区域
            if bbox and len(bbox) >= 4:
                # 转换边界框为整数
                x1, y1, x2, y2 = map(int, bbox)
                
                # 确保坐标在图片范围内
                h, w = image.shape[:2]
                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(w, x2), min(h, y2)
                
                if x2 > x1 and y2 > y1:
                    # 裁剪人脸区域
                    face_image = image[y1:y2, x1:x2]
                    
                    # 可以调整人脸图片大小（可选）
                    # max_size = 512
                    # h_face, w_face = face_image.shape[:2]
                    # if h_face > max_size or w_face > max_size:
                    #     scale = max_size / max(h_face, w_face)
                    #     new_h, new_w = int(h_face * scale), int(w_face * scale)
                    #     face_image = cv2.resize(face_image, (new_w, new_h))
                    
                    save_image = face_image
            
            # 保存图片（质量设置）
            cv2.imwrite(file_path, save_image, [cv2.IMWRITE_JPEG_QUALITY, 95])
            
            # 验证图片是否保存成功
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                return f"/static/faces/{filename}"
            else:
                return None
                
        except Exception as e:
            print(f"保存人脸图片失败: {e}")
            return None
    
    def validate_embedding(self, embedding: List[float]) -> bool:
        """验证人脸特征向量
        
        Args:
            embedding: 人脸特征向量
            
        Returns:
            bool: 是否有效
        """
        if not isinstance(embedding, list):
            return False
        
        # 检查向量长度（InsightFace 通常生成512维向量）
        if len(embedding) not in [256, 512, 1024]:  # 常见的人脸特征维度
            return False
        
        # 检查向量值是否合理
        if not all(isinstance(val, (int, float)) for val in embedding):
            return False
        
        # 检查向量是否全为零（无效向量）
        if all(abs(val) < 1e-10 for val in embedding):
            return False
        
        return True
    
    def compute_face_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """计算两个人脸特征的相似度
        
        Args:
            embedding1: 第一个人脸特征向量
            embedding2: 第二个人脸特征向量
            
        Returns:
            float: 余弦相似度得分 (范围 [-1, 1]，越高越相似)
        """
        if len(embedding1) != len(embedding2):
            raise ValueError("特征向量维度不匹配")
        
        # 转换为 numpy 数组
        vec1 = np.array(embedding1, dtype=np.float32)
        vec2 = np.array(embedding2, dtype=np.float32)
        
        # 归一化
        vec1_norm = vec1 / np.linalg.norm(vec1)
        vec2_norm = vec2 / np.linalg.norm(vec2)
        
        # 计算余弦相似度（范围在 [-1, 1] 之间）
        similarity = np.dot(vec1_norm, vec2_norm)
        
        return float(similarity)
    
    def is_same_person(self, embedding1: List[float], embedding2: List[float], threshold: float = 0.5) -> bool:
        """判断两个人脸是否为同一个人
        
        Args:
            embedding1: 第一个人脸特征向量
            embedding2: 第二个人脸特征向量
            threshold: 判断阈值（建议值 0.5-0.7）
            
        Returns:
            bool: 是否为同一个人
        """
        similarity = self.compute_face_similarity(embedding1, embedding2)
        return similarity > threshold


# 全局单例实例
face_recognition_service: Optional[FaceRecognitionService] = None


def get_face_recognition_service() -> FaceRecognitionService:
    """获取人脸识别服务实例"""
    global face_recognition_service
    
    if face_recognition_service is None:
        face_recognition_service = FaceRecognitionService()
    
    return face_recognition_service