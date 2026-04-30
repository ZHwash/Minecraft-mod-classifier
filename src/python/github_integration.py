#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub集成模块
提供创建GitHub Issue的功能（可选）
注意：此功能需要GitHub账号和Token，不是必需的
"""

import json
from pathlib import Path
from typing import Optional, Dict, List
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from logger import setup_logger

logger = setup_logger()


class GitHubIntegration:
    """GitHub集成管理器（可选功能）"""
    
    GITHUB_API_URL = "https://api.github.com"
    
    def __init__(self):
        self.logger = logger
        self.repo_info = self._get_repo_info()
    
    def _get_repo_info(self) -> Optional[Dict[str, str]]:
        """
        从git remote获取仓库信息（如果可用）
        
        Returns:
            包含owner和repo的字典，如果无法获取返回None
        """
        import subprocess
        try:
            result = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                capture_output=True,
                text=True,
                cwd=Path.cwd(),
                timeout=5
            )
            if result.returncode != 0:
                return None
            
            remote_url = result.stdout.strip()
            
            # 解析GitHub URL (支持https和ssh格式)
            if 'github.com' in remote_url:
                if remote_url.startswith('git@'):
                    # SSH格式
                    parts = remote_url.split(':')
                    path = parts[1].replace('.git', '')
                else:
                    # HTTPS格式
                    path = remote_url.split('github.com/')[1].replace('.git', '')
                
                parts = path.split('/')
                if len(parts) >= 2:
                    return {
                        'owner': parts[0],
                        'repo': parts[1]
                    }
            
            return None
            
        except Exception:
            # 如果没有git或获取失败，静默返回None
            return None
    
    def create_github_issue(self, title: str, body: str, labels: List[str] = None) -> bool:
        """
        创建GitHub Issue
        
        Args:
            title: Issue标题
            body: Issue内容
            labels: 标签列表
            
        Returns:
            是否成功创建
        """
        if not self.repo_info:
            self.logger.warning("无法获取仓库信息，请确保已配置git remote origin")
            return False
        
        # 需要GitHub Token
        import os
        token = os.environ.get('GITHUB_TOKEN')
        if not token:
            self.logger.warning("未设置GITHUB_TOKEN环境变量，无法创建Issue")
            print("\n提示: 创建GitHub Issue需要设置GITHUB_TOKEN环境变量")
            print("请访问 https://github.com/settings/tokens 生成Personal Access Token")
            print("并设置环境变量: set GITHUB_TOKEN=your_token_here (Windows)")
            print("或: export GITHUB_TOKEN=your_token_here (Linux/Mac)")
            return False
        
        try:
            owner = self.repo_info['owner']
            repo = self.repo_info['repo']
            url = f"{self.GITHUB_API_URL}/repos/{owner}/{repo}/issues"
            
            data = {
                'title': title,
                'body': body
            }
            
            if labels:
                data['labels'] = labels
            
            # 发送请求
            req = Request(url)
            req.add_header('Authorization', f'token {token}')
            req.add_header('Content-Type', 'application/json')
            req.add_header('User-Agent', 'Minecraft-Mod-Classifier/2.0.0')
            req.data = json.dumps(data).encode('utf-8')
            
            with urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode('utf-8'))
                issue_url = result.get('html_url', '')
                issue_number = result.get('number', 0)
                self.logger.info(f"成功创建GitHub Issue #{issue_number}: {issue_url}")
                print(f"\n✅ 成功创建GitHub Issue #{issue_number}")
                print(f"   {issue_url}")
                return True
                
        except HTTPError as e:
            if e.code == 401:
                self.logger.error("GitHub Token无效或已过期")
                print("\n❌ GitHub Token无效或已过期，请重新生成")
            elif e.code == 404:
                self.logger.error("仓库不存在或无权限")
                print("\n❌ 仓库不存在或无权限")
            else:
                self.logger.error(f"HTTP错误 {e.code}: {str(e)}")
            return False
        except URLError as e:
            self.logger.error(f"网络错误: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"创建Issue失败: {str(e)}")
            return False
    
    def generate_issue_content(self, new_mods: List[Dict]) -> tuple:
        """
        生成Issue内容
        
        Args:
            new_mods: 新分类的Mod列表
            
        Returns:
            (title, body) 元组
        """
        from datetime import datetime
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        title = f"自动分类报告 - {timestamp}"
        
        body = f"## 自动分类报告\n\n"
        body += f"**生成时间**: {timestamp}\n\n"
        body += f"**新增分类数量**: {len(new_mods)}\n\n"
        body += f"---\n\n"
        body += f"### 新增Mod分类\n\n"
        body += f"| Mod ID | Mod Name | 类型 |\n"
        body += f"|--------|----------|------|\n"
        
        for mod in new_mods:
            mod_id = mod.get('mod_id', 'N/A')
            mod_name = mod.get('mod_name', 'N/A')
            mod_type = mod.get('type', 'unknown')
            body += f"| {mod_id} | {mod_name} | {mod_type} |\n"
        
        body += f"\n---\n\n"
        body += f"*此Issue由Minecraft Mod Classifier自动生成*\n"
        
        return title, body
    
    def save_issue_to_file(self, title: str, body: str, filename: str = None) -> str:
        """
        将Issue内容保存为Markdown文件，方便用户手动提交
        
        Args:
            title: Issue标题
            body: Issue内容
            filename: 文件名（可选）
            
        Returns:
            保存的文件路径
        """
        if filename is None:
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"github_issue_{timestamp}.md"
        
        filepath = Path(filename)
        
        try:
            content = f"# {title}\n\n{body}"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"Issue内容已保存到: {filepath}")
            print(f"\n📄 Issue内容已保存到: {filepath}")
            print(f"   您可以打开此文件，复制内容到GitHub创建Issue")
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"保存Issue文件失败: {str(e)}")
            return ""


def main():
    """测试函数"""
    github = GitHubIntegration()
    print("GitHubIntegration模块加载成功")
    print(f"仓库信息: {github.repo_info}")


if __name__ == "__main__":
    main()
