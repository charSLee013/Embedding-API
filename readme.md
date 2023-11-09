# Embedding API

> 实现了OpenAI的Embedding API服务，支持BERT、SBERT和CoSENT模型。🚀
<div align="center">

[中文](./readme.md) | [English](./readme_en.md)
</div>
<br />

## 部署 🛠️

以`text2vec-base-chinese-paraphrase`为例，首先拉取镜像：
```shell
git lfs install
git clone https://huggingface.co/shibing624/text2vec-base-chinese-paraphrase
```

## 从项目开始 🚀

克隆项目：
```shell
git clone https://github.com/charSLee013/Embedding-API
```

安装依赖：
```shell
pip install -r requirements.txt
```

启动服务：
```shell
python3 server.py --model ./text2vec-base-chinese-paraphrase
```

## 从Docker容器开始 🐳

构建Docker镜像：
```shell
docker build -t embedding_api .
```

运行容器：
```shell
docker run --rm -p 8899:8899 -v /data/text2vec-base-multilingual/:/model embedding_api python server.py --model /model
```

# 使用方法 🚀

在项目中运行测试脚本：
```shell
bash test_client.sh
```

输出应类似于：
```json
{
  "object": "list",
  "model": "text-embedding-ada-002",
  "data": [
    {
      "index": 0,
      "object": "embedding",
      "embedding": [
        0.19880373775959015,
        ...[1024个字段]
        0.18911297619342804
      ]
    }
  ],
  "usage": {
    "prompt_tokens": 26,
    "total_tokens": 26
  }
}
```

# 文档 📚

在启动服务器后，直接在浏览器中打开 [http://localhost:8899/docs](http://localhost:8899/docs)。

![docs.png](./assets/docs.png)

## 许可证 📝本项目使用 [MIT许可证](LICENSE)。

## 问题和拉取请求 🙋‍♀️如果您遇到任何问题或想为此项目做贡献，请随时在 [GitHub存储库](https://github.com/charSLee013/Embedding-API) 上打开新的问题或提交拉取请求。我们欢迎您的反馈和贡献！❤️