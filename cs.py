# -*- coding: utf-8 -*-
# 修复版：成语接龙 + FAISS检索 + 强制从成语库取词 + 不会空结果
import re
import random
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI

# ---------------------- 模型配置 ----------------------
chat_model = ChatOpenAI(
    openai_api_key="ollama",
    base_url="http://localhost:11434/v1",
    model="gemma3:4b"
)

# ---------------------- 加载成语库 ----------------------
try:
    loader = TextLoader("成语大全.txt", encoding='utf-8')
    docs = loader.load()
except:
    print("❌ 请确保当前目录存在 成语大全.txt 文件！")
    exit()

# 读取所有成语（一行一个）
all_idioms = set()
for doc in docs:
    lines = doc.page_content.strip().split("\n")
    for line in lines:
        line = line.strip()
        if len(line) == 4:
            all_idioms.add(line)

print(f"✅ 成功加载成语数量：{len(all_idioms)} 个")

# ---------------------- 构建检索库 ----------------------
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
chunks = text_splitter.split_documents(docs)

embedding = HuggingFaceEmbeddings(model_name='models/AI-ModelScope/bge-large-zh-v1___5')
vs = FAISS.from_documents(chunks, embedding)
retriever = vs.as_retriever(search_kwargs={"k": 20})

# ---------------------- 核心工具函数 ----------------------
def get_last_char(idiom):
    return idiom[-1]

def is_valid_idiom(idiom):
    """强制从本地成语集合判断，100%准确"""
    return idiom in all_idioms

def find_idioms_start_with(char):
    """直接从成语库找，不会空！"""
    candidates = [idiom for idiom in all_idioms if idiom.startswith(char)]
    return candidates

# ---------------------- 游戏主逻辑 ----------------------
def play_game():
    print("=" * 50)
    print("     🎮 LangChain + FAISS 成语接龙（修复版）")
    print("规则：必须在【成语大全.txt】中才算有效")
    print("=" * 50)

    # 起始成语
    while True:
        start = input("\n请输入起始成语：").strip()
        if is_valid_idiom(start):
            current = start
            print("✅ 成语有效，游戏开始！")
            break
        else:
            print("❌ 成语不在库中，请重新输入")

    round_num = 1

    while True:
        print(f"\n===== 第 {round_num} 轮 =====")
        print(f"当前成语：{current}")

        last = get_last_char(current)
        print(f"需要接：【{last}】开头")

        # AI 直接从成语库找（修复关键！）
        ai_list = find_idioms_start_with(last)
        if not ai_list:
            print("🎉 AI 无成语可用 → 你获胜！")
            break

        ai_idiom = random.choice(ai_list)
        print(f"🤖 AI 接龙：{ai_idiom}")

        # 玩家输入
        last_ai = get_last_char(ai_idiom)
        user = input(f"\n请你接【{last_ai}】：").strip()

        # 判断
        if not is_valid_idiom(user):
            print("❌ 你的成语不在库中 → AI 获胜！")
            break
        if not user.startswith(last_ai):
            print("❌ 首字不匹配 → 你输了！")
            break

        current = user
        round_num += 1

if __name__ == "__main__":
    play_game()