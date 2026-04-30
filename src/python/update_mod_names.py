#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
规则数据库mod_name填充工具
对mod_rules.json中mod_name为空的条目执行Modrinth API检索并更新
"""

import json
import time
from pathlib import Path
from typing import List, Dict
from logger import setup_logger
from modrinth_api import ModrinthAPI

logger = setup_logger()


class ModNameUpdater:
    """Mod名称更新器"""
    
    def __init__(self, rules_path: str = "config/mod_rules.json"):
        """
        初始化更新器
        
        Args:
            rules_path: 规则文件路径
        """
        self.rules_path = Path(rules_path)
        self.modrinth_api = ModrinthAPI()
        self.logger = logger
    
    def load_rules(self) -> Dict:
        """加载规则文件"""
        if not self.rules_path.exists():
            self.logger.error(f"规则文件不存在: {self.rules_path}")
            return None
        
        try:
            with open(self.rules_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.logger.info(f"成功加载 {len(data.get('rules', []))} 条规则")
            return data
            
        except Exception as e:
            self.logger.error(f"加载规则文件失败: {str(e)}")
            return None
    
    def save_rules(self, data: Dict) -> bool:
        """保存规则文件"""
        try:
            with open(self.rules_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"成功保存 {len(data.get('rules', []))} 条规则")
            return True
            
        except Exception as e:
            self.logger.error(f"保存规则文件失败: {str(e)}")
            return False
    
    def update_mod_names(self, batch_size: int = 10, delay: float = 1.0) -> bool:
        """
        更新mod_name字段
        
        Args:
            batch_size: 每批处理的条目数
            delay: 每次API请求之间的延迟（秒），避免速率限制
            
        Returns:
            是否成功
        """
        print("\n" + "="*60)
        print("开始更新规则数据库中的mod_name字段")
        print("="*60)
        
        # 加载规则
        data = self.load_rules()
        if not data:
            return False
        
        rules = data.get('rules', [])
        
        # 筛选出mod_name为空的条目
        empty_name_rules = [rule for rule in rules if not rule.get('mod_name', '')]
        
        if not empty_name_rules:
            print("\n✅ 所有规则的mod_name字段都已填充，无需更新")
            return True
        
        print(f"\n找到 {len(empty_name_rules)} 条需要更新的规则")
        print(f"将分 {((len(empty_name_rules) - 1) // batch_size) + 1} 批处理\n")
        
        updated_count = 0
        failed_count = 0
        skipped_count = 0
        
        # 分批处理
        for i in range(0, len(empty_name_rules), batch_size):
            batch = empty_name_rules[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = ((len(empty_name_rules) - 1) // batch_size) + 1
            
            print(f"\n--- 处理第 {batch_num}/{total_batches} 批 ({len(batch)} 条) ---")
            
            for j, rule in enumerate(batch, 1):
                mod_id = rule.get('mod_id', '')
                current_index = i + j
                total = len(empty_name_rules)
                
                print(f"[{current_index}/{total}] 处理: {mod_id}", end=" ... ")
                
                # 使用Modrinth API检索
                try:
                    project = self.modrinth_api.search_project(mod_id)
                    
                    if project:
                        mod_name = project.get('title', '')
                        if mod_name:
                            rule['mod_name'] = mod_name
                            print(f"✅ {mod_name}")
                            updated_count += 1
                        else:
                            print("⚠️ 未找到名称")
                            skipped_count += 1
                    else:
                        print("❌ API未返回结果")
                        failed_count += 1
                    
                except Exception as e:
                    print(f"❌ 错误: {str(e)}")
                    failed_count += 1
                
                # 延迟以避免速率限制
                if j < len(batch):  # 最后一项不需要延迟
                    time.sleep(delay)
            
            # 批次间额外延迟
            if i + batch_size < len(empty_name_rules):
                print(f"\n等待 {delay * 2} 秒后继续下一批...")
                time.sleep(delay * 2)
        
        # 保存更新后的规则
        print("\n" + "="*60)
        print("保存更新后的规则...")
        
        if self.save_rules(data):
            print("\n" + "="*60)
            print("更新完成！")
            print("="*60)
            print(f"成功更新: {updated_count}")
            print(f"失败: {failed_count}")
            print(f"跳过: {skipped_count}")
            print("="*60)
            return True
        else:
            print("\n❌ 保存失败")
            return False


def main():
    """主函数"""
    updater = ModNameUpdater()
    
    print("\n此工具将对 mod_rules.json 中 mod_name 为空的条目")
    print("执行 Modrinth API 检索并填充 mod_name 字段。")
    print("注意：这可能需要较长时间，取决于条目数量和网络状况。\n")
    
    choice = input("是否继续? (y/n): ").strip().lower()
    if choice not in ['y', 'yes', '是']:
        print("已取消")
        return
    
    success = updater.update_mod_names(batch_size=10, delay=1.0)
    
    if success:
        print("\n✅ mod_name更新成功！")
    else:
        print("\n❌ mod_name更新失败，请查看日志")
    
    input("\n按Enter键退出...")


if __name__ == "__main__":
    main()
