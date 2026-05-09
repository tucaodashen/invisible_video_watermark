import rollbar
import coredumpy

from BasicSystem.log_client import setup_logger, get_logger

logger = get_logger("ErrorReport")



def process_data(data):
    """数据处理函数"""
    # 在松散模块中直接使用全局logger
    logger.info("Starting data processing")

    try:
        # 数据处理逻辑
        result = [item * 2 for item in data]
        logger.success(f"Processed {len(data)} items")
        return result
    except Exception as e:
        logger.error(f"Data processing failed: {str(e)}")
        raise

if __name__ == "__main__":
    data = [1, 2, 3, 4, 5]
    result = process_data(data)