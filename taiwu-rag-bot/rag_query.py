import json
import faiss
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModel
# from sentence_transformers.util import cos_sim  # 备用方案
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# 1. 设置设备和模型
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
EMBED_MODEL = "./models/qwen3-embedding"  # 本地路径
CHAT_MODEL = "./models/qwen1.5-chat"
# 2. 加载 embedding 模型
print("[INFO] Loading embedding model...")
embed_tokenizer = AutoTokenizer.from_pretrained(EMBED_MODEL)
embed_model = AutoModel.from_pretrained(EMBED_MODEL).to(DEVICE)

# 3. 加载 Chat 模型
print("[INFO] Loading chat model...")
chat_tokenizer = AutoTokenizer.from_pretrained(CHAT_MODEL)
chat_model = AutoModelForCausalLM.from_pretrained(CHAT_MODEL).to(DEVICE)

# 4. 加载 FAISS 向量库和 metadata
print("[INFO] Loading FAISS index and metadata...")
index = faiss.read_index("data/taiwu_index.faiss")
with open("data/taiwu_metadata.jsonl", "r", encoding="utf-8") as f:
    metadatas = [json.loads(line) for line in f]

# 5. 获取文本 embedding
@torch.no_grad()
def get_embedding(text: str):
    inputs = embed_tokenizer(text, return_tensors="pt", max_length=512, truncation=True).to(DEVICE)
    outputs = embed_model(**inputs)
    emb = outputs.last_hidden_state[:, 0, :].squeeze().cpu().numpy()
    return emb

# 6. 搜索最近邻文本
def search_similar_chunks(query: str, top_k: int = 10):
    query_vec = get_embedding(query).astype("float32")
    D, I = index.search(query_vec.reshape(1, -1), top_k)
    results = [metadatas[i] for i in I[0]]
    return results

# 7. 构造 prompt 并生成回答
def generate_answer(query):
    print('开始计算相似性')


    contexts = search_similar_chunks(query, top_k=5)
    print(contexts)

    context_texts = [f"[{i+1}] {ctx['chunk']}" for i, ctx in enumerate(contexts)]
    full_context = "\n".join(context_texts)
    prompt = f"以下是关于《太吾绘卷》的资料：\n{full_context}\n\n基于上述内容，回答问题：{query}"

    inputs = chat_tokenizer(prompt, return_tensors="pt").to(DEVICE)
    outputs = chat_model.generate(**inputs, max_new_tokens=300)
    return chat_tokenizer.decode(outputs[0], skip_special_tokens=True)

# 8. 简易 CLI 入口
if __name__ == '__main__':
    while True:
        query = input("请输入你的问题（按 Ctrl+C 退出）：")
        answer = generate_answer(query)
        print("\n【回答】：")
        print(answer)
        print("\n" + "=" * 50 + "\n")
# 太吾绘卷少林派的所有功法的介绍和详情