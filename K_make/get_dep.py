"""
递归查询依赖
ChatGPT写的

别问，问就是我这个笨比不会写递归（
꒰ঌ(⸝⸝ ↀ ᯅ ↀ⸝⸝)໒꒱
"""
import analysis_NDEP

def find_dependencies(packages, target_key):
    def recurse(package_key, result_set):
        # 找到当前key对应的包
        current_package = next((pkg for pkg in packages if pkg['package']['key'] == package_key), None)
        if not current_package:
            return  # 如果没有找到对应的包，直接返回

        # 添加当前包的key到结果集中
        result_set.add(package_key)

        # 遍历当前包的dependencies列表
        for dep in current_package['dependencies']:
            # 如果依赖项是一个字典，我们取它的key值
            if isinstance(dep, dict):
                dep_key = dep['key']
            else:
                dep_key = dep  # 如果依赖项不是一个字典，我们认为它是一个key

            # 递归处理依赖项
            recurse(dep_key, result_set)

    # 初始化结果集
    result_set = set()
    # 从目标key开始递归
    recurse(target_key, result_set)
    # 将结果集转换为列表并返回
    return list(result_set)


if __name__ == '__main__':
    print(find_dependencies(analysis_NDEP.get_full_dependence(), "pillow"))



