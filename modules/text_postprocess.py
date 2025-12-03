from datasketch import MinHash, MinHashLSH
from tqdm import tqdm
from BasicSystem.log_client import setup_logger,get_logger
setup_logger(default_tags="text_postprocess", enable_udp=True, enable_console=True)
logger = get_logger()

def group_text(strings, threshold=0.5, min_samples=2):
    """
    高效相似字符串检测（使用datasketch）并显示进度
    """
    logger.info(f"Begin to process {len(strings)} strings...",tags="text_postprocess:group_text")
    lsh = MinHashLSH(threshold=threshold, num_perm=128)
    minhashes = {}
    progress_bar = tqdm(total=len(strings), desc="Processing strings")

    for idx, s in enumerate(strings):
        normalized = s.lower()
        m = MinHash(num_perm=128)
        for i in range(len(normalized) - 2):
            gram = normalized[i:i + 3]
            m.update(gram.encode('utf-8'))

        lsh.insert(idx, m)
        minhashes[idx] = m
        progress_bar.update(1)

    progress_bar.close()
    logger.debug(f"MinHash index created with {len(minhashes)} strings",tags="text_postprocess:group_text")

    groups = []
    visited = set()

    group_progress = tqdm(total=len(strings), desc="查找相似组")

    for idx in range(len(strings)):
        if idx in visited:
            group_progress.update(1)
            continue

        similar_indices = lsh.query(minhashes[idx])

        visited.update(similar_indices)

        group_progress.update(len(similar_indices))

        if len(similar_indices) >= min_samples:
            group = [strings[i] for i in similar_indices]
            groups.append(group)

    group_progress.close()
    logger.debug(f"Find {len(groups)} groups with at least {min_samples} samples",tags="text_postprocess:group_text")

    return groups