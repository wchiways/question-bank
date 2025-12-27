# OCS Handler问题修复指南

## 问题分析

OCS配置中的handler逻辑有问题：
```javascript
"handler": "return (res)=>res.code === 0 ? [undefined, undefined] : [undefined,res.data.data]"
```

**问题**：
1. `code === 0` 表示**失败**，应该返回 undefined
2. `code === 1` 表示**成功**，应该返回 `res.data.data`
3. 逻辑完全反了！

## ✅ 正确的OCS配置

### 修正后的handler

```javascript
{
  "name": "OCS题库(自建版)",
  "homepage": "https://currso.com/",
  "url": "http://localhost:8000/api/v1/query",
  "method": "get",
  "type": "GM_xmlhttpRequest",
  "contentType": "json",
  "data": {
    "title": "${title}",
    "options": "${options}",
    "type": "${type}",
    "api-key": "a702e4dd929b6f38c48d45f15d43d760"
  },
  "handler": "return (res)=>res.code === 1 ? res.data.data : undefined"
}
```

**关键修正**：
- `res.code === 1` → 成功，返回答案
- `res.code === 0` → 失败，返回 undefined
- **不再检查 `res.data.data`**，直接返回 `res.data`

## 📋 响应格式说明

### 成功响应 (code: 1)
```json
{
  "success": true,
  "data": {
    "code": 1,
    "data": "答案内容",
    "msg": "AI回答",
    "source": "ai"
  }
}
```

### 失败响应 (code: 0)
```json
{
  "success": true,
  "data": {
    "code": 0,
    "data": null,
    "msg": "未找到答案",
    "source": "none"
  }
}
```

## 🎯 正确的Handler

### 简单版
```javascript
"handler": "return (res)=>res.code === 1 ? res.data.data : undefined"
```

### 详细版（带错误处理）
```javascript
"handler": "return (res)=>{
  if (res.success && res.data && res.data.code === 1) {
    return res.data.data;
  }
  return undefined;
}"
```

### 完整版（带日志）
```javascript
"handler": "return (res)=>{
  console.log('API响应:', res);
  if (res.success && res.data && res.data.code === 1) {
    console.log('答案:', res.data.data);
    return res.data.data;
  }
  console.log('未找到答案');
  return undefined;
}"
```

## 🔍 调试技巧

### 1. 在浏览器控制台查看响应
```javascript
fetch('http://localhost:8000/api/v1/query?title=测试&type=single')
  .then(r => r.json())
  .then(console.log);
```

### 2. 查看完整的响应结构
```javascript
"handler": "return (res)=>{
  console.log('完整响应:', JSON.stringify(res, null, 2));
  return res.success && res.data?.code === 1 ? res.data.data : undefined;
}"
```

### 3. 检查答案内容
```javascript
"handler": "return (res)=>{
  if (res.data && res.data.code === 1) {
    var answer = res.data.data;
    console.log('答案类型:', typeof answer);
    console.log('答案内容:', answer);
    return answer;
  }
  return undefined;
}"
```

## ⚠️ 常见错误

### 错误1：逻辑反了
```javascript
// ❌ 错误
"handler": "return (res)=>res.code === 0 ? res.data.data : undefined"

// ✅ 正确
"handler": "return (res)=>res.code === 1 ? res.data.data : undefined"
```

### 错误2：嵌套路径错误
```javascript
// ❌ 错误
"handler": "return (res)=>res.code === 1 ? res.data.data.data : undefined"

// ✅ 正确
"handler": "return (res)=>res.code === 1 ? res.data.data : undefined"
```

### 错误3：没有检查success
```javascript
// ❌ 错误
"handler": "return (res)=>res.data.data"

// ✅ 正确
"handler": "return (res)=>res.success && res.data.code === 1 ? res.data.data : undefined"
```

## 📝 推荐配置

```javascript
{
  "name": "OCS题库(自建版)",
  "homepage": "https://currso.com/",
  "url": "http://localhost:8000/api/v1/query",
  "method": "get",
  "type": "GM_xmlhttpRequest",
  "contentType": "json",
  "data": {
    "title": "${title}",
    "options": "${options}",
    "type": "${type}"
  },
  "handler": "return (res)=>res.success && res.data?.code === 1 ? res.data.data : undefined"
}
```

## 🎯 完整OCS配置示例

```javascript
{
  "name": "OCS题库(自建版)",
  "id": "ocs-tiku-custom",
  "icon": "https://example.com/icon.png",
  "homepage": "https://currso.com/",
  "url": "http://localhost:8000/api/v1/query",
  "method": "get",
  "type": "GM_xmlhttpRequest",
  "contentType": "json",
  "dataType": "json",
  "data": {
    "title": "${title}",
    "options": "${options}",
    "type": "${type}",
    "api-key": "a702e4dd929b6f38c48d45f15d43d760"
  },
  "handler": "return (res)=>{
    if (res.success && res.data && res.data.code === 1) {
      return res.data.data;
    }
    return undefined;
  }",
  "success": "res?.success === true && res?.data?.code === 1",
  "error": "res?.success === false || res?.data?.code === 0"
}
```

## 🚀 验证步骤

1. **更新OCS配置**
   - 使用上面的推荐配置
   - 特别注意 handler 部分

2. **测试查询**
   - 在OCS中查询一个简单问题
   - 查看浏览器控制台的日志

3. **检查答案**
   - 答案应该直接显示，不应该有额外的文本
   - 如果未找到答案，应该显示为空

4. **查看日志**
   - 打开浏览器开发者工具 → Console
   - 查看API响应和答案内容

---

> **提示**：如果问题有多个正确答案（如"算法的特征"），AI会返回所有用###连接的正确答案。这是正确的行为！
