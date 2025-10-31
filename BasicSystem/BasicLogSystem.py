import json
from loguru import logger
from typing import Dict, Any, Optional
from datetime import datetime


class CustomJSONLogger:
    def __init__(self, log_file: str = "app.log", rotation: str = "10 MB"):
        """
        初始化自定义JSON日志器

        Args:
            log_file: 日志文件路径
            rotation: 日志轮转设置
        """
        # 移除默认处理器
        logger.remove()

        # 自定义JSON格式化函数
        def json_format(record: Dict) -> str:
            """将日志记录格式化为JSON字符串"""
            # 正确处理时区信息
            if hasattr(record["time"], 'astimezone'):
                timestamp = record["time"].astimezone().isoformat()
            else:
                timestamp = record["time"].isoformat()

            log_entry = {
                "timestamp": timestamp,
                "level": record["level"].name,
                "message": record["message"],
                "module": record["module"],
                "function": record["function"],
                "line": record["line"]
            }

            # 添加自定义标签
            if "tags" in record["extra"] and record["extra"]["tags"]:
                log_entry["tags"] = record["extra"]["tags"]

            # 添加上下文信息
            if "context" in record["extra"] and record["extra"]["context"]:
                log_entry.update(record["extra"]["context"])

            return json.dumps(log_entry, ensure_ascii=False) + "\n"

        # 添加JSON格式的文件处理器
        logger.add(
            log_file,
            format=json_format,
            rotation=rotation,
            compression="zip",
            encoding="utf-8",
            serialize=False,  # 使用自定义序列化
            catch=False  # 禁用异常捕获，便于调试
        )

        # 添加控制台处理器（可选，非JSON格式）
        logger.add(
            lambda msg: print(msg, end=""),
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{module}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level> | tags: {extra[tags]}",
            colorize=True,
            level="INFO"
        )

    def log_with_tags(self, message: str, tags: Dict[str, Any] = None, **kwargs):
        """
        带标签的日志记录

        Args:
            message: 日志消息
            tags: 自定义标签字典
            kwargs: 额外的上下文信息
        """
        tags = tags or {}
        context = kwargs or {}

        # 绑定标签和上下文到日志记录
        with logger.contextualize(tags=tags, context=context):
            logger.info(message)


# 更简洁的版本（推荐）
class SimpleJSONLogger:
    """更简洁的JSON日志器"""

    def __init__(self, log_file: str = "app.log", rotation: str = "10 MB"):
        # 移除默认处理器
        logger.remove()

        # 文件处理器 - JSON格式
        logger.add(
            log_file,
            format=self._json_formatter,
            rotation=rotation,
            compression="zip",
            encoding="utf-8",
            level="INFO"
        )

        # 控制台处理器 - 可读格式
        logger.add(
            lambda msg: print(msg, end=""),
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level> | tags: {extra[tags]}",
            colorize=True,
            level="INFO"
        )

    def _json_formatter(self, record):
        """JSON格式化器"""
        # 处理时间戳
        time = record["time"]
        if hasattr(time, 'astimezone'):
            timestamp = time.astimezone().isoformat()
        else:
            timestamp = time.isoformat()

        # 构建基础日志条目
        log_entry = {
            "timestamp": timestamp,
            "level": record["level"].name,
            "message": record["message"],
            "logger": record["name"],
            "module": record["module"],
            "function": record["function"],
            "line": record["line"]
        }

        # 添加额外字段
        extra = record["extra"]
        if "tags" in extra and extra["tags"]:
            log_entry["tags"] = extra["tags"]

        # 添加其他额外字段（除了tags）
        for key, value in extra.items():
            if key != "tags" and value:
                log_entry[key] = value

        return json.dumps(log_entry, ensure_ascii=False)

    def info(self, message: str, **tags):
        """信息级别日志"""
        with logger.contextualize(tags=tags):
            logger.info(message)

    def debug(self, message: str, **tags):
        """调试级别日志"""
        with logger.contextualize(tags=tags):
            logger.debug(message)

    def warning(self, message: str, **tags):
        """警告级别日志"""
        with logger.contextualize(tags=tags):
            logger.warning(message)

    def error(self, message: str, **tags):
        """错误级别日志"""
        with logger.contextualize(tags=tags):
            logger.error(message)


# 使用示例
if __name__ == "__main__":
    # 使用更简洁的版本
    log = SimpleJSONLogger("my_app.log")

    # 基本使用
    log.info("用户登录成功", user_id=123, action="login", status="success")

    # 带复杂数据
    log.info(
        "订单创建",
        order_id="ORD001",
        type="purchase",
        amount=299.99,
        items_count=3
    )

    # 错误日志
    try:
        result = 1 / 0
    except Exception as e:
        log.error("计算错误", operation="division", dividend=1, divisor=0, error=str(e))

    # 调试日志
    log.debug("处理用户数据", user_count=150, processing_time=0.45)