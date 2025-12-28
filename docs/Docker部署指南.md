# Docker 部署指南

本文档介绍如何使用 Docker 和 Docker Compose 快速部署 OCS 题库系统。

## 1. 环境要求

- 已安装 [Docker](https://docs.docker.com/get-docker/)
- 已安装 [Docker Compose](https://docs.docker.com/compose/install/)

## 2. 快速部署

### 第一步：准备宿主机目录
在项目根目录下创建用于持久化存储数据和日志的文件夹：

```bash
mkdir -p data logs
chmod 777 data logs
```

### 第二步：准备配置文件
如果还没有 `config.json`，请从模板创建并修改：

```bash
cp config.example.json config.json
```

**重要：修改数据库连接字符串**
由于 Docker 内部使用了挂载目录，请确保 `config.json` 中的 `database.url` 指向容器内的绝对路径：

```json
"database": {
  "url": "sqlite+aiosqlite:////app/data/question_bank.db"
}
```
*注意：这里使用了四个斜杠 `////` 表示绝对路径 `/app/data/...`*

### 第三步：启动容器
运行以下命令构建镜像并启动服务：

```bash
docker-compose up -d --build
```

## 3. 访问与验证

- **API 文档 (Swagger)**: `http://localhost:8000/docs`
- **健康检查**: `http://localhost:8000/health`
- **API 查询**: `http://localhost:8000/api/v1/query`

## 4. 常用管理命令

### 查看日志
```bash
docker-compose logs -f
```

### 停止并移除容器
```bash
docker-compose down
```

### 更新应用
如果你修改了代码或更新了仓库，运行：
```bash
git pull
docker-compose up -d --build
```

## 5. 常见问题 (FAQ)

### 1. 数据库文件在哪里？
数据库文件存储在宿主机的 `data/question_bank.db` 中。删除容器不会丢失数据。

### 2. 如何修改 API 端口？
修改 `docker-compose.yml` 中的 `ports` 部分：
```yaml
ports:
  - "9000:8000"  # 将宿主机的 9000 端口映射到容器的 8000
```

### 3. 修改配置后需要重启吗？
是的，修改 `config.json` 后需要重启容器以生效：
```bash
docker-compose restart
```
