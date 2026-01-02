# Git 数据库清理指南

## 🎯 目标
从 Git 仓库中删除已提交的数据库文件（*.db），并确保后续不会被再次提交。

## 📋 当前状态
✅ `.gitignore` 已包含数据库文件忽略规则：
- `*.db`
- `question_bank.db`
- `*.db-journal`
- `*.db.backup`

## 🔧 清理步骤

### 步骤 1: 检查 Git 中的数据库文件

```bash
# 查看当前 Git 状态
git status

# 查看已追踪的数据库文件
git ls-files | grep -E "\\.db$"

# 查看提交历史中的数据库文件
git log --all --full-history -- "*.db"
```

### 步骤 2: 从 Git 追踪中移除数据库文件

```bash
# 从 Git 索引中删除（但保留本地文件）
git rm --cached question_bank.db
git rm --cached *.db

# 如果有其他 .db 文件
git rm --cached *.db
```

### 步骤 3: 提交删除操作

```bash
git commit -m "chore: remove database files from git tracking

- Remove *.db files from version control
- Keep .gitignore rules to prevent future commits
- Database files are now excluded from git tracking

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"
```

### 步骤 4: 清理 Git 历史记录（可选）

**警告：此操作会重写 Git 历史，请谨慎操作！**

如果你想从整个 Git 历史中彻底删除数据库文件：

```bash
# 方法1: 使用 git filter-repo（推荐）
git filter-repo --path question_bank.db --invert-paths

# 方法2: 使用 BFG Repo-Cleaner（需要安装）
bfg --delete-files *.db
bfg --strip-blobs-bigger-than 100K

# 清理和优化仓库
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

### 步骤 5: 强制推送（如果已远程）

⚠️ **危险操作** - 只有在你确定要执行时才运行

```bash
# 查看将要推送的差异
git diff origin/main

# 强制推送（会覆盖远程历史）
git push origin main --force

# 或者使用更安全的选项
git push origin main --force-with-lease
```

## ✅ 验证清理结果

### 检查当前状态

```bash
# 1. 确认数据库文件不再被追踪
git status
# 应该看到 question_bank.db 显示为 "not in git tracking"

# 2. 确认 .gitignore 生效
git check-ignore -v question_bank.db
# 应该显示匹配的忽略规则

# 3. 确认历史记录中已删除
git log --all --full-history -- "*.db"
# 应该为空或只显示删除操作的提交
```

### 测试未来提交

```bash
# 创建测试提交
touch test.txt
git add test.txt
git commit -m "test: check gitignore"

# 检查是否包含数据库文件
git ls-files | grep -E "\\.db$"
# 应该为空

# 清理测试
git reset --hard HEAD^
rm test.txt
```

## 🛡️ 防止未来提交

### 检查 .gitignore 配置

确保 `.gitignore` 包含以下规则：

```gitignore
# Database
*.db
*.db-journal
*.db.backup
*.sqlite
*.sqlite3

# 项目特定数据库
question_bank.db
question_bank.db.backup
```

### 添加 pre-commit hook（可选）

创建 `.git/hooks/pre-commit`：

```bash
#!/bin/bash
# 防止提交数据库文件

if git diff --cached --name-only | grep -E "\\.db$"; then
    echo "⚠️  警告: 检测到数据库文件 (*.db)"
    echo "请将这些文件添加到 .gitignore 或使用 git rm --cached"
    exit 1
fi
```

赋予执行权限：
```bash
chmod +x .git/hooks/pre-commit
```

## 📝 后续维护

### 团队成员注意事项

1. **克隆项目后**：
   ```bash
   # 本地会生成空的数据库
   python -c "from app.core.database import init_db; import asyncio; asyncio.run(init_db())"
   ```

2. **更新代码时**：
   ```bash
   git pull
   # 不会影响本地数据库
   ```

3. **提交代码时**：
   ```bash
   # 检查是否意外添加了数据库文件
   git status
   git add .
   git status  # 再次确认
   ```

## 🔧 故障排除

### 问题1: 数据库文件仍然被追踪

**解决方法**：
```bash
# 检查大文件存储
git lfs ls-files

# 如果使用了 Git LFS，取消追踪
git lfs untrack "*.db"
```

### 问题2: 远程仓库仍然有数据库文件

**解决方法**：
```bash
# 清理远程缓存
git fetch origin --prune
git remote prune origin

# 如果问题依旧，强制清理
git branch -D main
git checkout -b main
git push origin main --force
```

### 问题3: 需要共享初始数据库结构

**解决方案**：
```bash
# 方案1: 导出 SQL 结构
sqlite3 question_bank.db .schema > schema.sql

# 方案2: 创建初始化脚本
# scripts/init_db.py
# 包含创建表和初始数据的代码

# 方案3: 使用种子数据
# scripts/seed_db.py
# 导入示例数据用于开发
```

## 📚 参考资料

- [Git - gitignore](https://git-scm.com/docs/gitignore)
- [Git - git-rm](https://git-scm.com/docs/git-rm)
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)
- [git filter-repo](https://github.com/newren/git-filter-repo)

## ⚠️ 重要提醒

1. **备份重要数据** - 在执行任何删除操作前，先备份数据库文件
2. **通知团队** - 清理 Git 历史是团队协作，需要协调所有人重新克隆
3. **测试环境** - 先在测试分支验证，确认无问题后再应用到主分支
4. **文档同步** - 更新团队文档，说明数据库初始化方法
