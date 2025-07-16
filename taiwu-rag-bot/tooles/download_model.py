"""
从Hugging face下载模型
"""
from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM


# 下载 Embedding 模型
embed_model_id = "Qwen/Qwen3-Embedding-0.6B"
embed_save_dir = "./models/qwen3-embedding"

tokenizer = AutoTokenizer.from_pretrained(embed_model_id)
model = AutoModel.from_pretrained(embed_model_id)

tokenizer.save_pretrained(embed_save_dir)
model.save_pretrained(embed_save_dir)


# 下载 Chat 模型
chat_model_id = "Qwen/Qwen1.5-0.5B-Chat"
chat_save_dir = "./models/qwen1.5-0.5B-chat"

chat_tokenizer = AutoTokenizer.from_pretrained(chat_model_id)
chat_model = AutoModelForCausalLM.from_pretrained(chat_model_id)

chat_tokenizer.save_pretrained(chat_save_dir)
chat_model.save_pretrained(chat_save_dir)
