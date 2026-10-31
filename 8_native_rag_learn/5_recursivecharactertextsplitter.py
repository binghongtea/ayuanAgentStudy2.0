from langchain_text_splitters import RecursiveCharacterTextSplitter


text = "早上阳光明媚。鸟儿在歌唱！你听见了吗？真动听。午后可能下雨。别忘了带伞！"

# ===== case 1：False（普通字符串，切掉标点）=====
splitter1 = RecursiveCharacterTextSplitter(
    separators=["。", "！", "？"],
    is_separator_regex=False,
    chunk_size=10,   # 改小，强制切分
    chunk_overlap=0,
)
chunks1 = splitter1.split_text(text)
print("\n【is_separator_regex=False】切分结果:")
for i, chunk in enumerate(chunks1, 1):
    print(f"  块{i}: '{chunk}'")


# ===== case 2：True（正则表达式，保留标点）=====
splitter2 = RecursiveCharacterTextSplitter(
    separators=["(?<=。)", "(?<=！)", "(?<=？)"],
    is_separator_regex=True,
    chunk_size=10,   # 同样改小
    chunk_overlap=0,
)
chunks2 = splitter2.split_text(text)
print("\n【is_separator_regex=True】切分结果:")
for i, chunk in enumerate(chunks2, 1):
    print(f"  块{i}: '{chunk}'")
