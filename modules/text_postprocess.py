from datasketch import MinHash, MinHashLSH
from tqdm import tqdm

def group_text(strings, threshold=0.5, min_samples=2):
    """
    高效相似字符串检测（使用datasketch）并显示进度
    """
    print(f"开始处理 {len(strings)} 个字符串...")

    # 1. 创建MinHash LSH索引
    print("创建MinHash索引...")
    lsh = MinHashLSH(threshold=threshold, num_perm=128)
    minhashes = {}

    # 使用tqdm显示进度条
    progress_bar = tqdm(total=len(strings), desc="处理字符串")

    for idx, s in enumerate(strings):
        # 简化预处理：仅小写化
        normalized = s.lower()
        m = MinHash(num_perm=128)

        # 使用字符3-gram
        for i in range(len(normalized) - 2):
            gram = normalized[i:i + 3]
            m.update(gram.encode('utf-8'))

        lsh.insert(idx, m)
        minhashes[idx] = m

        # 更新进度条
        progress_bar.update(1)

    progress_bar.close()
    print("索引创建完成，开始查找相似组...")

    # 2. 查找相似组
    groups = []
    visited = set()

    # 创建第二个进度条
    group_progress = tqdm(total=len(strings), desc="查找相似组")

    for idx in range(len(strings)):
        if idx in visited:
            group_progress.update(1)
            continue

        # 查找相似字符串
        similar_indices = lsh.query(minhashes[idx])

        # 更新已访问索引
        visited.update(similar_indices)

        # 更新进度条（跳过已访问的项）
        group_progress.update(len(similar_indices))

        # 检查是否满足最小样本要求
        if len(similar_indices) >= min_samples:
            group = [strings[i] for i in similar_indices]
            groups.append(group)

    group_progress.close()

    return groups