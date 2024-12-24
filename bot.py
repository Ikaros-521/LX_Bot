# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

# import nonebot
# from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter

# # Custom your logger
# # 
# # from nonebot.log import logger, default_format
# # logger.add("error.log",
# #            rotation="00:00",
# #            diagnose=False,
# #            level="ERROR",
# #            format=default_format)

# # You can pass some keyword args config to init function
# nonebot.init()
# app = nonebot.get_asgi()

# driver = nonebot.get_driver()
# driver.register_adapter(ONEBOT_V11Adapter)


# nonebot.load_builtin_plugins("echo")
# # 导入src/plugins下自己开发的插件 ps:因为pyproject.toml的配置，src/plugins默认导入，所以不需要在手动导入了
# # nonebot.load_plugins('src/plugins')

# # nonebot.load_plugin("nonebot_plugin_translator")

# # Please DO NOT modify this file unless you know what you are doing!
# # As an alternative, you should use command `nb` or modify `pyproject.toml` to load plugins
# nonebot.load_from_toml("pyproject.toml")

# # Modify some config / config depends on loaded configs
# # 
# # config = driver.config
# # do something...


# if __name__ == "__main__":
#     nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
#     nonebot.run(app="__mp_main__:app")
import nonebot
from nonebot.adapters.console import Adapter as ConsoleAdapter  # 避免重复命名
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter

# 初始化 NoneBot
nonebot.init()

# 注册适配器
driver = nonebot.get_driver()
#driver.register_adapter(ConsoleAdapter)
driver.register_adapter(ONEBOT_V11Adapter)

# 在这里加载插件
nonebot.load_builtin_plugins("echo")  # 内置插件
nonebot.load_plugins("src/plugins")
# nonebot.load_plugin("thirdparty_plugin")  # 第三方插件
# nonebot.load_plugins("awesome_bot/plugins")  # 本地插件

if __name__ == "__main__":
    nonebot.run()