from typing import List, Dict

import requests
import BasicSystem
from PySide6.QtCore import QObject, Signal
import threading

class UpdateRunner(QObject):
    update_available = Signal(str, str)
    def __init__(self):
        super().__init__()
        self.check_thread = threading.Thread(target=self.check_update)
        self._is_thread_running = False
        self.version = ""
        self.change_log = ""

    def check_thread(self):
        try:
            self._is_thread_running = True
            version, changelog = get_latest_github_release_info(BasicSystem.const.owner, BasicSystem.const.name)
            if version and changelog:
                self.version = version
                self.change_log = changelog
                self.update_available.emit(version, changelog)
        except:
            raise
        finally:
            self._is_thread_running = False

    def check_update(self):
        if self._is_thread_running:
            return
        self.check_thread.start()


def get_latest_github_release_info(repo_owner, repo_name):
    """
    通过 GitHub API 获取最新 Release 的版本号和更新日志。
    """
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    headers = {
        # GitHub 推荐在请求 API 时设置 User-Agent
        "User-Agent": "Python Script"
    }

    try:
        # 发送 GET 请求
        response = requests.get(api_url, headers=headers)

        # 检查响应状态码
        if response.status_code == 200:
            # 解析 JSON 响应
            release_data = response.json()

            # 提取所需信息
            version = release_data.get('tag_name')
            changelog = release_data.get('body')

            return version, changelog
        elif response.status_code == 404:
            print("错误：仓库或 Release 未找到。请检查拥有者和仓库名称是否正确。")
            return None, None
        else:
            print(f"错误：请求失败，状态码：{response.status_code}")
            return None, None

    except requests.exceptions.RequestException as e:
        print(f"请求发生异常: {e}")
        return None, None


def get_latest_release_assets(owner: str, repo: str) -> List[Dict[str, str]]:
    """
    从 GitHub 仓库获取最新 release 中的发布文件的下载链接和名称。

    Args:
        owner: 仓库所有者的用户名（例如: 'tucaodashen'）。
        repo: 仓库名称（例如: 'invisible_video_watermark'）。

    Returns:
        包含文件名称 (name) 和下载链接 (browser_download_url) 的字典列表。
        如果获取失败或没有 assets，则返回空列表。
    """
    api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"

    # 推荐设置 Accept 头部以确保接收到正确的 JSON 格式
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"  # 推荐指定 API 版本
    }

    print(f"正在请求: {api_url}")

    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()  # 如果状态码不是 2xx，则抛出异常

        release_data = response.json()

        # 检查是否存在 assets 列表
        assets = release_data.get('assets', [])

        if not assets:
            print("最新 release 中没有找到发布文件 (assets)。")
            return []

        # 提取所需信息
        asset_info_list = []
        for asset in assets:
            name = asset.get('name')
            download_url = asset.get('browser_download_url')

            if name and download_url:
                asset_info_list.append({
                    "name": name,
                    "download_url": download_url
                })

        return asset_info_list

    except requests.exceptions.HTTPError as e:
        print(f"HTTP 错误: {e}")
        print(f"状态码: {e.response.status_code}")
        # 如果是 404 (Not Found)，可能是因为仓库不存在或者没有发布正式 release
        if e.response.status_code == 404:
            print(
                "仓库或最新 release 未找到。请确认仓库所有者和名称是否正确，以及是否有正式发布 (non-draft, non-prerelease)。")
        return []
    except requests.exceptions.RequestException as e:
        print(f"请求发生错误: {e}")
        return []
    except Exception as e:
        print(f"发生意外错误: {e}")
        return []

