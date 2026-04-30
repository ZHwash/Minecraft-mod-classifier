#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用Modrinth API重新分类规则数据库中的Mod
直接调用优先级C（API检索）更新type字段
"""

import json
import time
from pathlib import Path
from typing import Dict
from logger import setup_logger
from modrinth_api import ModrinthAPI

logger = setup_logger()


class TypeUpdater:
    """类型更新器 - 直接使用Modrinth API"""
    
    def __init__(self, rules_path: str = "config/mod_rules.json"):
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
    
    def update_types(self, batch_size: int = 10, delay: float = 1.0) -> bool:
        """
        使用Modrinth API更新type字段
        
        Args:
            batch_size: 每批处理的条目数
            delay: 每次API请求之间的延迟（秒）
            
        Returns:
            是否成功
        """
        print("\n" + "="*60)
        print("使用Modrinth API重新分类规则数据库")
        print("="*60)
        
        # 加载规则
        data = self.load_rules()
        if not data:
            return False
        
        rules = data.get('rules', [])
        
        # 筛选出mod_name不为空的条目（已有名称才能进行API检索）
        named_rules = [rule for rule in rules if rule.get('mod_name', '')]
        
        if not named_rules:
            print("\n⚠️ 没有mod_name字段的规则，无法进行API检索")
            return False
        
        print(f"\n找到 {len(named_rules)} 条有mod_name的规则")
        print(f"将分 {((len(named_rules) - 1) // batch_size) + 1} 批处理\n")
        
        updated_count = 0
        unchanged_count = 0
        failed_count = 0
        
        # 分批处理
        for i in range(0, len(named_rules), batch_size):
            batch = named_rules[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = ((len(named_rules) - 1) // batch_size) + 1
            
            print(f"\n--- 处理第 {batch_num}/{total_batches} 批 ({len(batch)} 条) ---")
            
            for j, rule in enumerate(batch, 1):
                mod_id = rule.get('mod_id', '')
                mod_name = rule.get('mod_name', '')
                old_type = rule.get('type', 'unknown')
                current_index = i + j
                total = len(named_rules)
                
                print(f"[{current_index}/{total}] {mod_id}", end=" ... ")
                
                try:
                    # 直接使用Modrinth API分类（优先级C）
                    new_type = self.modrinth_api.classify_mod_via_api(mod_name, mod_id)
                    
                    if new_type:
                        if new_type != old_type:
                            rule['type'] = new_type
                            rule['reason'] = f"通过Modrinth API重新分类: {mod_name}"
                            print(f"✅ {old_type} → {new_type}")
                            updated_count += 1
                        else:
                            print(f"⏭️ 保持不变 ({old_type})")
                            unchanged_count += 1
                    else:
                        print(f"⚠️ API无法判断，保持原类型 ({old_type})")
                        failed_count += 1
                    
                except Exception as e:
                    print(f"❌ 错误: {str(e)}")
                    failed_count += 1
                
                # 延迟以避免速率限制
                if j < len(batch):
                    time.sleep(delay)
            
            # 批次间额外延迟
            if i + batch_size < len(named_rules):
                print(f"\n等待 {delay * 2} 秒后继续下一批...")
                time.sleep(delay * 2)
        
        # 保存更新后的规则
        print("\n" + "="*60)
        print("保存更新后的规则...")
        
        if self.save_rules(data):
            print("\n" + "="*60)
            print("更新完成！")
            print("="*60)
            print(f"类型变更: {updated_count}")
            print(f"保持不变: {unchanged_count}")
            print(f"无法判断: {failed_count}")
            print("="*60)
            return True
        else:
            print("\n❌ 保存失败")
            return False


def main():
    """主函数"""
    updater = TypeUpdater()
    
    print("\n此工具将使用 Modrinth API 重新分类 mod_rules.json 中的Mod")
    print("注意：")
    print("  1. 仅处理已有 mod_name 的条目")
    print("  2. 直接调用API检索，不使用规则数据库或JAR配置")
    print("  3. 这可能需要较长时间，取决于条目数量和网络状况\n")
    
    choice = input("是否继续? (y/n): ").strip().lower()
    if choice not in ['y', 'yes', '是']:
        print("已取消")
        return
    
    success = updater.update_types(batch_size=10, delay=1.0)
    
    if success:
        print("\n✅ 类型更新成功！")
    else:
        print("\n❌ 类型更新失败，请查看日志")
    
    try:
        input("\n按Enter键退出...")
    except EOFError:
        pass  # 管道输入时跳过


if __name__ == "__main__":
    main()
