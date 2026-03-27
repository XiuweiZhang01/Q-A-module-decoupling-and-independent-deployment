# Q-A-module-decoupling-and-independent-deployment
Phase 3 independent QA service based on FastAPI, supporting text chat, audio chat and audio-tts
# Part3 Xiaozhi QA Service
基于 FastAPI 的独立问答服务项目，用于完成第三阶段“问答模块解耦与服务独立部署”任务。项目目标包括提取并独立部署语音问答核心逻辑，提供支持文本/语音问答的 REST API，并补充接口文档、Postman 示例和性能测试。:contentReference[oaicite:0]{index=0}

---

## 项目简介

本项目基于原始 `xiaozhi-esp32-server` 进行模块拆解与服务化改造，将问答核心能力从原项目中独立出来，构建为可单独部署和调用的 FastAPI 服务。

当前已支持以下功能：

- 文本问答
- 音频问答
- 音频问答 + TTS
- 健康检查
- Swagger 在线接口文档

---

## 项目结构

```text
Part3/
├── api/                  # 路由接口
├── config/               # 配置与日志管理
├── core/                 # 核心处理逻辑
├── data/                 # 数据与配置文件
├── models/               # 模型文件
├── plugins_func/         # 插件功能
├── schemas/              # 请求与响应数据结构
├── services/             # 服务层逻辑
├── test/                 # 测试页面与静态资源
├── tmp/                  # 临时文件目录
├── docs/                 # 部署文档、接口文档、Postman 等
├── tests/                # 接口测试与压测脚本
├── reports/              # 测试报告与压测报告
├── main.py               # 服务启动入口
├── config.yaml           # 项目配置
└── requirements.txt      # 依赖文件

```

## 部署指南

# 1. 环境要求
Python 3.10 及以上
pip
ffmpeg
2. 安装依赖
```
pip install -r requirements.txt

```
3. 配置文件

项目配置文件为：
```
config.yaml
```
根据实际环境补充或修改所需的模型、ASR、TTS、问答接口配置。

4. 启动服务
```
python main.py
```
或使用 uvicorn 启动：
```
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
5. 访问地址

服务启动后可通过以下地址访问：
```
Swagger UI: http://127.0.0.1:8000/docs
OpenAPI JSON: http://127.0.0.1:8000/openapi.json
```
6. 接口测试

项目支持通过 Swagger UI 直接进行接口测试：

文本接口：直接输入文本参数进行测试
音频接口：上传音频文件进行测试
音频 + TTS 接口：上传音频文件并验证返回结果
