from langchain_text_splitters import RecursiveCharacterTextSplitter


text = "早上阳光明媚。鸟儿在歌唱！你听见了吗？真动听。午后可能下雨。别忘了带伞！"

# ===== case 1：普通字符串分隔符，移除实际用于切分的标点 =====
# 分隔符会按顺序递归尝试；未参与切分的标点仍可能保留。
splitter1 = RecursiveCharacterTextSplitter(
    separators=["。", "！", "？"],
    is_separator_regex=False,
    keep_separator=False,
    chunk_size=10,   # 改小，强制切分
    chunk_overlap=0,
)
chunks1 = splitter1.split_text(text)
print("\n【is_separator_regex=False】切分结果:")
for i, chunk in enumerate(chunks1, 1):
    print(f"  块{i}: '{chunk}'")


# ===== case 2：正则表达式，在中文句末标点后切分，保留标点 =====
splitter2 = RecursiveCharacterTextSplitter(
    chunk_size=10,
    chunk_overlap=2,
    is_separator_regex=True,
    # 匹配“。！？后面的位置”，而不是匹配标点本身。
    separators=[r"(?<=[。！？])"],
)
chunks2 = splitter2.split_text(text)
print("\n【is_separator_regex=True】切分结果:")
for i, chunk in enumerate(chunks2, 1):
    print(i, chunk)
"""
早上阳光明媚。
鸟儿在歌唱！
你听见了吗？真动听。
午后可能下雨。
别忘了带伞！
"""
