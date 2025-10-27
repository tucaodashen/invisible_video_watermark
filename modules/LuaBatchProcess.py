import lupa
from lupa import LuaRuntime

# 定义一些你想要暴露的 Python 函数
def python_add(a, b):
    """一个简单的加法函数"""
    return a + b

def python_get_info():
    """返回一些信息"""
    return {"version": "1.0", "author": "You"}

# 创建 Lua 运行时
lua = LuaRuntime()

# 将 Python 函数设置为 Lua 的全局变量
lua.globals()['add'] = python_add
lua.globals()['get_info'] = python_get_info
# 你也可以暴露整个模块（谨慎使用），但通常更推荐暴露特定函数
# lua.globals()['os'] = os

# 现在在 Lua 代码中就可以直接调用 `add` 和 `get_info` 了
lua_script = '''
-- 调用暴露的 Python 函数
local result = add(10, 20)
print("Result of add(10, 20):", result)

-- 调用另一个函数，处理返回的 Python 字典（在 Lua 中表现为表）
local info = get_info()
print("Software version:", info['version'])
print("Author:", info['author'])

-- 甚至可以把这个表再传回给 Python
return info
'''

# 执行这段 Lua 脚本
lua_result = lua.execute(lua_script)
print("Returned from Lua:", lua_result)
# 输出类似: Returned from Lua: {'version': '1.0', 'author': 'You'}