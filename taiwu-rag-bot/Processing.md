# 1.切分文本（Chunking） 
 LangChain  RecursiveCharacterTextSplitter
# 2. 文本向量化（Embedding） 
Qwen-Embedding
# 3. 建向量数据库（索引）
将 embedding 存入向量数据库中以支持向量检索（相似度 Top-K 搜索）
FAISS（轻量级、快速，适合本地 RAG）
Chroma / Qdrant（支持 LangChain）
# 4. 集成 RAG 流程（LangChain / LlamaIndex）
把步骤 1～3 组织起来后，就可以构建如下流程：

用户问题 → embedding → Top-K相似段落 → 组成 prompt → 送入大模型（Qwen） → 得到答案

 LangChain（模块清晰，支持 Qwen，教程多）
 
# 7.16 表现不佳，优化方向
| 问题                | 说明        | 建议                        |
| ----------------- | --------- | ------------------------- |
| 模型小               | 理解和生成能力有限 | 尝试更大模型或者微调模型              |
| 检索文本质量            | 数据缺失或不相关  | 确保爬取完整数据，优化检索策略           |
| embedding和chat不匹配 | 匹配不准确     | 尽量用同一系列模型的embedding和chat  |
| prompt设计          | 信息没充分传达   | 设计更详细、上下文丰富的prompt        |
| 生成参数              | 参数不合理     | 尝试调节temperature、top\_k等参数 |
| 微调缺失              | 缺少领域专用知识  | 尝试做领域微调                   |

# 回复速度也很慢
