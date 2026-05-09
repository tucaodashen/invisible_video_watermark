import gettext
import json
import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

_ = gettext.gettext

# --- 1. 权限与样式定义 ---
SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid'
]


client_id = os.environ.get("GOOGLE_CLIENT_ID", "")
client_secret = os.environ.get("GOOGLE_CLIENT_SECRET", "")


# 添加了自动关闭脚本的 HTML
SUCCESS_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>认证成功</title>
    <style>
        body { font-family: 'Segoe UI', system-ui, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); margin: 0; }
        .card { background: white; padding: 3rem; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); text-align: center; max-width: 400px; animation: slideUp 0.5s ease-out; }
        @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .icon { font-size: 60px; margin-bottom: 1rem; }
        h1 { color: #1a73e8; margin: 0 0 1rem 0; font-size: 24px; }
        p { color: #5f6368; line-height: 1.6; margin-bottom: 2rem; }
        .btn { background-color: #1a73e8; color: white; border: none; padding: 12px 30px; border-radius: 50px; cursor: pointer; font-weight: bold; transition: all 0.3s; text-decoration: none; }
        .btn:hover { background-color: #1557b0; transform: scale(1.05); }
        .countdown { font-size: 12px; color: #999; margin-top: 1.5rem; }
    </style>
</head>
<body>
    <div class="card">
        <div class="icon">🎉</div>
        <h1>授权成功</h1>
        <p>您的账号已安全连接至应用。<br>现在可以关闭此窗口返回程序了。</p>
        <button onclick="window.close()" class="btn">立即关闭</button>
        <div class="countdown" id="timer">窗口将在 5 秒后自动关闭</div>
    </div>
    <script>
        let seconds = 5;
        const timer = document.getElementById('timer');
        const countdown = setInterval(() => {
            seconds--;
            timer.innerText = `窗口将在 ${seconds} 秒后自动关闭`;
            if (seconds <= 0) {
                clearInterval(countdown);
                window.close();
            }
        }, 1000);
    </script>
</body>
</html>
"""

def patch_google_server():
    """这是让 Google 库支持 HTML 渲染的黑魔法"""
    from google_auth_oauthlib.flow import _RedirectWSGIApp
    original_call = _RedirectWSGIApp.__call__

    def new_call(self, environ, start_response):
        def custom_start_response(status, headers, exc_info=None):
            # 找到 Content-Type 并修改为 text/html
            new_headers = []
            for name, value in headers:
                if name.lower() == 'content-type':
                    new_headers.append((name, 'text/html; charset=utf-8'))
                else:
                    new_headers.append((name, value))
            return start_response(status, new_headers, exc_info)

        return original_call(self, environ, custom_start_response)

    _RedirectWSGIApp.__call__ = new_call


def login():
    creds = None
    if os.path.exists('./assets/auth/google/token.json'):
        creds = Credentials.from_authorized_user_file('./assets/auth/google/token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # 应用补丁
            patch_google_server()

            client_config = {
                "installed": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": ["http://localhost"]
                }
            }
            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            # 在这里传入 SUCCESS_HTML
            creds = flow.run_local_server(
                port=0,
                success_message=SUCCESS_HTML,
                authorization_prompt_message=_("请在浏览器中完成登录...")
            )

        with open('./assets/auth/google/token.json', 'w') as token:
            token.write(creds.to_json())
    if not os.path.exists('./assets/auth/google/user_info.json') or not creds.valid:
        user_service = build('oauth2', 'v2', credentials=creds)
        user_info = user_service.userinfo().get().execute()
        with open('./assets/auth/google/user_info.json', 'w') as user_info_file:
            json.dump(user_info, user_info_file, indent=4)
    return creds


def get_drive_service():
    return build('drive', 'v3', credentials=login())

def get_user_info():
    user_info = None
    if not os.path.exists('./assets/auth/google/user_info.json'):
        creds = login()
        user_service = build('oauth2', 'v2', credentials=creds)
        user_info = user_service.userinfo().get().execute()
        with open('./assets/auth/google/user_info.json', 'w') as user_info_file:
            json.dump(user_info, user_info_file, indent=4)
    else:
        with open('./assets/auth/google/user_info.json', 'r') as user_info_file:
            user_info = json.load(user_info_file)
    return user_info





if __name__ == '__main__':
    info = get_user_info()
    print(f"你好, {info.get('name')}!")