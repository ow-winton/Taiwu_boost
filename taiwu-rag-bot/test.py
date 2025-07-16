# Load model directly
from sympy.printing.pytorch import torch
from transformers import AutoTokenizer, AutoModelForCausalLM



device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"当前设备: {device}")

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen1.5-1.8B-Chat")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen1.5-1.8B-Chat")
model.to(device)

prompt = '介绍一下太吾绘卷这款游戏。'
inputs = tokenizer(prompt, return_tensors="pt")
inputs = {k: v.to(device) for k, v in inputs.items()}


with torch.no_grad():
    outputs = model.generate(**inputs, max_new_tokens =200)

print(tokenizer.decode(outputs[0], skip_special_tokens=True))

