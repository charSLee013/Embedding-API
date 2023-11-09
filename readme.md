# Embedding API
> 实现OpenAI的Embedding API 服务，支持BERT, SBERT, CoSENT 模型

# 使用

拉取镜像，这里以`text2vec-base-chinese-paraphrase`为例子
```shell
git lfs install
git clone https://huggingface.co/shibing624/text2vec-base-chinese-paraphrase
```

## 从项目开始
拉取项目
```shell
git clone https://github.com/charSLee013/Embedding-API
```

安装依赖
```shell
pip install ./requirements.txt
```

启动服务
```shell
python3 server.py --model ./text2vec-base-chinese-paraphrase
```

## 从容器开始

构建镜像
```shell
docker build -t embedding_api .
```

启动容器
```shell

```