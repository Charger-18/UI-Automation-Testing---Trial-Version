# -*- coding: utf-8 -*-
import os
import glob
import sys
import re
import json
from datetime import datetime

# ------------------------------------------------------------------
# 1. 需要扫描的根目录（写死）
# ------------------------------------------------------------------
ROOT_DOCS = r"C:\Users\74515\Desktop\UI自动化测试_体验版\docs"

# ------------------------------------------------------------------
# 2. 主流程：找到所有 */log.html  → 检查 → 汇总
# ------------------------------------------------------------------
def main():
    if not os.path.isdir(ROOT_DOCS):
        print("[错误] 目录不存在：", ROOT_DOCS)
        sys.exit(1)

    # 2.1 扫描所有 */log.html
    pattern = os.path.join(ROOT_DOCS, "*", "log.html")
    html_files = glob.glob(pattern)
    if not html_files:
        print("未找到任何 */log.html 报告文件")
        sys.exit(1)

    print(f"共找到 {len(html_files)} 份 log.html 报告")

    # 2.2 逐份检查
    results = []
    for log_path in html_files:
        print("正在检查:", log_path)
        results.append(check_single_html_report(log_path))

    # 2.3 生成汇总
    summary = generate_summary_report(results)
    print_results(results, summary)

    # 2.4 退出码
    sys.exit(0 if summary['failed_reports'] == 0 else 1)

# ------------------------------------------------------------------
# 3. 复用你原来的函数（仅删掉与命令行相关的代码）
# ------------------------------------------------------------------
def check_single_html_report(html_report_path):
    try:
        with open(html_report_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        match = re.search(r'data = ({.*?});', html_content, re.DOTALL)
        if not match:
            return {
                'success': False,
                'file_path': html_report_path,
                'test_name': os.path.basename(os.path.dirname(html_report_path)),  # 用上级文件夹名当模块名
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
                'test_name': os.path.basename(os.path.dirname(html_report_path)),
                'reason': '解析 data 对象失败: ' + str(e),
                'element_found': False
            }

        test_result = data.get("test_result", False)
        return {
            'success': test_result,
            'file_path': html_report_path,
            'test_name': os.path.basename(os.path.dirname(html_report_path)),
            'reason': 'test_result 为 true' if test_result else 'test_result 为 false',
            'element_found': True
        }
    except Exception as e:
        return {
            'success': False,
            'file_path': html_report_path,
            'test_name': os.path.basename(os.path.dirname(html_report_path)),
            'reason': f'解析文件时出错: {str(e)}',
            'element_found': False
        }

def generate_summary_report(results, output_file=None):
    total_reports = len(results)
    passed_reports = sum(1 for r in results if r['success'])
    failed_reports = total_reports - passed_reports
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

if __name__ == "__main__":
    main()