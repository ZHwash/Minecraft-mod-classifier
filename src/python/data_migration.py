#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据转正工具
将mods_data.json中的配置数据转入mod_rules.json规则数据库

用途：
1. 在全部分类完成后，将临时配置转正为永久规则
2. 自动添加mod_name字段（从JAR解析获取）
3. 生成详细的分类原因说明
"""

import json
from pathlib import Path
from typing import List, Dict
from logger import setup_logger
from jar_parser import JarParser
from i18n import i18n

logger = setup_logger()


class DataMigrationTool:
    """数据迁移工具"""
    
    def __init__(self, 
                 mods_data_path: str = "config/mods_data.json",
                 mod_rules_path: str = "config/mod_rules.json",
                 input_dir: str = "Input"):
        """
        初始化工具
        
        Args:
            mods_data_path: mods_data.json路径
            mod_rules_path: mod_rules.json路径
            input_dir: Input目录路径（用于重新解析JAR获取mod_name）
        """
        self.mods_data_path = Path(mods_data_path)
        self.mod_rules_path = Path(mod_rules_path)
        self.input_dir = Path(input_dir)
        self.jar_parser = JarParser()
        self.logger = logger
    
    def load_mods_data(self) -> List[Dict]:
        """加载mods_data.json"""
        if not self.mods_data_path.exists():
            self.logger.error(f"文件不存在: {self.mods_data_path}")
            return []
        
        try:
            with open(self.mods_data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.logger.info(f"成功加载 {len(data)} 条mods_data记录")
            return data
            
        except Exception as e:
            self.logger.error(f"加载mods_data.json失败: {str(e)}")
            return []
    
    def load_mod_rules(self) -> Dict:
        """加载mod_rules.json"""
        if not self.mod_rules_path.exists():
            self.logger.warning(f"规则文件不存在，将创建新文件: {self.mod_rules_path}")
            return {
                "version": "1.0.0",
                "description": "Mod分类规则数据库 - 从历史配置转换而来",
                "rules": []
            }
        
        try:
            with open(self.mod_rules_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.logger.info(f"成功加载 {len(data.get('rules', []))} 条规则")
            return data
            
        except Exception as e:
            self.logger.error(f"加载mod_rules.json失败: {str(e)}")
            return {
                "version": "1.0.0",
                "description": "Mod分类规则数据库",
                "rules": []
            }
    
    def get_mod_name_from_jar(self, mod_id: str) -> str:
        """
        从Input目录中的JAR文件解析mod_name
        
        Args:
            mod_id: Mod ID
            
        Returns:
            Mod名称，如果未找到返回空字符串
        """
        # 在Input目录中搜索包含mod_id的JAR文件
        if not self.input_dir.exists():
            return ''
        
        for jar_file in self.input_dir.glob('*.jar'):
            try:
                mod_info = self.jar_parser.parse_jar(jar_file)
                if mod_info and mod_info.get('mod_id', '').lower() == mod_id.lower():
                    return mod_info.get('mod_name', '')
            except Exception:
                continue
        
        return ''
    
    def generate_reason(self, mod_type: str, mod_name: str = '') -> str:
        """
        生成分类原因说明
        
        Args:
            mod_type: Mod类型
            mod_name: Mod名称
            
        Returns:
            原因说明文本
        """
        type_descriptions = {
            'client_only': '仅客户端需要，通常为界面优化、HUD、小地图等',
            'server_only': '仅服务端需要，通常为管理工具、性能优化等',
            'client_required_server_optional': '客户端必装，服务端可选，通常为JEI等辅助工具',
            'client_optional_server_required': '客户端可选，服务端必装，通常为世界生成Mod',
            'client_and_server_required': '两端都必须安装，通常为内容Mod、生物、物品等',
            'client_optional_server_optional': '两端都可选，通常为配置库、API库等',
            'unknown': '无法自动识别，需手动确认'
        }
        
        base_reason = type_descriptions.get(mod_type, '未知类型')
        
        if mod_name:
            return f"{base_reason} (Mod: {mod_name})"
        else:
            return base_reason
    
    def migrate_data(self, auto_detect_names: bool = True) -> bool:
        """
        执行数据迁移
        
        Args:
            auto_detect_names: 是否自动从JAR解析mod_name
            
        Returns:
            是否成功
        """
        print("\n" + "="*60)
        print("开始数据转正流程")
        print("="*60)
        
        # 1. 加载数据
        mods_data = self.load_mods_data()
        if not mods_data:
            self.logger.error("没有可迁移的数据")
            return False
        
        mod_rules = self.load_mod_rules()
        existing_rules = {rule['mod_id'].lower(): rule for rule in mod_rules.get('rules', [])}
        
        # 2. 转换数据
        new_rules = []
        updated_count = 0
        skipped_count = 0
        
        for mod_entry in mods_data:
            mod_id = mod_entry.get('mod_id', '')
            mod_type = mod_entry.get('type', 'unknown')
            mod_name = mod_entry.get('mod_name', '')
            
            if not mod_id:
                self.logger.warning(f"跳过无效条目: {mod_entry}")
                skipped_count += 1
                continue
            
            # 检查是否已存在
            if mod_id.lower() in existing_rules:
                self.logger.debug(f"规则已存在，跳过: {mod_id}")
                skipped_count += 1
                continue
            
            # 如果没有mod_name且启用了自动检测，尝试从JAR解析
            if not mod_name and auto_detect_names:
                self.logger.info(f"正在解析 {mod_id} 的mod_name...")
                mod_name = self.get_mod_name_from_jar(mod_id)
                if mod_name:
                    self.logger.info(f"  找到mod_name: {mod_name}")
            
            # 生成规则
            reason = self.generate_reason(mod_type, mod_name)
            
            rule = {
                "mod_id": mod_id,
                "mod_name": mod_name,
                "type": mod_type,
                "reason": reason
            }
            
            new_rules.append(rule)
            updated_count += 1
        
        # 3. 合并到现有规则
        mod_rules['rules'].extend(new_rules)
        
        # 4. 保存规则文件
        try:
            self.mod_rules_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.mod_rules_path, 'w', encoding='utf-8') as f:
                json.dump(mod_rules, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"成功保存 {len(mod_rules['rules'])} 条规则到 {self.mod_rules_path}")
            
            # 输出统计信息
            print("\n" + "="*60)
            print("数据转正完成！")
            print("="*60)
            print(f"新增规则: {updated_count}")
            print(f"跳过(已存在): {skipped_count}")
            print(f"总规则数: {len(mod_rules['rules'])}")
            print("="*60)
            
            return True
            
        except Exception as e:
            self.logger.error(f"保存规则文件失败: {str(e)}")
            return False


def main():
    """主函数"""
    tool = DataMigrationTool()
    
    print("\n此工具将把 mods_data.json 中的数据转入 mod_rules.json")
    print("这将使临时配置变为永久规则。")
    print()
    
    choice = input("是否继续? (y/n): ").strip().lower()
    if choice not in ['y', 'yes', '是']:
        print("已取消")
        return
    
    success = tool.migrate_data(auto_detect_names=True)
    
    if success:
        print("\n✅ 数据转正成功！")
    else:
        print("\n❌ 数据转正失败，请查看日志")
    
    input("\n按Enter键退出...")


if __name__ == "__main__":
    main()
