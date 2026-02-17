import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 定义权限范围
SCOPES = [
    'https://www.googleapis.com/auth/drive.file',        # 操作云盘
    'https://www.googleapis.com/auth/userinfo.profile', # 获取头像、昵称
    'openid'                                        # 获取唯一用户 ID
]


def get_gdrive_service():
    creds = None
    # token.json 存储用户的访问和刷新令牌
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # 如果没有有效的凭据，让用户登录
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # 保存凭据以备下次使用
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)


def get_user_info():
    service_drive = get_gdrive_service()  # 你之前的 drive service
    creds = service_drive._http.credentials  # 获取当前已授权的凭据

    # 构建 oauth2 服务对象
    from googleapiclient.discovery import build
    user_service = build('oauth2', 'v2', credentials=creds)

    # 获取用户信息
    user_info = user_service.userinfo().get().execute()

    print(f"用户 ID: {user_info.get('id')}")
    print(f"用户姓名: {user_info.get('name')}")
    print(f"头像链接: {user_info.get('picture')}")

    return user_info

if __name__ == '__main__':
    print(get_user_info())
