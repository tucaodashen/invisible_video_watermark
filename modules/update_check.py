
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


# 目标仓库信息
owner = "tucaodashen"
name = "invisible_video_watermark"

version, changelog = get_latest_github_release_info(owner, name)

if version and changelog:
    print(f"## 🎉 最新版本号：{version}")
    print("\n--- 更新日志 ---\n")
    print(changelog)
else:
    print("未能获取最新 Release 信息。")