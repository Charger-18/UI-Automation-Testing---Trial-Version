# -*- coding: utf-8 -*-
import os
import glob
import sys
import re
import json
from datetime import datetime
from bs4 import BeautifulSoup

def check_single_html_report(html_report_path):
    """
    检查单个HTML格式的Airtest报告
    从 JavaScript 中提取 data 对象，判断 test_result
    """
    try:
        with open(html_report_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 正则提取 data 对象
        match = re.search(r'data = ({.*?});', html_content, re.DOTALL)
        if not match:
            return {
                'success': False,
                'file_path': html_report_path,
                'test_name': os.path.basename(html_report_path),
                'reason': '未找到页面中的 data 对象',
                'element_found': False
            }

        data_str = match.group(1)
        try:
            data = json.loads(data_str)
        except json.JSONDecodeError as e:
            return {
                'success': False,
                'file_path': html_report_path,
                'test_name': os.path.basename(html_report_path),
                'reason': '解析 data 对象失败: ' + str(e),
                'element_found': False
            }

        test_result = data.get("test_result", False)

        return {
            'success': test_result,
            'file_path': html_report_path,
            'test_name': os.path.basename(html_report_path),
            'reason': 'test_result 为 true' if test_result else 'test_result 为 false',
            'element_found': True
        }

    except Exception as e:
        return {
            'success': False,
            'file_path': html_report_path,
            'test_name': os.path.basename(html_report_path),
            'reason': f'解析文件时出错: {str(e)}',
            'element_found': False
        }

def check_all_html_reports(reports_directory):
    """
    检查指定目录下的所有HTML报告
    """
    # 支持多种可能的HTML文件位置
    search_patterns = [
        os.path.join(reports_directory, "**", "*.html"),
        os.path.join(reports_directory, "*.html"),
        os.path.join(reports_directory, "**", "*.htm"),
        os.path.join(reports_directory, "*.htm")
    ]
    
    html_files = []
    for pattern in search_patterns:
        files = glob.glob(pattern, recursive=True)
        html_files.extend(files)
    
    # 去重
    html_files = list(set(html_files))
    
    if not html_files:
        print(f"在目录 {reports_directory} 中未找到HTML报告文件")
        return []
    
    return html_files

def check_reports_and_get_results(html_files):
    """
    检查所有HTML文件并返回结果
    """
    results = []
    for html_file in html_files:
        print(f"正在检查: {os.path.basename(html_file)}")
        result = check_single_html_report(html_file)
        results.append(result)
    
    return results

def generate_summary_report(results, output_file=None):
    """
    生成汇总报告
    """
    total_reports = len(results)
    passed_reports = sum(1 for r in results if r['success'])
    failed_reports = total_reports - passed_reports
    
    # 统计通过元素检查的报告数量
    element_checked_passed = sum(1 for r in results if r['success'] and r.get('element_found', False))
    
    summary = {
        'total_reports': total_reports,
        'passed_reports': passed_reports,
        'failed_reports': failed_reports,
        'pass_rate': round(passed_reports / total_reports * 100, 2) if total_reports > 0 else 0,
        'element_checked_count': element_checked_passed,
        'check_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'details': results
    }
    
    # 输出到文件
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("AIRTEST HTML报告检查汇总\n")
            f.write("=" * 60 + "\n")
            f.write(f"检查时间: {summary['check_time']}\n")
            f.write(f"总报告数: {summary['total_reports']}\n")
            f.write(f"通过报告: {summary['passed_reports']}\n")
            f.write(f"失败报告: {summary['failed_reports']}\n")
            f.write(f"通过率: {summary['pass_rate']}%\n")
            f.write(f"元素确认的报告: {element_checked_passed}\n\n")
            
            f.write("详细结果:\n")
            for i, result in enumerate(results, 1):
                status = " 通过" if result['success'] else " 失败"
                element_status = " (元素确认)" if result.get('element_found', False) else " (未找到元素)"
                f.write(f"{i}. {result['test_name']}: {status}{element_status}\n")
                f.write(f"   原因: {result['reason']}\n")
                f.write(f"   文件: {os.path.basename(result['file_path'])}\n")
                f.write("-" * 50 + "\n")
    
    return summary

def print_results(results, summary):
    """
    打印检查结果
    """
    print("=" * 80)
    print(" AIRTEST HTML报告自动检查结果")
    print("=" * 80)
    
    for i, result in enumerate(results, 1):
        status = " 通过" if result['success'] else " 失败"
        element_indicator = " " if result.get('element_found', False) else ""
        print(f"{i}. {result['test_name']}")
        print(f"   状态: {status}{element_indicator}")
        print(f"   原因: {result['reason']}")
        print(f"   文件: {os.path.basename(result['file_path'])}")
        print("-" * 60)
    
    print("\n 汇总统计:")
    print(f"   总报告数: {summary['total_reports']}")
    print(f"   通过报告: {summary['passed_reports']}")
    print(f"   失败报告: {summary['failed_reports']}")
    print(f"   通过率: {summary['pass_rate']}%")
    print(f"   元素确认的报告: {summary['element_checked_count']}")
    print(f"   检查时间: {summary['check_time']}")
    print("=" * 80)

def main():
    if len(sys.argv) < 2:
        print("使用方法: python check_reports.py <报告目录> [输出文件]")
        print("示例: python check_reports.py C:/Users/74515/Desktop/UI自动化测试_体验版/report")
        print("示例: python check_reports.py C:/Users/74515/Desktop/UI自动化测试_体验版/report summary.txt")
        sys.exit(1)
    
    reports_dir = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(reports_dir):
        print(f"错误: 目录不存在 {reports_dir}")
        sys.exit(1)
    
    print(f"开始检查HTML报告目录: {reports_dir}")
    
    # 查找所有HTML文件
    html_files = check_all_html_reports(reports_dir)
    
    if not html_files:
        print("未找到任何HTML报告文件")
        sys.exit(1)
    
    print(f"找到 {len(html_files)} 个HTML文件")
    
    # 检查所有报告
    results = check_reports_and_get_results(html_files)
    
    # 调试信息：检查结果结构
    print(f"检查完成，共 {len(results)} 个结果")
    for i, result in enumerate(results):
        print(f"结果 {i+1}: {result}")
    
    summary = generate_summary_report(results, output_file)
    
    # 打印结果
    print_results(results, summary)
    
    # 输出文件信息
    if output_file:
        print(f"\n 汇总报告已保存: {output_file}")
    
    # 返回退出码
    if summary['failed_reports'] > 0:
        print("\n 存在失败的测试报告")
        sys.exit(1)
    else:
        print("\n 所有测试报告均通过")
        sys.exit(0)

if __name__ == "__main__":
    main()