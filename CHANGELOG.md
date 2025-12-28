# 更新日志 (Changelog)

本文档记录OCS题库系统的所有重要更改。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [未发布]

### 计划中
- Docker 容器化部署支持
- 更多AI提供商集成
- 用户反馈系统
- 题目导出功能

## [1.2.1] - 2025-12-28

### 新增
- ✨ 新增火山引擎 (Volcengine) AI提供商支持
- 🔐 在配置示例中添加管理员账户配置项
- 📝 在README中添加默认管理员账户说明和安全提示
- 📚 添加首次使用指南

### 改进
- 🎨 优化管理后台提供商配置页面的提示文本
- 📱 更新API URL和模型输入的示例，更加清晰易懂

### 文档
- 📖 添加关于修改默认密码的安全警告

## [1.2.0] - 2025-12-28

### 🎉 重大更新

### 新增
- ✨ **全新的管理后台**
  - 基于 React 19 + TypeScript 构建
  - 使用 Ant Design 6 UI 组件库
  - 采用 Vite 7 构建工具
  - 集成 Tailwind CSS 样式系统
  - 支持响应式设计，移动端友好

- 🔑 **API密钥管理系统**
  - 完整的密钥创建、删除、查看功能
  - 密钥使用次数追踪
  - 最后使用时间记录
  - 通过API密钥进行请求认证

- 📊 **日志与统计分析**
  - 详细的AI调用日志记录
  - 提供商使用统计
  - 每日调用趋势分析
  - 平均响应时间追踪
  - 错误日志记录

- 🎛️ **管理后台功能**
  - 仪表盘 (Dashboard) - 系统概览
  - API密钥管理 (Keys) - 密钥CRUD操作
  - 提供商配置 (Providers) - AI服务配置
  - 调用日志 (Logs) - 请求历史查看
  - 数据分析 (Analysis) - 趋势图表
  - 系统设置 (Settings) - 配置管理
  - AI测试场 (Playground) - 实时测试AI响应

### 改进
- 🚀 性能优化：管理后台使用现代化前端技术栈
- 🔒 安全改进：使用API密钥替代硬编码认证
- 📚 文档完善：添加管理后台使用说明
- 🗂️ 项目结构优化：前端与后端分离

### 移除
- 🗑️ 清理旧的 question_bank.db 数据库文件
- ❌ 删除根目录重复的 package.json
- 🧹 移除 ocs-tiku.spec 打包配置文件

### 技术栈更新

**管理后台**
- React 19.2.0
- TypeScript 5.9.3
- Ant Design 6.1.2
- Vite 7.2.4
- Tailwind CSS 3.4.0
- React Router DOM 7.11.0
- Recharts 3.6.0

**后端新增**
- API密钥数据模型 (ApiKey)
- 日志数据模型 (CallLog)
- 统计数据模型 (ProviderStats)
- 相应的Repository层

### 文档
- 📖 更新README，添加管理后台章节
- 📖 添加管理后台启动和使用说明
- 📖 更新项目结构说明
- 📖 添加OCS网课助手配置示例（含API密钥）

## [1.1.0] - 2025-12-27

### 新增
- ✨ 智能选项匹配功能：优化AI回答与选项的匹配逻辑
- 🌐 多AI提供商支持：
  - 硅基流动 (SiliconFlow)
  - 阿里百炼 (Ali Bailian)
  - 智谱AI (Zhipu AI)
  - Google Studio AI
  - OpenAI

### 改进
- ⚡ 性能优化：从Flask迁移到FastAPI，并发处理能力提升50倍
- 🎯 AI提示词优化：提高答案准确性
- 🔄 自动重试机制：AI调用失败时自动重试
- 📊 响应时间优化：从~100ms降低到<50ms

### 配置
- 🔧 从 .env 配置迁移到 config.json
- 📝 支持多个AI提供商配置
- ⚙️ 可配置默认提供商、最大token数、温度参数等

### 文档
- 📚 添加AI提供商配置指南
- 📚 添加OCS集成故障排除指南
- 📚 添加开发脚本和文档

## [1.0.0] - 2025-12-26

### 🎉 首个正式版本

### 新增
- 🚀 基于FastAPI的异步架构
- 📦 完整的分层设计（API -> Service -> Repository）
- 🎯 题库查询核心功能
- 🤝 OCS网课助手集成支持
- 📖 自动生成API文档（Swagger UI + ReDoc）
- 🔒 Pydantic数据验证
- 📝 结构化日志系统

### 技术栈
- FastAPI 0.127+
- SQLModel (Pydantic + SQLAlchemy)
- SQLite (aiosqlite异步驱动)
- httpx (异步HTTP客户端)
- loguru (日志)
- uv (包管理)

### 架构
- 清晰的分层架构
- API路由层
- 业务逻辑层
- 数据访问层
- 外部服务提供商层

### 文档
- README.md 完整文档
- 开发指南
- API使用示例

---

## 版本说明

### 版本号规则
- **主版本号**：不兼容的API变更
- **次版本号**：向下兼容的新增功能
- **修订号**：向下兼容的问题修复

### 更新类型标识
- **新增** - 新功能
- **改进** - 现有功能的改进
- **修复** - 问题修复
- **移除** - 功能移除
- **安全** - 安全相关修复或改进
- **文档** - 文档更新

### 升级指南

#### 从 1.1.x 升级到 1.2.0
1. 拉取最新代码
2. 安装管理后台依赖：
   ```bash
   cd admin
   npm install
   ```
3. 启动管理后台：
   ```bash
   npm run dev
   ```
4. 使用默认管理员账户登录（admin/admin123）
5. 创建API密钥用于认证
6. 更新OCS网课助手配置，添加API密钥参数

#### 从 1.0.x 升级到 1.1.0
1. 拉取最新代码
2. 迁移配置：
   - 复制 `.env` 中的配置到 `config.json`
   - 添加多个AI提供商配置
3. 运行依赖更新：`uv sync`
4. 重启服务

## 贡献

欢迎提交Issue和Pull Request来帮助改进项目！

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件
