#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minecraft Mod Classifier - Python Version
自动分类 Minecraft Mod 文件的命令行工具
"""

import sys
import json
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
                    # 读取最近生成的增量补丁文件
                    import glob
                    patch_files = glob.glob('rule_update_patch_*.json')
                    
                    if patch_files:
                        # 使用最新的补丁文件
                        latest_patch = max(patch_files, key=lambda x: x)
                        try:
                            with open(latest_patch, 'r', encoding='utf-8') as f:
                                patch_data = json.load(f)
                            
                            # 从补丁中提取新增的Mod
                            new_mods_from_patch = patch_data.get('new_rules', [])
                            
                            if new_mods_from_patch:
                                title, body = github.generate_issue_content(new_mods_from_patch)
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
                                print("\n补丁中没有新增Mod，无需创建Issue")
                        except Exception as e:
                            print(f"\n⚠️ 读取补丁文件失败: {str(e)}")
                            print("   将使用自动检测的Mod列表")
                            # 降级方案：使用原来的方法
                            new_mods = classifier.config_manager.mods_data[-classifier.stats['auto_detected']:]
                            if new_mods:
                                title, body = github.generate_issue_content(new_mods)
                                github.save_issue_to_file(title, body)
                    else:
                        print("\n未找到增量补丁文件，无法生成Issue报告")
                else:
                    print("\n已跳过GitHub Issue创建")
            else:
                print("\n💡 提示: 如果配置了Git远程仓库，可以自动创建GitHub Issue报告新分类的Mod")
        
    except Exception as e:
        logger.error(f"{i18n.get('error')}: {str(e)}", exc_info=True)
        print(f"\n[ERROR] {i18n.get('error')}: {str(e)}")
        input(f"\n{i18n.get('press_enter')}")
        return 1
    
    input(f"\n{i18n.get('press_enter')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
