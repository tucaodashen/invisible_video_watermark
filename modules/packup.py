import datetime
import os
import zipfile
from typing import Optional, List


def pack_files_to_zip(
        file_paths: List[str],
        output_dir: str,
        zip_name: Optional[str] = None,
        preserve_structure: bool = False
) -> str:
    """
    将多个文件打包为ZIP压缩文件

    Args:
        file_paths: 要压缩的文件路径列表
        output_dir: 输出目录
        zip_name: ZIP文件名（可选，默认为当前时间戳）
        preserve_structure: 是否保留原文件目录结构（默认不保留）

    Returns:
        生成的ZIP文件完整路径

    Raises:
        FileNotFoundError: 当输入文件或输出目录不存在时
        ValueError: 当文件路径列表为空时
    """

    # 输入验证
    if not file_paths:
        raise ValueError("文件路径列表不能为空")

    if not os.path.exists(output_dir):
        raise FileNotFoundError(f"输出目录不存在: {output_dir}")

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 设置ZIP文件名
    if zip_name is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_name = f"archive_{timestamp}.zip"
    elif not zip_name.endswith('.zip'):
        zip_name += '.zip'

    # 完整输出路径
    zip_path = os.path.join(output_dir, zip_name)

    # 验证所有输入文件是否存在
    missing_files = []
    for file_path in file_paths:
        if not os.path.exists(file_path):
            missing_files.append(file_path)

    if missing_files:
        raise FileNotFoundError(f"以下文件不存在: {missing_files}")

    # 创建ZIP文件
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in file_paths:
            if preserve_structure:
                # 保留完整路径结构
                arcname = file_path
            else:
                # 只保留文件名
                arcname = os.path.basename(file_path)

            # 添加文件到ZIP
            zipf.write(file_path, arcname)

    return zip_path