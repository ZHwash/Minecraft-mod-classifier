#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub集成模块
提供将mods_data.json提交到GitHub仓库的功能
"""

import subprocess
import sys
from pathlib import Path
from logger import setup_logger
from i18n import i18n

logger = setup_logger()


class GitHubIntegration:
    """GitHub集成管理器"""
    
    def __init__(self):
        self.logger = logger
        self.config_file = Path('config/mods_data.json')
        
    def is_git_repository(self) -> bool:
        """检查当前目录是否是Git仓库"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--git-dir'],
                capture_output=True,
                text=True,
                cwd=Path.cwd()
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def has_uncommitted_changes(self) -> bool:
        """检查是否有未提交的更改"""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain', str(self.config_file)],
                capture_output=True,
                text=True,
                cwd=Path.cwd()
            )
            return len(result.stdout.strip()) > 0
        except Exception:
            return False
    
    def commit_and_push_mods_data(self, message: str = None) -> bool:
        """
        提交并推送mods_data.json到GitHub
        
        Args:
            message: 提交信息，默认为自动生成
            
        Returns:
            是否成功
        """
        if not message:
            # 自动生成提交信息
            import json
            from datetime import datetime
            
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            mod_count = len(data)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            message = f"Update mods_data.json ({mod_count} mods) - {timestamp}"
        
        try:
            # 1. 添加文件到暂存区
            self.logger.info(i18n.get('github_adding_file').format(file=self.config_file.name))
            result = subprocess.run(
                ['git', 'add', str(self.config_file)],
                capture_output=True,
                text=True,
                cwd=Path.cwd()
            )
            if result.returncode != 0:
                self.logger.error(f"Git add failed: {result.stderr}")
                return False
            
            # 2. 提交更改
            self.logger.info(i18n.get('github_committing'))
            result = subprocess.run(
                ['git', 'commit', '-m', message],
                capture_output=True,
                text=True,
                cwd=Path.cwd()
            )
            if result.returncode != 0:
                self.logger.error(f"Git commit failed: {result.stderr}")
                return False
            
            # 3. 推送到远程仓库
            self.logger.info(i18n.get('github_pushing'))
            result = subprocess.run(
                ['git', 'push'],
                capture_output=True,
                text=True,
                cwd=Path.cwd()
            )
            if result.returncode != 0:
                self.logger.error(f"Git push failed: {result.stderr}")
                self.logger.warning(i18n.get('github_push_failed_manual'))
                return False
            
            self.logger.info(i18n.get('github_success'))
            return True
            
        except Exception as e:
            self.logger.error(f"{i18n.get('error')}: {str(e)}")
            return False
    
    def prompt_user_to_submit(self) -> bool:
        """
        提示用户是否提交mods_data.json到GitHub
        
        Returns:
            用户选择的结果
        """
        print("\n" + "="*60)
        print(i18n.get('github_prompt_title'))
        print("="*60)
        print(i18n.get('github_prompt_description'))
        print()
        
        # 检查是否是Git仓库
        if not self.is_git_repository():
            print(f"[WARN] {i18n.get('github_not_git_repo')}")
            return False
        
        # 检查是否有更改
        if not self.has_uncommitted_changes():
            print(f"[INFO] {i18n.get('github_no_changes')}")
            return False
        
        # 询问用户
        while True:
            choice = input(f"\n{i18n.get('github_ask_submit')} (y/n): ").strip().lower()
            if choice in ['y', 'yes', i18n.get('yes'), '是']:
                # 获取自定义提交信息
                custom_message = input(f"{i18n.get('github_ask_message')} (Enter使用默认): ").strip()
                
                if custom_message:
                    success = self.commit_and_push_mods_data(custom_message)
                else:
                    success = self.commit_and_push_mods_data()
                
                if success:
                    print(f"\n[OK] {i18n.get('github_success')}")
                else:
                    print(f"\n[ERROR] {i18n.get('github_failed')}")
                
                return success
                
            elif choice in ['n', 'no', i18n.get('no'), '否']:
                print(f"[INFO] {i18n.get('github_skipped')}")
                return False
            else:
                print(f"[WARN] {i18n.get('invalid_choice')}")


def main():
    """测试函数"""
    github = GitHubIntegration()
    github.prompt_user_to_submit()


if __name__ == "__main__":
    main()
