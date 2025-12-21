#!/usr/bin/env python3
"""
清理脚本 - 清空results文件夹
Clean Script - Clear results folder

运行此脚本来清空results文件夹中的所有文件
"""

import os
import shutil

RESULTS_DIR = "results"

def clean_results():
    """清空results文件夹"""
    if not os.path.exists(RESULTS_DIR):
        print(f"✓ {RESULTS_DIR}/ 文件夹不存在，无需清理")
        return
    
    # 统计文件数量
    midi_count = len([f for f in os.listdir(RESULTS_DIR) if f.endswith('.mid')])
    
    if midi_count == 0:
        print(f"✓ {RESULTS_DIR}/ 文件夹已经是空的")
        return
    
    # 询问确认
    print(f"⚠️  将删除 {RESULTS_DIR}/ 文件夹中的 {midi_count} 个MIDI文件")
    response = input("确认删除? (y/N): ").strip().lower()
    
    if response in ['y', 'yes']:
        # 删除文件夹
        shutil.rmtree(RESULTS_DIR)
        # 重新创建空文件夹
        os.makedirs(RESULTS_DIR)
        print(f"✓ 已清空 {RESULTS_DIR}/ 文件夹")
    else:
        print("✗ 取消删除")

if __name__ == "__main__":
    clean_results()

