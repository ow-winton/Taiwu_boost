import json
from tqdm import tqdm
import numpy as np
import faiss
import os

from transformers import AutoTokenizer, AutoModel
import torch

# 设备设置
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"当前设备: {device}")

# 模型加载
model_name = "Qwen/Qwen3-Embedding-0.6B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
model.to(device)

# 嵌入函数
def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
        emb = outputs.last_hidden_state[:, 0, :].squeeze().cpu().numpy()
    return emb


# === 加载 chunk 数据 ===
data_path = os.path.join("../data", "taiwu_wiki_chunks.jsonl")
chunks = []
metadatas = []

with open(data_path, "r", encoding="utf-8") as f:
    for line in f:
        item = json.loads(line)
        text = item["chunk"]
        url = item["url"]
        chunks.append(text)
        metadatas.append(url)

print(f"共加载 {len(chunks)} 个文本片段")

# === 生成 embedding 向量 ===
embeddings = []
for text in tqdm(chunks, desc="Embedding"):
    vec = get_embedding(text)
    embeddings.append(vec)

embeddings = np.array(embeddings).astype("float32")

# === 构建 FAISS 向量索引 ===
dim = embeddings.shape[1]  # 向量维度
index = faiss.IndexFlatL2(dim)  # 使用 L2 距离（也可以使用余弦）
index.add(embeddings)

# === 保存索引和元数据 ===
faiss.write_index(index, "../data/taiwu_index.faiss")

with open("../data/taiwu_metadata.jsonl", "w", encoding="utf-8") as f:
    for url, chunk in zip(metadatas, chunks):
        json.dump({"url": url, "chunk": chunk}, f, ensure_ascii=False)
        f.write("\n")


print("✅ 向量数据库已构建并保存完成！")
