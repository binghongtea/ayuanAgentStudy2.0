from mcp.server.fastmcp import FastMCP

# ========== 1. 导入 DBManager ==========
from db_manager import DBManager

# ========== 2. 创建数据库连接 ==========
db = DBManager(
    username="root",
    password="254083",
    host="localhost",
    port=3306,
    database="test"
)

# ========== 3. 创建 MCP Server ==========
mcp = FastMCP(
    "text2sql-db-server",
    host="127.0.0.1",
    port=8000,
    # Streamable HTTP 的访问路径
    streamable_http_path="/mcp",
    # 无状态模式：每个请求独立处理，适合生产部署
    stateless_http=True,

    # True：普通 JSON 响应
    # False：允许通过 SSE 流式返回响应
    json_response=True
)

# ========== 4. 定义工具函数 ==========
@mcp.tool()
def execute_sql_query(sql: str) -> str:
    """
    执行 SQL 查询语句并返回结果。
    参数 sql: 要执行的 SELECT 查询语句
    返回: 查询结果的文本描述
    """
    try:
        result = db.execute_query(sql)

        if not result:
            return "查询结果为空"

        # 格式化输出
        if len(result) == 1:
            return str(result[0])
        else:
            output = f"共查询到 {len(result)} 条记录：\n"
            for i, row in enumerate(result, 1):
                output += f"  {i}. {row}\n"
            return output.strip()

    except Exception as e:
        return f"查询失败: {str(e)}"


@mcp.tool()
def get_table_schema() -> str:
    """
    获取当前数据库的所有表结构信息，包括表名、字段、类型、主键、外键等。
    返回: 表结构的文本描述
    """
    try:
        schemas = db.get_all_table_schemas()

        if not schemas:
            return "数据库中没有表"

        output = "【数据库表结构】\n\n"
        for table_name, info in schemas.items():
            output += f"   表名: {table_name}\n"
            output += f"   注释: {info['comment']}\n"
            output += "   字段:\n"

            for col in info["columns"]:
                null_str = "可空" if col["nullable"] else "非空"
                output += f"     - {col['name']} ({col['type']}) {null_str}"
                if col['comment']:
                    output += f" 注释: {col['comment']}"
                output += "\n"

            if info["primary_keys"]:
                output += f"   主键: {', '.join(info['primary_keys'])}\n"

            if info.get("foreign_keys"):
                output += "   外键:\n"
                for fk in info["foreign_keys"]:
                    constrained = ", ".join(fk.get("constrained_columns", []))
                    referred_cols = ", ".join(fk.get("referred_columns", []))
                    output += f"     - {constrained} -> {fk.get('referred_table', '')}({referred_cols})\n"

            if info["indexes"]:
                output += "   索引:\n"
                for idx in info["indexes"]:
                    unique_str = "唯一" if idx["unique"] else "普通"
                    output += f"     - {idx['name']} ({unique_str}): {', '.join(idx['columns'])}\n"

            output += "\n"

        return output.strip()

    except Exception as e:
        return f"获取表结构失败: {str(e)}"


@mcp.tool()
def get_table_names() -> str:
    """
    获取数据库中所有表名列表。
    返回: 表名列表的文本描述
    """
    try:
        tables = db.get_table_names()
        if not tables:
            return "数据库中没有表"
        return f"数据库中的表有：{', '.join(tables)}"
    except Exception as e:
        return f"获取表名失败: {str(e)}"


# ========== 5. 启动 ==========
if __name__ == "__main__":
    mcp.run(transport="streamable-http")