from transformers import AutoTokenizer, AutoModel
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"当前设备: {device}")
# 加载 Qwen-Embedding 模型和分词器
model_name = "Qwen/Qwen3-Embedding-0.6B"  # 你用的具体embedding模型名，替换成实际的

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
model.to(device)
def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
    inputs = {k: v.to("cuda") for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
        # 假设取第一个token的hidden state作为embedding，也可以根据模型说明选择池化方法
        embedding = outputs.last_hidden_state[:, 0, :]
        embedding = embedding.squeeze().cpu().numpy()
    return embedding

# 测试
text = "介绍一下太吾绘卷这款游戏。"
emb = get_embedding(text)
print(emb.shape)  # 维度大小
