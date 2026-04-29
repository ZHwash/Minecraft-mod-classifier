#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
国际化 (i18n) 模块
支持中文和英文界面
"""

import json
import os
from pathlib import Path


class I18nManager:
    """国际化管理器"""
    
    def __init__(self):
        self.current_language = 'zh'  # 默认中文
        self.translations = {
            'zh': {
                # 程序信息
                'app_name': 'Minecraft Mod 分类器',
                'app_version': 'v2.0.0',
                'app_description': '自动分类 Minecraft Mod 文件的命令行工具',
                
                # 启动信息
                'starting': '正在启动...',
                'checking_python': '检查Python环境...',
                'python_version': 'Python版本',
                
                # 目录操作
                'creating_dirs': '创建必要目录...',
                'dir_created': '目录已创建',
                'input_dir': 'Input',
                'output_dir': 'Output',
                
                # 分类文件夹名称
                'client_only': '仅客户端',
                'server_only': '仅服务端',
                'client_required_server_optional': '客户端必需-服务端可选',
                'client_optional_server_required': '客户端可选-服务端必需',
                'client_and_server_required': '客户端和服务端必需',
                'client_optional_server_optional': '客户端和服务端可选',
                'unknown': '未知类型',
                
                # 处理过程
                'scanning_input': '扫描Input目录...',
                'found_files': '找到 {} 个Mod文件',
                'processing': '正在处理',
                'classified_as': '分类为',
                'copied_to': '已复制到',
                
                # 状态信息
                'success': '成功',
                'warning': '警告',
                'error': '错误',
                'info': '信息',
                'completed': '完成',
                'total_processed': '共处理 {} 个文件',
                'total_success': '成功 {} 个',
                'total_failed': '失败 {} 个',
                
                # JAR解析
                'parsing_jar': '解析JAR配置文件...',
                'detected_type': '检测到Mod类型',
                'saving_config': '保存配置到数据库...',
                'config_saved': '配置已保存',
                
                # 提示信息
                'press_enter': '按回车键退出...',
                'no_files_found': 'Input目录中未找到Mod文件',
                'unknown_mod': '未知的Mod类型，请手动分类',
                'file_exists': '文件已存在，跳过',
                
                # 设置相关
                'language_setting': '语言设置',
                'select_language': '选择语言 / Select Language',
                'chinese': '中文',
                'english': 'English',
                'current_language': '当前语言',
                'language_changed': '语言已切换',
                'yes': '是',
                'no': '否',
                'invalid_choice': '无效选择',
                
                # GitHub集成
                'github_prompt_title': '📤 提交到GitHub',
                'github_prompt_description': '是否将更新后的mods_data.json提交到GitHub仓库?\n这将帮助社区共享Mod分类数据。',
                'github_not_git_repo': '当前目录不是Git仓库,无法提交',
                'github_no_changes': 'mods_data.json没有未提交的更改',
                'github_ask_submit': '是否提交到GitHub?',
                'github_ask_message': '请输入提交信息',
                'github_adding_file': '正在添加文件: {file}',
                'github_committing': '正在提交...',
                'github_pushing': '正在推送到远程仓库...',
                'github_success': '✅ 成功提交到GitHub!',
                'github_failed': '❌ 提交失败',
                'github_push_failed_manual': '推送失败,请手动执行 git push',
                'github_skipped': '已跳过提交',
            },
            'en': {
                # App info
                'app_name': 'Minecraft Mod Classifier',
                'app_version': 'v2.0.0',
                'app_description': 'Command-line tool for automatically classifying Minecraft Mod files',
                
                # Startup
                'starting': 'Starting...',
                'checking_python': 'Checking Python environment...',
                'python_version': 'Python version',
                
                # Directory operations
                'creating_dirs': 'Creating necessary directories...',
                'dir_created': 'Directory created',
                'input_dir': 'Input',
                'output_dir': 'Output',
                
                # Classification folder names
                'client_only': 'ClientOnly',
                'server_only': 'ServerOnly',
                'client_required_server_optional': 'ClientRequiredServerOptional',
                'client_optional_server_required': 'ClientOptionalServerRequired',
                'client_and_server_required': 'ClientAndServerRequired',
                'client_optional_server_optional': 'ClientOptionalServerOptional',
                'unknown': 'Unknown',
                
                # Processing
                'scanning_input': 'Scanning Input directory...',
                'found_files': 'Found {} mod files',
                'processing': 'Processing',
                'classified_as': 'Classified as',
                'copied_to': 'Copied to',
                
                # Status
                'success': 'Success',
                'warning': 'Warning',
                'error': 'Error',
                'info': 'Info',
                'completed': 'Completed',
                'total_processed': 'Total processed: {} files',
                'total_success': 'Success: {}',
                'total_failed': 'Failed: {}',
                
                # JAR parsing
                'parsing_jar': 'Parsing JAR configuration...',
                'detected_type': 'Detected mod type',
                'saving_config': 'Saving configuration to database...',
                'config_saved': 'Configuration saved',
                
                # Messages
                'press_enter': 'Press Enter to exit...',
                'no_files_found': 'No mod files found in Input directory',
                'unknown_mod': 'Unknown mod type, please classify manually',
                'file_exists': 'File already exists, skipped',
                
                # Settings
                'language_setting': 'Language Setting',
                'select_language': '选择语言 / Select Language',
                'chinese': '中文',
                'english': 'English',
                'current_language': 'Current language',
                'language_changed': 'Language changed',
                'yes': 'Yes',
                'no': 'No',
                'invalid_choice': 'Invalid choice',
                
                # GitHub Integration
                'github_prompt_title': '📤 Submit to GitHub',
                'github_prompt_description': 'Submit the updated mods_data.json to GitHub repository?\nThis helps the community share mod classification data.',
                'github_not_git_repo': 'Current directory is not a Git repository, cannot commit',
                'github_no_changes': 'No uncommitted changes in mods_data.json',
                'github_ask_submit': 'Submit to GitHub?',
                'github_ask_message': 'Enter commit message',
                'github_adding_file': 'Adding file: {file}',
                'github_committing': 'Committing...',
                'github_pushing': 'Pushing to remote repository...',
                'github_success': '✅ Successfully committed to GitHub!',
                'github_failed': '❌ Commit failed',
                'github_push_failed_manual': 'Push failed, please run git push manually',
                'github_skipped': 'Skipped submission',
            }
        }
        
        # 尝试加载用户设置
        self._load_settings()
    
    def _load_settings(self):
        """加载用户设置"""
        settings_file = Path('config/settings.json')
        if settings_file.exists():
            try:
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.current_language = settings.get('language', 'zh')
            except Exception:
                pass
    
    def save_settings(self):
        """保存用户设置"""
        settings_file = Path('config/settings.json')
        settings_file.parent.mkdir(parents=True, exist_ok=True)
        
        settings = {
            'language': self.current_language
        }
        
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
    
    def set_language(self, lang):
        """设置语言"""
        if lang in ['zh', 'en']:
            self.current_language = lang
            self.save_settings()
            return True
        return False
    
    def get(self, key, default=None):
        """获取翻译文本"""
        lang_data = self.translations.get(self.current_language, {})
        return lang_data.get(key, default or key)
    
    def get_folder_name(self, category):
        """获取分类文件夹名称"""
        folder_mapping = {
            'client_only': self.get('client_only'),
            'server_only': self.get('server_only'),
            'client_required_server_optional': self.get('client_required_server_optional'),
            'client_optional_server_required': self.get('client_optional_server_required'),
            'client_and_server_required': self.get('client_and_server_required'),
            'client_optional_server_optional': self.get('client_optional_server_optional'),
            'unknown': self.get('unknown'),
        }
        return folder_mapping.get(category, category)
    
    def select_language_interactive(self):
        """交互式选择语言"""
        print("\n" + "="*50)
        print(self.get('select_language'))
        print("="*50)
        print("1. 中文 (Chinese)")
        print("2. English")
        print("="*50)
        
        choice = input("请选择 / Please select (1/2): ").strip()
        
        if choice == '1':
            self.set_language('zh')
        elif choice == '2':
            self.set_language('en')
        else:
            print(f"{self.get('current_language')}: {self.get('chinese') if self.current_language == 'zh' else self.get('english')}")
            return
        
        # 使用ASCII字符避免编码问题
        print(f"[OK] {self.get('language_changed')}")
        print(f"  {self.get('current_language')}: {self.get('chinese') if self.current_language == 'zh' else self.get('english')}")

# 全局实例
i18n = I18nManager()
