# Q-A-module-decoupling-and-independent-deployment
Phase 3 independent QA service based on FastAPI, supporting text chat, audio chat and audio-tts
# Part3 Xiaozhi QA Service
# 基于 FastAPI 的独立问答服务项目，用于完成第三阶段“问答模块解耦与服务独立部署”任务。
# 项目目标包括提取并独立部署语音问答核心逻辑，提供支持文本/语音问答的 REST API，并补充接口文档、Postman 示例和性能测试。:contentReference[oaicite:0]{index=0}

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
