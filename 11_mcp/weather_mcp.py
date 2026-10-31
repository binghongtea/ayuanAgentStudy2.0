# weather_server.py
from mcp.server.fastmcp import FastMCP

# 创建 MCP 服务实例
mcp = FastMCP("weather-server")


@mcp.tool()
def get_weather(location: str) -> str:
    """
    获取某个位置的天气信息

    :param location: 地理位置
    :return: 天气情况
    """
    return f"{location}的天气是100摄氏度，请你准备防晒。"


if __name__ == "__main__":
    # 默认使用 stdio 传输（适合被 Claude Desktop / Cursor 等客户端调用）
    mcp.run(transport="stdio")