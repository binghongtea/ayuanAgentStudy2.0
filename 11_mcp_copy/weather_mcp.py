import mcp
from mcp.server.fastmcp import FastMCP

# 1.创建 MCP 服务实例
mcp = FastMCP(name="weather-server")

# 2.往 mcp 服务里面添加工具
@mcp.tool()
def get_weather(location: str) -> str:
    """
    获取某个位置的天气信息
    :param location: 地理位置
    :return: 天气情况
    """
    return f"{location}的天气是100摄氏度，请你准备防晒。"

# 启动服务
if __name__ == '__main__':
    mcp.run()