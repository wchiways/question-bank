"""OCS题库系统启动器 - 自动检测配置并显示OCS配置代码"""
import sys
import os
import json
from pathlib import Path


def check_and_create_config():
    """检查并创建config.json文件"""
    # 获取可执行文件所在目录
    if getattr(sys, 'frozen', False):
        # 打包后的exe环境
        base_dir = Path(sys.executable).parent
    else:
        # 开发环境
        base_dir = Path(__file__).parent

    config_file = base_dir / "config.json"
    config_example = base_dir / "config.example.json"

    # 检查config.json是否存在
    if not config_file.exists():
        print("=" * 70)
        print("⚠️  未找到 config.json 文件")
        print("=" * 70)

        # 尝试从config.example.json复制
        if config_example.exists():
            print("📋 正在从 config.example.json 创建 config.json...")
            try:
                with open(config_example, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
                print("✅ config.json 创建成功!")
                print(f"📍 位置: {config_file}")
                print("\n⚠️  请编辑 config.json 填入您的API密钥!")
            except Exception as e:
                print(f"❌ 创建失败: {e}")
                print("请手动创建 config.json 文件")
                sys.exit(1)
        else:
            print("❌ 未找到 config.example.json 文件")
            print("请手动创建 config.json 文件")
            sys.exit(1)
    else:
        print("=" * 70)
        print("✅ config.json 已存在")
        print("=" * 70)

    return config_file


def show_ocs_config(config_file):
    """显示OCS配置代码"""
    # 读取配置获取端口号
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        port = config.get('server', {}).get('port', 8000)
    except:
        port = 8000

    print("\n" + "=" * 70)
    print("📱 OCS网课助手配置代码")
    print("=" * 70)
    print()
    print("请将以下配置添加到 OCS网课助手 → 自定义题库:")
    print()
    print("─" * 70)
    ocs_config = f'''{{
  "name": "OCS题库(自建版)",
  "homepage": "https://chiway.blog/",
  "url": "http://localhost:{port}/api/v1/query",
  "method": "get",
  "type": "GM_xmlhttpRequest",
  "contentType": "json",
  "data": {{
    "title": "${{title}}",
    "options": "${{options}}",
    "type": "${{type}}"
  }},
  "handler": "return (res)=>res.code === 1 ? [undefined, res.data] : [undefined, undefined]"
}}'''
    print(ocs_config)
    print("─" * 70)
    print()
    print("📋 使用说明:")
    print("1. 打开OCS网课助手")
    print("2. 进入: 题库管理 → 自定义题库 → 添加")
    print("3. 将上方配置代码粘贴到配置区域")
    print("4. 保存并启用该题库")
    print()
    print("=" * 70)


def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("🎓 OCS题库系统 v2.0")
    print("=" * 70)

    # 检查并创建配置
    config_file = check_and_create_config()

    # 显示OCS配置
    show_ocs_config(config_file)

    # 启动FastAPI应用
    print("\n🚀 正在启动服务...")
    print("-" * 70)

    # 导入并启动应用
    from app.main import app
    import uvicorn

    # 从配置文件读取设置
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        host = config.get('server', {}).get('host', '0.0.0.0')
        port = config.get('server', {}).get('port', 8000)
        reload = config.get('app', {}).get('debug', False)
    except:
        host = '0.0.0.0'
        port = 8000
        reload = False

    # 启动服务
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )


if __name__ == "__main__":
    main()
