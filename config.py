from dotenv import dotenv_values

# 从本地的 dotenv 文件加载配置
config = {
    **dotenv_values('.env'),
}
