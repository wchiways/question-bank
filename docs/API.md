# API 使用文档

本文档详细介绍了 OCS 题库系统的所有 API 接口、参数说明、返回格式和使用示例。

## 目录

- [API 概述](#api-概述)
- [基础信息](#基础信息)
- [API 接口](#api-接口)
  - [1. 查询问题答案](#1-查询问题答案)
  - [2. 健康检查](#2-健康检查)
- [请求/响应格式](#请求响应格式)
- [错误处理](#错误处理)
- [使用场景](#使用场景)
- [SDK 和集成](#sdk-和集成)

---

## API 概述

OCS 题库系统基于 RESTful API 设计，提供简单易用的题库查询接口。所有接口返回 JSON 格式数据。

### 核心特性

- **智能查询**: 三级缓存策略（缓存 → 数据库 → AI）
- **异步处理**: 全链路异步，支持高并发
- **自动降级**: AI 服务失败时自动降级到缓存/数据库
- **智能匹配**: 自动匹配选项字母前缀
- **多种题型**: 支持单选、多选、判断、填空

---

## 基础信息

### Base URL

```
http://localhost:8000
```

生产环境请替换为实际域名。

### API 版本

当前版本: `v1`

所有接口路径前缀: `/api/v1`

### 认证方式

当前版本无需认证，生产环境建议添加 API Key 或 JWT 认证。

### 请求头

```http
Content-Type: application/json
Accept: application/json
```

### 速率限制

默认限制: 60 次/分钟

可在 `config.json` 中配置：

```json
{
  "rate_limit": {
    "enabled": true,
    "per_minute": 60
  }
}
```

---

## API 接口

### 1. 查询问题答案

这是系统的核心接口，用于查询问题答案。

#### 接口信息

- **路径**: `/api/v1/query`
- **方法**: `GET`
- **描述**: 查询问题答案，支持缓存、数据库和 AI 智能回答

#### 请求参数（Query Parameters）

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| `title` | string | ✅ | 问题标题 | `中国的首都是哪里？` |
| `options` | string | ❌ | 问题选项 | `A. 北京 B. 上海 C. 广州` |
| `type` | string | ❌ | 题目类型 | `single` (默认) |

#### 题目类型 (type)

| 值 | 说明 | 示例 |
|----|------|------|
| `single` | 单选题（默认） | A. 北京 B. 上海 |
| `multiple` | 多选题 | A. 北京 B. 上海 C. 广州 D. 深圳 |
| `judgement` | 判断题 | 对/错 |
| `fill` | 填空题 | ____是中国的首都 |

#### 请求示例

##### cURL

```bash
# 单选题
curl "http://localhost:8000/api/v1/query?title=中国的首都是哪里？&options=A.北京 B.上海 C.广州&type=single"

# 判断题
curl "http://localhost:8000/api/v1/query?title=地球是圆的&type=judgement"

# 多选题
curl "http://localhost:8000/api/v1/query?title=以下哪些是城市？&options=A.北京 B.桌子 C.上海 D.椅子&type=multiple"

# 填空题
curl "http://localhost:8000/api/v1/query?title=____是中国最大的城市&type=fill"
```

##### Python (requests)

```python
import requests

url = "http://localhost:8000/api/v1/query"
params = {
    "title": "中国的首都是哪里？",
    "options": "A. 北京 B. 上海 C. 广州",
    "type": "single"
}

response = requests.get(url, params=params)
result = response.json()

print(result)
# {'code': 1, 'data': 'A. 北京', 'msg': 'AI回答', 'source': 'ai'}
```

##### JavaScript (fetch)

```javascript
const params = new URLSearchParams({
    title: '中国的首都是哪里？',
    options: 'A. 北京 B. 上海 C. 广州',
    type: 'single'
});

fetch(`http://localhost:8000/api/v1/query?${params}`)
    .then(res => res.json())
    .then(data => {
        console.log(data);
        // {code: 1, data: 'A. 北京', msg: 'AI回答', source: 'ai'}
    });
```

##### Java (OkHttp)

```java
import okhttp3.*;

OkHttpClient client = new OkHttpClient();

HttpUrl url = HttpUrl.parse("http://localhost:8000/api/v1/query").newBuilder()
    .addQueryParameter("title", "中国的首都是哪里？")
    .addQueryParameter("options", "A. 北京 B. 上海 C. 广州")
    .addQueryParameter("type", "single")
    .build();

Request request = new Request.Builder()
    .url(url)
    .get()
    .build();

Response response = client.newCall(request).execute();
```

#### 响应格式

##### 成功响应 (HTTP 200)

```json
{
  "code": 1,
  "data": "A. 北京",
  "msg": "AI回答",
  "source": "ai"
}
```

##### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | int | 状态码：`1`-成功，`0`-失败 |
| `data` | string \| null | 答案内容，失败时为 `null` |
| `msg` | string | 响应消息 |
| `source` | string | 答案来源：`cache`-缓存、`database`-数据库、`ai`-AI服务、`none`-未找到 |

##### 答案来源说明

1. **cache**: 从缓存中获取，速度最快
2. **database**: 从本地数据库获取，速度较快
3. **ai**: 由 AI 服务实时生成，并自动保存到数据库和缓存
4. **none**: 未找到答案（数据库无记录且 AI 调用失败）

##### 失败响应 (HTTP 400/500)

```json
{
  "success": false,
  "error": "标题不能为空"
}
```

##### HTTP 状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 429 | 速率限制超出 |
| 500 | 服务器内部错误 |
| 503 | AI 服务不可用 |

---

### 2. 健康检查

用于监控服务状态，常用于负载均衡器健康检查。

#### 接口信息

- **路径**: `/health`
- **方法**: `GET`
- **描述**: 检查服务健康状态

#### 请求示例

```bash
curl http://localhost:8000/health
```

#### 响应格式

##### 成功响应 (HTTP 200)

```json
{
  "status": "healthy"
}
```

##### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | string | 服务状态：`healthy`-健康 |

---

## 请求/响应格式

### 请求编码

所有请求使用 UTF-8 编码，URL 参数需要正确编码。

### URL 编码示例

```python
import urllib.parse

title = "中国的首都是哪里？"
encoded_title = urllib.parse.quote(title)
# 结果: %E4%B8%AD%E5%9B%BD%E7%9A%84%E9%A6%96%E9%83%BD%E6%98%AF%E5%93%AA%E9%87%8C%EF%BC%9F

url = f"http://localhost:8000/api/v1/query?title={encoded_title}"
```

### 响应时间

- **缓存命中**: < 10ms
- **数据库命中**: < 50ms
- **AI 服务**: 500ms - 3s（取决于 AI 提供商）

---

## 错误处理

### 错误响应格式

```json
{
  "success": false,
  "error": "错误描述信息"
}
```

### 常见错误

#### 1. 参数验证错误 (HTTP 400)

```json
{
  "success": false,
  "error": "标题不能为空"
}
```

**原因**: 标题参数为空或只包含空格

**解决**: 确保 `title` 参数有有效内容

#### 2. 速率限制超出 (HTTP 429)

```json
{
  "success": false,
  "error": "Rate limit exceeded"
}
```

**原因**: 超过每分钟请求次数限制

**解决**:
1. 降低请求频率
2. 在 `config.json` 中提高 `rate_limit.per_minute` 值
3. 实现客户端缓存

#### 3. AI 服务不可用 (HTTP 503)

```json
{
  "code": 0,
  "data": null,
  "msg": "未找到答案",
  "source": "none"
}
```

**原因**:
- AI 服务配置错误
- API Key 无效
- 网络连接失败
- AI 服务商配额用尽

**解决**:
1. 检查 `config.json` 中 AI 配置
2. 验证 API Key 是否有效
3. 检查网络连接
4. 查看日志: `tail -f logs/app.log`
5. 切换到其他 AI 服务商

#### 4. 数据库错误 (HTTP 500)

```json
{
  "success": false,
  "error": "Database connection failed"
}
```

**原因**: 数据库文件权限或路径错误

**解决**:
1. 检查数据库文件权限
2. 确认数据库路径配置正确
3. 确保 `data` 目录存在且有写入权限

---

## 使用场景

### 场景 1: OCS 网课助手集成

在油猴脚本或 OCS 软件中配置自定义题库。

#### 配置格式

```json
{
    "name": "OCS题库(FastAPI版)",
    "homepage": "https://chiway.blog/",
    "url": "http://localhost:8000/api/v1/query",
    "method": "get",
    "type": "GM_xmlhttpRequest",
    "contentType": "json",
    "data": {
        "title": "${title}",
        "options": "${options}",
        "type": "${type}"
    },
    "handler": "return (res)=>res.code === 0 ? [undefined, undefined] : [undefined, res.data]"
}
```

#### 油猴脚本示例

```javascript
// ==UserScript==
// @name         OCS题库自动答题
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  OCS题库自动答题脚本
// @match        https://ocs.example.com/*
// @grant        GM_xmlhttpRequest
// ==/UserScript==

(function() {
    'use strict';

    function queryAnswer(title, options, type) {
        return new Promise((resolve, reject) => {
            const url = `http://localhost:8000/api/v1/query?title=${encodeURIComponent(title)}&options=${encodeURIComponent(options)}&type=${type}`;

            GM_xmlhttpRequest({
                method: 'GET',
                url: url,
                onload: function(response) {
                    const result = JSON.parse(response.responseText);
                    if (result.code === 1) {
                        resolve(result.data);
                    } else {
                        reject(new Error(result.msg));
                    }
                },
                onerror: function(error) {
                    reject(error);
                }
            });
        });
    }

    // 使用示例
    async function autoAnswer() {
        const title = document.querySelector('.question-title').textContent;
        const options = document.querySelector('.question-options').textContent;
        const type = 'single';

        try {
            const answer = await queryAnswer(title, options, type);
            console.log('答案:', answer);
            // 自动选择答案
        } catch (error) {
            console.error('查询失败:', error);
        }
    }
})();
```

### 场景 2: 批量导入题目

```python
import requests
import csv

def batch_import(csv_file):
    """批量导入题目到数据库"""

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            # 调用 API 查询，自动保存到数据库
            params = {
                'title': row['question'],
                'options': row.get('options', ''),
                'type': row.get('type', 'single')
            }

            response = requests.get(
                'http://localhost:8000/api/v1/query',
                params=params
            )

            result = response.json()
            print(f"题目: {row['question']}")
            print(f"答案: {result.get('data')}")
            print(f"来源: {result.get('source')}")
            print("-" * 50)

if __name__ == '__main__':
    batch_import('questions.csv')
```

### 场景 3: 构建问答应用

```python
from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

@app.post("/chat")
async def chat(question: str):
    """问答接口"""

    # 调用题库 API
    response = requests.get(
        'http://localhost:8000/api/v1/query',
        params={'title': question}
    )

    result = response.json()

    if result['code'] == 1:
        return {
            'answer': result['data'],
            'confidence': 'high' if result['source'] == 'database' else 'medium'
        }
    else:
        raise HTTPException(status_code=404, detail='未找到答案')
```

---

## SDK 和集成

### Python SDK

```python
from typing import Optional
import requests

class OCSClient:
    """OCS 题库系统 Python SDK"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.api_endpoint = f"{base_url}/api/v1/query"

    def query(
        self,
        title: str,
        options: Optional[str] = None,
        question_type: str = "single"
    ) -> dict:
        """
        查询问题答案

        Args:
            title: 问题标题
            options: 选项内容
            question_type: 题目类型

        Returns:
            查询结果字典
        """
        params = {
            "title": title,
            "options": options or "",
            "type": question_type
        }

        response = requests.get(self.api_endpoint, params=params)
        response.raise_for_status()

        return response.json()

    def query_single_choice(self, title: str, options: str) -> Optional[str]:
        """查询单选题"""
        result = self.query(title, options, "single")
        return result.get("data") if result.get("code") == 1 else None

    def query_multiple_choice(self, title: str, options: str) -> Optional[str]:
        """查询多选题"""
        result = self.query(title, options, "multiple")
        return result.get("data") if result.get("code") == 1 else None

    def query_judgement(self, title: str) -> Optional[str]:
        """查询判断题"""
        result = self.query(title, "", "judgement")
        return result.get("data") if result.get("code") == 1 else None

# 使用示例
if __name__ == "__main__":
    client = OCSClient()

    # 单选题
    answer = client.query_single_choice(
        "中国的首都是哪里？",
        "A. 北京 B. 上海 C. 广州"
    )
    print(f"答案: {answer}")

    # 判断题
    answer = client.query_judgement("地球是圆的")
    print(f"答案: {answer}")
```

### JavaScript SDK

```javascript
class OCSClient {
    constructor(baseUrl = 'http://localhost:8000') {
        this.baseUrl = baseUrl;
        this.apiEndpoint = `${baseUrl}/api/v1/query`;
    }

    /**
     * 查询问题答案
     * @param {string} title - 问题标题
     * @param {string} options - 选项内容
     * @param {string} type - 题目类型
     * @returns {Promise<Object>} 查询结果
     */
    async query(title, options = '', type = 'single') {
        const params = new URLSearchParams({
            title,
            options,
            type
        });

        const response = await fetch(`${this.apiEndpoint}?${params}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    /**
     * 查询单选题
     */
    async querySingleChoice(title, options) {
        const result = await this.query(title, options, 'single');
        return result.code === 1 ? result.data : null;
    }

    /**
     * 查询多选题
     */
    async queryMultipleChoice(title, options) {
        const result = await this.query(title, options, 'multiple');
        return result.code === 1 ? result.data : null;
    }

    /**
     * 查询判断题
     */
    async queryJudgement(title) {
        const result = await this.query(title, '', 'judgement');
        return result.code === 1 ? result.data : null;
    }
}

// 使用示例
(async () => {
    const client = new OCSClient();

    // 单选题
    const answer = await client.querySingleChoice(
        '中国的首都是哪里？',
        'A. 北京 B. 上海 C. 广州'
    );
    console.log('答案:', answer);

    // 判断题
    const judgement = await client.queryJudgement('地球是圆的');
    console.log('答案:', judgement);
})();
```

---

## 最佳实践

### 1. 客户端缓存

实现客户端缓存，减少重复查询：

```python
import hashlib
import json
from pathlib import Path

class CachedOCSClient:
    def __init__(self, cache_dir='cache'):
        self.client = OCSClient()
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def _get_cache_key(self, title, options, type):
        content = f"{title}|{options}|{type}"
        return hashlib.md5(content.encode()).hexdigest()

    def query(self, title, options='', type='single'):
        cache_key = self._get_cache_key(title, options, type)
        cache_file = self.cache_dir / f"{cache_key}.json"

        # 检查缓存
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)

        # 调用 API
        result = self.client.query(title, options, type)

        # 保存缓存
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False)

        return result
```

### 2. 错误重试

实现智能重试机制：

```python
import time
from functools import wraps

def retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay * (attempt + 1))
            return None
        return wrapper
    return decorator

class RobustOCSClient:
    def __init__(self):
        self.client = OCSClient()

    @retry(max_attempts=3, delay=1)
    def query(self, title, options='', type='single'):
        return self.client.query(title, options, type)
```

### 3. 批量查询优化

```python
import asyncio
import aiohttp

async def query_async(session, title, options='', type='single'):
    url = 'http://localhost:8000/api/v1/query'
    params = {'title': title, 'options': options, 'type': type}

    async with session.get(url, params=params) as response:
        return await response.json()

async def batch_query(questions):
    """批量异步查询"""
    async with aiohttp.ClientSession() as session:
        tasks = [
            query_async(session, q['title'], q.get('options', ''), q.get('type', 'single'))
            for q in questions
        ]
        return await asyncio.gather(*tasks)

# 使用示例
questions = [
    {'title': '问题1', 'options': 'A. xxx B. xxx'},
    {'title': '问题2', 'options': 'A. xxx B. xxx'},
    # ...
]

results = asyncio.run(batch_query(questions))
```

---

## 相关文档

- [安装指南 (INSTALL.md)](./INSTALL.md)
- [开发指南 (DEVELOPMENT.md)](./DEVELOPMENT.md)
- [Docker 部署 (DOCKER.md)](./DOCKER.md)

---

**如有问题，请提交 [Issue](https://github.com/wchiways/question-bank/issues)**
