# data_processor.py
from BasicSystem.NewLogSystem import get_module_logger

# 获取当前模块的日志记录器
logger = get_module_logger()


def process_data(data):
    """数据处理函数"""
    logger.info("Starting data processing")

    try:
        # 数据处理逻辑
        result = [item * 2 for item in data]
        logger.success(f"Processed {len(data)} items")
        return result
    except Exception as e:
        logger.error(f"Data processing failed: {str(e)}")
        raise