import sys
import traceback


def custom_exception_hook(exc_type, exc_value, exc_traceback):
    """
    这是一个自定义的异常钩子函数，用于捕获所有未处理的异常。
    """

    # --- 1. 记录/处理异常信息 ---
    print("=" * 60)
    print("🚨 捕获到一个未处理的异常！")
    print(f"异常类型: {exc_type.__name__}")
    print(f"异常信息: {exc_value}")

    formatted_traceback_lines = traceback.format_exception(
        exc_type, exc_value, exc_traceback
    )

    print("\n--- 完整追溯信息 (格式化为字符串) ---")
    # 将列表中的行连接成一个完整的字符串
    full_traceback_string = "".join(formatted_traceback_lines)
    print(full_traceback_string)

    # 也可以将信息写入日志文件
    # logging.error("未处理的致命错误:", exc_info=(exc_type, exc_value, exc_traceback))

    # --- 2. 可选：执行清理工作或优雅退出 ---
    # 例如：关闭数据库连接、保存临时文件等。

    print("=" * 60)


# 将系统的异常钩子设置为我们的自定义函数
sys.excepthook = custom_exception_hook


# --- 演示代码 ---

def protected_function():
    try:
        # 这个内部 try/except 块捕获并处理了 NameError
        a = 1 / 0  # 制造一个 ZeroDivisionError
    except ZeroDivisionError:
        print("✅ 内部 try/except 成功捕获并处理了 ZeroDivisionError。")
    finally:
        # 这里故意抛出一个不会被内部 try/except 捕获的异常
        # 它将逃逸到主程序，并最终被 sys.excepthook 捕获。
        print(unknown_variable)  # 制造一个 NameError


def main_code():
    print("程序开始运行...")
    protected_function()
    print("程序理论上不会运行到这里（因为前面抛出了未捕获的异常）。")


# 运行主代码
main_code()