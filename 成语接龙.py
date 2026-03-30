# -*- coding: utf-8 -*-
# 时间 : 2026/3/30 09:08
# 作者 : mcy
# 文件 : 成语接龙.py
from langchain_community.vectorstores import FAISS # 导入FAISS向量存储库
from langchain_huggingface import HuggingFaceEmbeddings # 导入Hugging Face嵌入模型
from langchain_community.document_loaders import TextLoader # 导入文本加载器
from langchain.text_splitter import RecursiveCharacterTextSplitter
# 导入递归字符文本分割器
from langchain_openai import ChatOpenAI # 导入ChatOpenAI模型
# 使用 OpenAI API 的 ChatOpenAI 模型
chat_model = ChatOpenAI(openai_api_key="ollama", # ollama兼容OpenAI API的格式
    base_url="http://localhost:11434/v1",
    model="gemma3:4b"
    )
# 加载文本文件 "sanguoyanyi.txt"，编码格式为 'utf-8'
loader = TextLoader("成语大全.txt", encoding='utf-8')
docs = loader.load() # 将文件内容加载到变量 docs 中
# 把文本分割成4 字一组的切片，每组之间有 20 字重叠
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200,
chunk_overlap=20)
chunks = text_splitter.split_documents(docs) # 将文档分割成多个小块
# print(chunks)
# 初始化嵌入模型，使用预训练的语言模型 'bge-large-zh-v1___5'
embedding = HuggingFaceEmbeddings(model_name='models/AI-ModelScope/bge-large-zh-v1___5')
# 构建 FAISS 向量存储和对应的 retriever
vs = FAISS.from_documents(chunks, embedding) # 将文本块转换为向量并存储在FAISS中
retriever = vs.as_retriever() # 创建一个检索器用于从向量存储中获取相关信息
from langchain.chains import RetrievalQA # 导入RetrievalQA链
from langchain.prompts import (
ChatPromptTemplate,
SystemMessagePromptTemplate,
HumanMessagePromptTemplate,
)
# 创建一个系统消息，用于定义机器人的角色
system_message = SystemMessagePromptTemplate.from_template(
"根据以下已知信息回答用户问题。\n 已知信息{context}"
)
# 创建一个人类消息，用于接收用户的输入
human_message = HumanMessagePromptTemplate.from_template(
"用户问题：{question}"
)
# 将这些模板结合成一个完整的聊天提示
chat_prompt = ChatPromptTemplate.from_messages([
system_message,
human_message,
])