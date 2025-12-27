# OCS集成使用指南

## 🔗 API集成说明

OCS插件调用题库API时遇到 `Internal Server Error`，通常是以下原因：

### 常见问题

1. **AI服务未配置** - API密钥为空
2. **配置文件不存在** - config.json缺失
3. **配置格式错误** - JSON格式不正确
4. **网络问题** - 无法连接到AI服务

### ✅ 快速修复步骤

#### 1. 检查配置文件

确保 `config.json` 文件存在：

```bash
ls -la config.json
```

如果不存在，创建它：

```bash
cp config.example.json config.json
```

#### 2. 配置AI服务密钥

编辑 `config.json`，至少配置一个AI服务：

```json
{
  "ai": {
    "default_provider": "siliconflow",
    "providers": {
      "siliconflow": {
        "enabled": true,
        "api_key": "sk-your-api-key-here"
      }
    }
  }
}
```

**获取API密钥**：
- 硅基流动: https://cloud.siliconflow.cn/
- 阿里百炼: https://bailian.console.aliyun.com/
- 智谱AI: https://open.bigmodel.cn/

#### 3. 启动服务

```bash
./scripts/dev.sh
```

#### 4. 测试API

在浏览器访问：
```
http://localhost:8000/health
```

应该看到：
```json
{
  "status": "healthy",
  "app_name": "OCS题库系统",
  "version": "2.0.0",
  "environment": "development"
}
```

#### 5. 测试查询API

```bash
curl "http://localhost:8000/api/v1/query?title=测试&type=single"
```

### 🔧 OCS插件配置

在OCS中使用以下配置：

```javascript
{
  "name": "OCS题库(自建版)",
  "url": "http://localhost:8000/api/v1/query",
  "method": "GET",
  "contentType": "json",
  "data": {
    "title": "${title}",
    "options": "${options}",
    "type": "${type}"
  },
  "handler": "return (res)=>res.code === 1 ? [undefined, res.data.data] : [undefined, undefined]"
}
```

### 🐛 调试技巧

#### 查看日志

```bash
tail -f logs/app.log
```

#### 测试单个查询

```bash
# 测试单选题
curl "http://localhost:8000/api/v1/query?title=中国的首都是&type=single"

# 测试判断题
curl "http://localhost:8000/api/v1/query?title=地球是圆的吗&type=judgement"

# 测试填空题
curl "http://localhost:8000/api/v1/query?title=中国的首都是__&type=fill"
```

#### 使用Mock提供商测试（不需要API密钥）

编辑 `config.json`，将provider设为mock：

```json
{
  "ai": {
    "default_provider": "mock"
  }
}
```

这样可以不调用真实AI服务，直接返回模拟答案。

### 📊 支持的题目类型

| 类型 | type参数 | 说明 |
|------|---------|------|
| 单选题 | single | 只有一个正确答案 |
| 多选题 | multiple | 多个正确答案，用###连接 |
| 判断题 | judgement | 对/错判断 |
| 填空题 | fill | 填空，多个空用###连接 |

### ⚡ 性能优化

1. **启用缓存** - 答案会被缓存1小时
2. **本地数据库** - 已查询过的问题直接返回
3. **异步处理** - 支持高并发查询

### 🔗 相关链接

- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health
- 配置指南: [docs/配置指南.md](docs/配置指南.md)

### ❓ 常见错误

#### Error 500: Internal Server Error

**原因**：
1. AI服务未配置或API密钥错误
2. 网络无法连接到AI服务
3. 配置文件格式错误

**解决**：
1. 检查 `config.json` 中的 `api_key` 是否正确
2. 查看日志 `logs/app.log`
3. 使用mock提供商测试

#### Error 400: Bad Request

**原因**：
1. 缺少必需参数 `title`
2. 参数类型错误

**解决**：
1. 确保 `title` 参数不为空
2. 检查 `type` 参数是否为有效值

---

> 如有问题，请查看日志或提交Issue
