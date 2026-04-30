#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
强制重新分类Input目录中的Mod并更新规则数据库

功能：
1. 重新解析所有JAR文件（优先级A - JAR配置）
2. 如果JAR中没有environment/side字段，使用Modrinth API（优先级C）
3. 更新mod_rules.json规则数据库
4. 将新的分类结果同步到mods_data.json
"""

import sys
import json
from pathlib import Path
from jar_parser import JarParser
from rule_manager import RuleManager
from config_manager import ConfigManager
from logger import setup_logger
from file_utils import get_jar_files

logger = setup_logger()


class ForceReclassifier:
    """强制重新分类器"""
    
    def __init__(self, input_dir: str = "Input", 
                 rules_path: str = "config/mod_rules.json",
                 config_path: str = "config/mods_data.json"):
        self.input_dir = Path(input_dir)
        self.jar_parser = JarParser(skip_rules=True)  # 强制重新分类时跳过规则数据库
        self.rule_manager = RuleManager(rules_path)
        self.config_manager = ConfigManager(config_path)
        
        # 统计信息
        self.stats = {
            'total': 0,
            'updated': 0,
            'unchanged': 0,
            'failed': 0,
            'new_rules': 0
        }
    
    def run(self):
        """执行强制重新分类"""
        logger.info("=" * 60)
        logger.info("开始强制重新分类Input目录中的Mod")
        logger.info("=" * 60)
        
        # 加载现有规则
        if not self.rule_manager.load_rules():
            logger.warning("规则文件不存在，将创建新规则")
        
        # 加载现有配置
        if not self.config_manager.load_config():
            logger.warning("配置文件不存在，将创建新配置")
        
        # 获取所有JAR文件
        jar_files = get_jar_files(self.input_dir)
        
        if not jar_files:
            logger.error(f"输入目录 {self.input_dir} 中没有找到JAR文件")
            return False
        
        self.stats['total'] = len(jar_files)
        logger.info(f"找到 {self.stats['total']} 个JAR文件\n")
        
        # 处理每个JAR文件
        for jar_path in jar_files:
            self._process_jar(jar_path)
        
        # 保存更新后的规则
        if self.stats['updated'] > 0 or self.stats['new_rules'] > 0:
            logger.info(f"\n保存规则数据库...")
            self.rule_manager.save_rules()
            logger.info(f"✓ 规则数据库已更新")
        
        # 保存配置
        if self.config_manager.mods_data:
            logger.info(f"保存配置文件...")
            self.config_manager.save_config()
            logger.info(f"✓ 配置文件已更新")
        
        # 输出统计信息
        self._print_statistics()
        
        return True
    
    def _process_jar(self, jar_path: Path):
        """处理单个JAR文件"""
        filename = jar_path.name
        logger.info(f"处理: {filename}")
        
        # 解析JAR文件（完全忽略现有规则，强制重新解析）
        mod_info = self.jar_parser.parse_jar(jar_path)
        
        if not mod_info:
            logger.warning(f"  ✗ 无法解析 {filename}")
            self.stats['failed'] += 1
            return
        
        mod_id = mod_info.get('mod_id', '')
        mod_name = mod_info.get('mod_name', '')
        mod_type = mod_info.get('type', 'unknown')
        
        if not mod_id:
            logger.warning(f"  ✗ {filename} 中未找到modId")
            self.stats['failed'] += 1
            return
        
        logger.debug(f"  Mod ID: {mod_id}, Mod Name: {mod_name}, 类型: {mod_type}")
        
        # 检查规则数据库中是否已存在
        existing_rule = self.rule_manager.find_rule(mod_id)
        
        if existing_rule:
            old_type = existing_rule.get('type', '')
            
            # 强制更新：无论旧规则是什么，都用新的JAR解析结果覆盖
            if old_type != mod_type:
                # 类型发生变化
                existing_rule['type'] = mod_type
                existing_rule['reason'] = f"通过JAR配置强制更新: {mod_name}"
                existing_rule['mod_name'] = mod_name
                
                logger.info(f"  ✓ 强制更新: {old_type} → {mod_type}")
                self.stats['updated'] += 1
            else:
                # 类型未变化，但强制更新reason和mod_name
                existing_rule['reason'] = f"通过JAR配置验证: {mod_name}"
                existing_rule['mod_name'] = mod_name
                
                logger.info(f"  ⊙ 验证通过: {mod_type}")
                self.stats['unchanged'] += 1
        else:
            # 新规则
            new_rule = {
                'mod_id': mod_id,
                'mod_name': mod_name,
                'type': mod_type,
                'reason': f"通过JAR配置新增: {mod_name}"
            }
            self.rule_manager.rules.append(new_rule)
            
            logger.info(f"  + 新增规则: {mod_type}")
            self.stats['new_rules'] += 1
        
        # 同步到mods_data.json
        existing_config = self.config_manager.find_mod(mod_id)
        if existing_config:
            if existing_config['type'] != mod_type:
                existing_config['type'] = mod_type
                logger.debug(f"  同步更新配置: {mod_type}")
        else:
            self.config_manager.add_mod(mod_id, mod_type, mod_name)
            logger.debug(f"  同步新增配置: {mod_type}")
    
    def _print_statistics(self):
        """打印统计信息"""
        logger.info("\n" + "=" * 60)
        logger.info("强制重新分类完成")
        logger.info("=" * 60)
        logger.info(f"总文件数: {self.stats['total']}")
        logger.info(f"更新规则: {self.stats['updated']}")
        logger.info(f"新增规则: {self.stats['new_rules']}")
        logger.info(f"未变化: {self.stats['unchanged']}")
        logger.info(f"失败: {self.stats['failed']}")
        logger.info("=" * 60)


def main():
    """主函数"""
    try:
        reclassifier = ForceReclassifier()
        success = reclassifier.run()
        
        if success:
            print("\n[OK] 强制重新分类完成")
        else:
            print("\n[ERROR] 强制重新分类失败")
            return 1
        
        input("\n按Enter键退出...")
        return 0
        
    except Exception as e:
        logger.error(f"错误: {str(e)}", exc_info=True)
        print(f"\n[ERROR] 错误: {str(e)}")
        input("\n按Enter键退出...")
        return 1


if __name__ == "__main__":
    sys.exit(main())
