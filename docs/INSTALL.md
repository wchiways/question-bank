# 安装指南

本文档提供了 OCS 题库系统的完整安装和配置指南，适用于多种部署环境。

## 目录

- [环境要求](#环境要求)
- [安装方式](#安装方式)
  - [方式一：使用 uv（推荐）](#方式一使用-uv推荐)
  - [方式二：使用 pip](#方式二使用-pip)
  - [方式三：使用 Docker](#方式三使用-docker)
- [配置指南](#配置指南)
- [启动服务](#启动服务)
- [验证安装](#验证安装)
- [常见问题](#常见问题)

---

## 环境要求

### 基础要求

- **操作系统**: Linux / macOS / Windows (WSL2)
- **Python**: 3.11 或更高版本
- **内存**: 至少 512MB 可用内存
- **磁盘**: 至少 100MB 可用空间

### AI 服务要求

本系统需要配置至少一个 AI 服务提供商。目前支持以下平台：

| 平台 | 说明 | 获取 API Key |
|------|------|--------------|
| **硅基流动** (siliconflow) | 性价比高，默认推荐 | [https://siliconflow.cn](https://siliconflow.cn) |
| **阿里百炼** (ali_bailian) | 阿里云大模型平台 | [https://bailian.console.aliyun.com](https://bailian.console.aliyun.com) |
| **智谱AI** (zhipu) | 清华 KEG 实验室 | [https://open.bigmodel.cn](https://open.bigmodel.cn) |
| **火山引擎** (volcengine) | 字节跳动旗下 | [https://console.volcengine.com/ark](https://console.volcengine.com/ark) |
| **Google Studio AI** (google) | Google Gemini | [https://makersuite.google.com](https://makersuite.google.com) |
| **OpenAI** (openai) | GPT 系列模型 | [https://platform.openai.com](https://platform.openai.com) |

---

## 安装方式

### 方式一：使用 uv（推荐）

`uv` 是新一代 Python 包管理器，速度快且资源占用少。

#### 1. 安装 uv

**Linux/macOS**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows**:
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

或使用 pip:
```bash
pip install uv
```

#### 2. 克隆项目

```bash
git clone https://github.com/wchiways/question-bank.git
cd ocs-tiku
```

#### 3. 安装依赖

```bash
uv sync
```

这会自动创建虚拟环境并安装所有依赖。

---

### 方式二：使用 pip

如果您更熟悉传统的 pip 安装方式。

#### 1. 克隆项目

```bash
git clone https://github.com/wchiways/question-bank.git
cd ocs-tiku
```

#### 2. 创建虚拟环境（推荐）

**Linux/macOS**:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows**:
```cmd
python -m venv .venv
.venv\Scripts\activate
```

#### 3. 安装依赖

```bash
pip install -e .
```

或使用 requirements.txt（如果需要）:

```bash
pip install -r requirements.txt
```

#### 4. 安装开发依赖（可选）

如果需要运行测试或开发：

```bash
pip install -e ".[dev]"
```

---

### 方式三：使用 Docker

Docker 部署适合生产环境和需要快速启动的场景。

详细的 Docker 部署指南请参考：[Docker 部署指南 (DOCKER.md)](./DOCKER.md)

快速开始：

```bash
# 1. 创建持久化目录
mkdir -p data logs
chmod 777 data logs

# 2. 配置文件（参考下方配置指南）
cp config.example.json config.json

# 3. 启动容器
docker-compose up -d --build
```

---

## 配置指南

### 1. 创建配置文件

```bash
cp config.example.json config.json
```

### 2. 编辑配置文件

编辑 `config.json`，主要配置以下部分：

#### AI 服务配置（必须）

```json
{
  "ai": {
    "default_provider": "siliconflow",
    "timeout": 30,
    "max_retries": 3,
    "providers": {
      "siliconflow": {
        "enabled": true,
        "api_key": "YOUR_SILICONFLOW_API_KEY",
        "model": "Qwen/QwQ-32B"
      }
    }
  }
}
```

**重要参数说明**:

- `default_provider`: 默认使用的 AI 服务商
- `enabled`: 是否启用该服务商
- `api_key`: **必须替换为你的真实 API Key**
- `model`: 使用的模型名称
- `timeout`: API 请求超时时间（秒）
- `max_retries`: 失败重试次数

#### 数据库配置

默认使用 SQLite，无需额外配置：

```json
{
  "database": {
    "url": "sqlite+aiosqlite:////app/data/question_bank.db",
    "echo": false
  }
}
```

**Docker 用户注意**: 路径必须保持为 `////app/data/question_bank.db`

**本地开发用户**: 可以改为：
```json
{
  "database": {
    "url": "sqlite+aiosqlite:///./question_bank.db"
  }
}
```

#### 服务器配置

```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 8000
  }
}
```

#### 日志配置

```json
{
  "logging": {
    "level": "INFO",
    "file": "logs/app.log",
    "rotation": "10 MB"
  }
}
```

#### 速率限制（可选）

```json
{
  "rate_limit": {
    "enabled": true,
    "per_minute": 60
  }
}
```

---

## 启动服务

### 本地开发模式

#### 方法 1：使用 uv

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 方法 2：使用提供的脚本

```bash
./scripts/dev.sh
```

#### 方法 3：激活虚拟环境后运行

```bash
# 激活虚拟环境
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate     # Windows

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker 模式

```bash
docker-compose up -d
```

---

## 验证安装

### 1. 检查服务状态

访问健康检查端点：

```bash
curl http://localhost:8000/health
```

正常返回：
```json
{"status": "healthy"}
```

### 2. 访问 API 文档

在浏览器中打开：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 3. 测试查询接口

```bash
curl "http://localhost:8000/api/v1/query?title=中国的首都是哪里？&options=A.北京 B.上海 C.广州 D.深圳&type=single"
```

成功返回：
```json
{
  "code": 1,
  "data": "A.北京",
  "msg": "AI回答",
  "source": "ai"
}
```

---

## 常见问题

### Q1: 如何查看 Python 版本？

```bash
python3 --version
# 或
python --version
```

### Q2: uv 安装依赖时出错？

**解决方案**:
1. 确保 Python 版本 >= 3.11
2. 更新 uv 到最新版本：`uv self update`
3. 清理缓存重试：`uv sync --reinstall`

### Q3: AI 调用失败，返回 500 错误？

**可能原因**:
1. API Key 未配置或配置错误
2. 网络连接问题
3. API 服务商配额用完

**解决方案**:
1. 检查 `config.json` 中的 `api_key` 是否正确
2. 确认该服务商已启用 `"enabled": true`
3. 查看日志：`tail -f logs/app.log`
4. 尝试切换到其他 AI 服务商

### Q4: 数据库文件权限错误？

**错误示例**: `unable to open database file`

**解决方案**:

本地开发：
```bash
chmod 644 question_bank.db
```

Docker 环境：
```bash
mkdir -p data logs
chmod 777 data logs
```

### Q5: 端口 8000 已被占用？

**解决方案**: 修改 `config.json` 中的端口配置：

```json
{
  "server": {
    "port": 8080
  }
}
```

或使用其他端口启动：
```bash
uvicorn app.main:app --port 8080
```

### Q6: 如何在后台运行服务？

**使用 nohup**:
```bash
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > logs/server.log 2>&1 &
```

**使用 systemd（生产环境推荐）**:

创建 `/etc/systemd/system/ocs-tiku.service`:

```ini
[Unit]
Description=OCS Question Bank System
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/ocs-tiku
Environment="PATH=/path/to/ocs-tiku/.venv/bin"
ExecStart=/path/to/ocs-tiku/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl start ocs-tiku
sudo systemctl enable ocs-tiku  # 开机自启
```

### Q7: 如何更新到最新版本？

```bash
# 拉取最新代码
git pull origin main

# 更新依赖
uv sync

# 或使用 pip
pip install -e .

# 重启服务
# 如果使用 systemd
sudo systemctl restart ocs-tiku

# 如果使用 Docker
docker-compose up -d --build
```

### Q8: Windows 环境下路径问题？

**问题**: Windows 使用反斜杠 `\`，可能导致路径错误。

**解决方案**:
1. 使用 Python 的原始字符串：`r"C:\path\to\db"`
2. 或使用正斜杠：`"C:/path/to/db"`
3. 推荐使用相对路径：`"./question_bank.db"`

### Q9: 如何开启调试模式？

编辑 `config.json`:

```json
{
  "app": {
    "debug": true
  },
  "logging": {
    "level": "DEBUG"
  },
  "database": {
    "echo": true
  }
}
```

### Q10: 多个 AI 服务商如何配置？

可以同时配置多个服务商，系统会按优先级使用：

```json
{
  "ai": {
    "default_provider": "siliconflow",
    "providers": {
      "siliconflow": {
        "enabled": true,
        "api_key": "YOUR_API_KEY_HERE"
      },
      "zhipu": {
        "enabled": true,
        "api_key": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

当主服务商失败时，系统会自动尝试其他启用的服务商。

---

## 下一步

安装完成后，建议阅读：

- [API 使用文档](./API.md)
- [Docker 部署指南](./DOCKER.md)
- [开发指南](./DEVELOPMENT.md)

## 获取帮助

如有问题，请：

1. 查看 [GitHub Issues](https://github.com/wchiways/question-bank/issues)
2. 发送邮件至：wchiway@163.com
3. 访问博客：[chiway.blog](https://chiway.blog)

---

**祝您使用愉快！** 🎉
