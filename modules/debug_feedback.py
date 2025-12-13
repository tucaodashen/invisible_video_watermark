import rollbar
from BasicSystem import const


def report_error(error_frame):
    rollbar.init(const.rollbar_token, 'production', code_version='COMMIT_SHA')
    custom_payload = {
        # 包含手动堆栈信息
        'manual_stack_trace': [1,1,4,5,1,4],
        # 包含日志文件内容
        'full_log_file_content': [1,9,1,9,8,1,0]
    }

    # 4. 发送自定义消息到 Rollbar
    # 使用 'error' 级别，让它显示为错误事件
    rollbar.report_message(
        '关键日志和手动堆栈报告',
        'error',  #  级别
        extra_data=custom_payload  # 附加自定义数据
    )

    # 确保消息发送完成（如果使用异步发送）
    rollbar.wait()

if __name__ == '__main__':
    report_error([])
