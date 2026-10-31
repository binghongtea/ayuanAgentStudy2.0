"""将文件或标准输入中的学习笔记保存为 UTF-8 Markdown。"""

import argparse
from pathlib import Path
import sys


def save_notes(content: str, output: Path, overwrite: bool = False) -> Path:
    if not content.strip():
        raise ValueError("学习笔记内容不能为空")
    output = output.expanduser().resolve()
    if output.suffix.lower() != ".md":
        raise ValueError("输出文件必须使用 .md 扩展名")
    output.parent.mkdir(parents=True, exist_ok=True)
    # x 模式避免在检查后、写入前发生文件重名而意外覆盖。
    with output.open("w" if overwrite else "x", encoding="utf-8", newline="\n") as stream:
        stream.write(content)
        if not content.endswith("\n"):
            stream.write("\n")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="UTF-8 输入文件；省略时从标准输入读取")
    parser.add_argument("--output", required=True, type=Path, help="目标 Markdown 文件路径")
    parser.add_argument("--overwrite", action="store_true", help="允许覆盖已有文件")
    args = parser.parse_args()

    try:
        if args.input:
            content = args.input.read_text(encoding="utf-8-sig")
        else:
            if sys.stdin.isatty():
                parser.error("请使用 --input 指定文件，或通过标准输入传入笔记")
            # 以 UTF-8 读取管道，避免 Windows 默认编码损坏中文。
            content = sys.stdin.buffer.read().decode("utf-8-sig")
        path = save_notes(content, args.output, args.overwrite)
    except (OSError, ValueError) as error:
        print(f"保存失败：{error}", file=sys.stderr)
        return 1

    print(f"保存成功：{path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
