#!/usr/bin/env python3
"""
PDF Organizer Script
重命名PDF文件为 会议-年份-标题.pdf 格式

使用前请安装依赖：
pip3 install PyPDF2

或者：
pip3 install -r requirements.txt
"""

import os
import re
import argparse
from pathlib import Path
from typing import Dict, Optional, Tuple

try:
    import PyPDF2
except ImportError:
    print("错误: 未找到 PyPDF2 模块")
    print("请运行: pip3 install PyPDF2")
    print("或者: pip3 install -r requirements.txt")
    exit(1)

class PDFOrganizer:
    def __init__(self, base_path: str, dry_run: bool = True):
        self.base_path = Path(base_path)
        self.dry_run = dry_run
        
        # 常见会议和期刊缩写映射
        self.conference_patterns = {
            # 顶级会议
            'DAC': ['Design Automation Conference', 'DAC'],
            'DATE': ['Design, Automation and Test in Europe', 'DATE'],
            'ICCAD': ['International Conference on Computer-Aided Design', 'ICCAD'],
            'ISCA': ['International Symposium on Computer Architecture', 'ISCA'],
            'MICRO': ['International Symposium on Microarchitecture', 'MICRO'],
            'HPCA': ['International Symposium on High-Performance Computer Architecture', 'HPCA'],
            'ASPLOS': ['Architectural Support for Programming Languages and Operating Systems', 'ASPLOS'],
            'USENIX': ['USENIX', 'ATC'],
            
            # 安全和密码学会议
            'CCS': ['Computer and Communications Security', 'CCS'],
            'CRYPTO': ['International Cryptology Conference', 'CRYPTO'],
            'EUROCRYPT': ['European Cryptology Conference', 'EUROCRYPT'],
            'ASIACRYPT': ['International Conference on the Theory and Application of Cryptology', 'ASIACRYPT'],
            'CHES': ['Cryptographic Hardware and Embedded Systems', 'CHES'],
            'PKC': ['Public Key Cryptography', 'PKC'],
            'TCC': ['Theory of Cryptography Conference', 'TCC'],
            
            # 期刊
            'TOCS': ['ACM Transactions on Computer Systems', 'TOCS'],
            'TPDS': ['IEEE Transactions on Parallel and Distributed Systems', 'TPDS'],
            'TCAD': ['IEEE Transactions on Computer-Aided Design', 'TCAD'],
            'TC': ['IEEE Transactions on Computers', 'TC'],
            'TVLSI': ['IEEE Transactions on Very Large Scale Integration Systems', 'TVLSI'],
        }
        
        # 年份提取模式
        self.year_patterns = [
            r'20\d{2}',  # 2000-2099
            r'19\d{2}',  # 1900-1999
        ]
    
    def extract_pdf_metadata(self, pdf_path: Path) -> Dict[str, str]:
        """从PDF文件中提取元数据"""
        metadata = {
            'title': '',
            'author': '',
            'subject': '',
            'creator': '',
            'producer': '',
            'creation_date': '',
            'modification_date': ''
        }
        
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                if reader.metadata:
                    for key in metadata.keys():
                        value = getattr(reader.metadata, f'/{key}', '') or getattr(reader.metadata, f'/{key.capitalize()}', '')
                        if value:
                            metadata[key] = str(value).strip()
                
                # 尝试从第一页提取文本作为标题补充
                if not metadata['title'] and len(reader.pages) > 0:
                    first_page_text = reader.pages[0].extract_text()
                    if first_page_text:
                        # 提取第一行作为可能的标题
                        lines = [line.strip() for line in first_page_text.split('\n') if line.strip()]
                        if lines:
                            metadata['title'] = lines[0][:100]  # 限制长度
        
        except Exception as e:
            print(f"无法读取PDF元数据: {pdf_path.name} - {e}")
        
        return metadata
    
    def extract_year_from_text(self, text: str) -> Optional[str]:
        """从文本中提取年份"""
        for pattern in self.year_patterns:
            matches = re.findall(pattern, text)
            if matches:
                # 返回最合理的年份（通常是最新的）
                years = [int(year) for year in matches if 1990 <= int(year) <= 2025]
                if years:
                    return str(max(years))
        return None
    
    def detect_conference(self, filename: str, title: str, text_content: str = '') -> Optional[str]:
        """检测会议名称"""
        search_text = f"{filename} {title} {text_content}".lower()
        
        for conf_abbr, conf_names in self.conference_patterns.items():
            for conf_name in conf_names:
                if conf_name.lower() in search_text:
                    return conf_abbr
        
        # 从文件名中检测数字模式（可能是会议论文编号）
        if re.search(r'\d{4}-\d{3,4}', filename):
            return 'IACR'  # IACR eprint 格式
        
        # 根据目录名检测
        if 'dac' in filename.lower():
            return 'DAC'
        elif 'date' in filename.lower():
            return 'DATE'
        
        return 'Unknown'
    
    def clean_filename(self, text: str) -> str:
        """清理文件名，移除非法字符"""
        # 移除或替换非法字符
        text = re.sub(r'[<>:"/\\|?*]', '', text)
        text = re.sub(r'\s+', ' ', text)  # 合并多个空格
        text = text.strip()
        
        # 限制长度
        if len(text) > 100:
            text = text[:100].rsplit(' ', 1)[0]  # 在单词边界截断
        
        return text
    
    def generate_new_filename(self, pdf_path: Path) -> str:
        """生成新的文件名"""
        metadata = self.extract_pdf_metadata(pdf_path)
        
        # 提取标题
        title = metadata.get('title', '')
        if not title:
            title = pdf_path.stem
        
        # 提取年份
        year = None
        
        # 从元数据日期提取年份
        creation_date = metadata.get('creation_date', '')
        if creation_date:
            year = self.extract_year_from_text(creation_date)
        
        # 从文件名提取年份
        if not year:
            year = self.extract_year_from_text(pdf_path.name)
        
        # 从标题提取年份
        if not year:
            year = self.extract_year_from_text(title)
        
        # 默认年份
        if not year:
            year = 'Unknown'
        
        # 检测会议
        conference = self.detect_conference(pdf_path.name, title)
        
        # 清理标题
        clean_title = self.clean_filename(title)
        if not clean_title:
            clean_title = self.clean_filename(pdf_path.stem)
        
        # 生成新文件名
        new_filename = f"{conference}-{year}-{clean_title}.pdf"
        
        return new_filename
    
    def rename_pdf(self, pdf_path: Path) -> bool:
        """重命名单个PDF文件"""
        try:
            new_filename = self.generate_new_filename(pdf_path)
            new_path = pdf_path.parent / new_filename
            
            # 避免文件名冲突
            counter = 1
            while new_path.exists() and new_path != pdf_path:
                name_without_ext = new_filename[:-4]
                new_filename = f"{name_without_ext}_{counter}.pdf"
                new_path = pdf_path.parent / new_filename
                counter += 1
            
            if self.dry_run:
                print(f"[DRY RUN] {pdf_path.name} -> {new_filename}")
            else:
                if new_path != pdf_path:
                    pdf_path.rename(new_path)
                    print(f"重命名: {pdf_path.name} -> {new_filename}")
                else:
                    print(f"跳过: {pdf_path.name} (名称未改变)")
            
            return True
            
        except Exception as e:
            print(f"重命名失败: {pdf_path.name} - {e}")
            return False
    
    def organize_pdfs(self):
        """组织所有PDF文件"""
        pdf_files = list(self.base_path.rglob("*.pdf"))
        
        print(f"找到 {len(pdf_files)} 个PDF文件")
        
        if self.dry_run:
            print("=== DRY RUN 模式 - 不会实际重命名文件 ===")
        
        success_count = 0
        for pdf_file in pdf_files:
            if self.rename_pdf(pdf_file):
                success_count += 1
        
        print(f"\n完成! 成功处理 {success_count}/{len(pdf_files)} 个文件")

def main():
    parser = argparse.ArgumentParser(description='重命名PDF文件为 会议-年份-标题.pdf 格式')
    parser.add_argument('path', help='包含PDF文件的目录路径')
    parser.add_argument('--no-dry-run', action='store_true', help='实际执行重命名（默认为dry-run模式）')
    parser.add_argument('--recursive', '-r', action='store_true', default=True, help='递归处理子目录')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        print(f"错误: 路径不存在 - {args.path}")
        return
    
    dry_run = not args.no_dry_run
    organizer = PDFOrganizer(args.path, dry_run=dry_run)
    organizer.organize_pdfs()

if __name__ == "__main__":
    main()