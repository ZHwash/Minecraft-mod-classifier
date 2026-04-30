#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minecraft Mod Classifier - Python Version
自动分类 Minecraft Mod 文件的命令行工具
"""

import sys
from pathlib import Path
from mod_classifier import ModClassifier
from logger import setup_logger
from i18n import i18n
from github_integration import GitHubIntegration


def main():
    """主函数"""
    # 首次运行时询问语言设置
    settings_file = Path('config/settings.json')
    if not settings_file.exists():
        i18n.select_language_interactive()
    
    # 设置日志
    logger = setup_logger()
    
    # 显示启动信息
    print("\n" + "="*60)
    print(f"  {i18n.get('app_name')} {i18n.get('app_version')}")
    print(f"  {i18n.get('app_description')}")
    print("="*60)
    print(f"  {i18n.get('current_language')}: {i18n.get('chinese') if i18n.current_language == 'zh' else i18n.get('english')}")
    print("="*60 + "\n")
    
    logger.info("程序启动")
    
    try:
        # 创建分类器实例
        classifier = ModClassifier()
        
        # 确保输入输出目录存在
        classifier.ensure_directories()
        
        # 加载或创建配置文件
        classifier.load_or_create_config()
        
        # 执行分类
        classifier.classify_mods()
        
        logger.info(i18n.get('completed'))
        print(f"\n[OK] {i18n.get('completed')}")
        
        # 询问是否创建GitHub Issue（可选功能）
        if classifier.stats['auto_detected'] > 0:
            github = GitHubIntegration()
            if github.repo_info:
                print("\n" + "="*60)
                print("📋 GitHub Issue 报告（可选）")
                print("="*60)
                print(f"本次分类新增了 {classifier.stats['auto_detected']} 个Mod")
                print("可以创建一个GitHub Issue来记录这些新分类。")
                print("注意：这需要GitHub账号和Personal Access Token\n")
                
                choice = input("是否创建GitHub Issue? (y/n): ").strip().lower()
                if choice in ['y', 'yes', '是']:
                    # 获取新分类的Mod列表
                    new_mods = classifier.config_manager.mods_data[-classifier.stats['auto_detected']:]
                    if new_mods:
                        title, body = github.generate_issue_content(new_mods)
                        success = github.create_github_issue(
                            title, 
                            body, 
                            labels=['automation', 'mod-classification']
                        )
                        if not success:
                            # 如果API提交失败，提供保存文件的选项
                            print("\n💡 提示: 您可以选择将Issue内容保存为文件，然后手动提交")
                            save_choice = input("是否保存Issue内容为Markdown文件? (y/n): ").strip().lower()
                            if save_choice in ['y', 'yes', '是']:
                                github.save_issue_to_file(title, body)
                    else:
                        print("\n没有新分类的Mod，无需创建Issue")
                else:
                    print("\n已跳过GitHub Issue创建")
            else:
                print("\n💡 提示: 如果配置了Git远程仓库，可以自动创建GitHub Issue报告新分类的Mod")
        
        # 提示生成规则更新补丁（更简单的贡献方式）
        if classifier.stats['auto_detected'] > 0 or True:  # 总是提示，因为可能有更新
            print("\n" + "="*60)
            print("🔄 规则数据库更新（推荐）")
            print("="*60)
            print("您可以帮助改进分类规则数据库！")
            print("我们可以生成一个更新补丁文件，您只需将其提交到GitHub即可。")
            print("无需任何技术知识，小白也能轻松贡献！\n")
            
            patch_choice = input("是否生成规则更新补丁文件? (y/n): ").strip().lower()
            if patch_choice in ['y', 'yes', '是']:
                from generate_patch import generate_incremental_patch
                patch_file = generate_incremental_patch()
                if patch_file:
                    print(f"\n✅ 增量补丁文件已生成: {patch_file}")
                    print(f"   提交方式：")
                    print(f"   1. 通过GitHub Issue提交补丁内容")
                    print(f"   2. 维护者使用 apply_patch.py 自动合并")
            else:
                print("\n已跳过补丁生成")
        
    except Exception as e:
        logger.error(f"{i18n.get('error')}: {str(e)}", exc_info=True)
        print(f"\n[ERROR] {i18n.get('error')}: {str(e)}")
        input(f"\n{i18n.get('press_enter')}")
        return 1
    
    input(f"\n{i18n.get('press_enter')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
