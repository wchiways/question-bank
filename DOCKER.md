# Docker 部署指南

本文档详细介绍了如何使用 Docker 和 Docker Compose 快速部署并运行 OCS 题库系统。

## 1. 环境准备

确保您的系统中已安装以下软件：
- **Docker**: [安装指南](https://docs.docker.com/get-docker/)
- **Docker Compose**: [安装指南](https://docs.docker.com/compose/install/)

## 2. 快速开始

### 步骤 A：创建持久化目录
在项目根目录下创建 `data` 和 `logs` 目录，并确保容器有权限写入：

```bash
mkdir -p data logs
chmod 777 data logs
```

### 步骤 B：配置参数
1. 从模板创建 `config.json`：
   ```bash
   cp config.example.json config.json
   ```
2. **重要**：编辑 `config.json`，确保数据库连接指向容器内的挂载路径：
   ```json
   "database": {
     "url": "sqlite+aiosqlite:////app/data/question_bank.db"
   }
   ```
   *注意：四个斜杠 `////` 表示容器内的绝对路径。*

### 步骤 C：启动服务
在包含 `docker-compose.yml` 的目录下运行：

```bash
docker-compose up -d --build
```

## 3. 访问与验证

- **API 接口**: `http://localhost:8000/api/v1/query`
- **自动文档 (Swagger)**: `http://localhost:8000/docs`
- **健康检查**: `http://localhost:8000/health`

## 4. 常用管理命令

| 命令 | 说明 |
| :--- | :--- |
| `docker-compose logs -f` | 查看实时日志 |
| `docker-compose restart` | 重启服务（修改配置后需执行） |
| `docker-compose down` | 停止并移除容器 |
| `docker-compose ps` | 查看容器运行状态 |

## 5. 常见问题排查

### 1. 数据库连接失败
如果看到 `unable to open database file`，请检查：
- `data` 目录是否存在且权限为 777。
- `config.json` 中的路径是否使用了容器内的绝对路径 `/app/data/...`。

### 2. 修改配置未生效
修改 `config.json` 后，必须运行 `docker-compose restart` 才能让容器加载新配置。

### 3. 如何更新到最新版本
```bash
git pull
docker-compose up -d --build
```
