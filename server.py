import argparse
import logging
import os
import time
from fastapi import FastAPI
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, List, Union
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
from typing import Any, List, Optional, Dict, Union
from typing_extensions import TypedDict, NotRequired, Literal

logging.basicConfig(level=logging.INFO,
                    format=r"%(asctime)s - %(module)s - %(levelname)s - %(message)s")

# 设置服务器
MODEL = None
app = FastAPI(title="Bert model Python API like OpenAI",
              version="0.0.1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
router = APIRouter()

# Health check
@app.get("/ping")
async def ping():
    return "pong"

model_field = Field(
    description="The model to use for generating completions.", default=None
)


class CreateEmbeddingRequest(BaseModel):
    model: Optional[str] = model_field
    input: Union[str, List[str]] = Field(description="The input to embed.")
    user: Optional[str] = Field(default=None)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "input": "The food was delicious and the waiter...",
                }
            ]
        }
    }


class EmbeddingUsage(BaseModel):
    prompt_tokens: int
    total_tokens: int


class Embedding(BaseModel):
    index: int
    object: str
    embedding: List[float]


class CreateEmbeddingResponse(BaseModel):
    object: Literal["list"]
    model: str
    data: List[Embedding]
    usage: EmbeddingUsage

# 兼容LocalAI的Embedding 接口


@router.post("/embeddings", response_model=CreateEmbeddingResponse)
def create_embeddings_localai(request: CreateEmbeddingRequest) -> CreateEmbeddingResponse:
    return create_embeddings(request=request)


@router.post("/v1/embeddings", response_model=CreateEmbeddingResponse)
def create_embeddings(request: CreateEmbeddingRequest) -> CreateEmbeddingResponse:
    # 记录请求开始时间戳
    start_time = time.time()
    model_name = request.model
    if not model_name:
        model_name = ""
    sentences = request.input
    if isinstance(sentences, str):
        sentences = [sentences]

    # 转换成向量
    # Sentences are encoded by calling model.encode()
    global MODEL
    embeddings = MODEL.encode(sentences)

    # 处理请求逻辑，生成相应的数据
    embedding_data = {}
    embedding_data['model'] = model_name
    embedding_data["object"] = "list"
    embedding_data["data"] = []
    total_tokens = 0
    for sentence, embedding in zip(sentences, embeddings):
        embedding = {
            "object": "embedding",
            "embedding": embedding.tolist(),
            "index": 0,
        }
        embedding_data["data"].append(embedding)
        total_tokens += len(sentence)
    embedding_data["usage"] = {
        "prompt_tokens": total_tokens,
        "total_tokens": total_tokens
    }

    # 记录请求结束时间戳
    end_time = time.time()
    # 计算请求耗时
    elapsed_time = end_time - start_time
    logging.info(
        f"embedding input: {sentences}\n Request time: {elapsed_time} seconds")
    return embedding_data


if __name__ == '__main__':
    # 创建参数解析器
    parser = argparse.ArgumentParser(description="FastAPI Server")

    # 添加文件夹路径参数
    parser.add_argument("--model", type=str, help="The model folder path")

    # 解析命令行参数
    args, _ = parser.parse_known_args()

    # 获取文件夹路径参数的值
    folder_path = args.model

    # 如果未提供文件夹路径参数，则使用 server.py 所在的文件夹作为默认路径
    if not folder_path:
        folder_path = os.path.dirname(os.path.abspath(__file__))

    # 检查文件夹路径是否存在并且是一个文件夹
    if not os.path.isdir(folder_path):
        print("Invalid folder path. Please provide a valid folder path.")
        exit(1)

    # 加载目标模型
    MODEL = SentenceTransformer(folder_path)

    # 注册路由和启动
    app.include_router(router)
    uvicorn.run(app, host=os.getenv("HOST", "0.0.0.0"),
                port=int(os.getenv("PORT", 8899)))
