import os
import re
from collections import defaultdict

def find_md_files(src_dir):
    md_files = []
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    return md_files

def extract_section_and_headers(file_path):
    section_match = re.search(r'Section(\d+)', file_path)
    if not section_match:
        return None, [], None

    section_num = section_match.group(1)
    headers = []
    file_name = os.path.basename(file_path)  # 파일명 추출

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        headers = re.findall(r'^#\s+(.+)$', content, re.MULTILINE)

    return section_num, headers, file_name

def generate_toc():
    sections = defaultdict(list)
    md_files = find_md_files('src')

    for file in md_files:
        section_num, headers, file_name = extract_section_and_headers(file)
        if section_num:
            for header in headers:
                sections[int(section_num)].append((header, file_name))

    toc = ["# JAVA 학습 기록 📚\n\n"]
    toc.append("자바 기초부터 심화까지의 학습 내용을 정리합니다.\n")
    toc.append("김영한 선생님의 강의를 듣고 코드를 작성하고 내용을 요약합니다.\n\n")

    for section_num in sorted(sections.keys()):
        toc.append(f"## Section {section_num}\n")
        for i, (header, file_name) in enumerate(sorted(set(sections[section_num])), 1):
            link_path = f"src/Section{section_num}/{file_name}"
            toc.append(f"{i}. [{header}]({link_path})\n")
        toc.append("\n")

    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()

        toc_content = ''.join(toc)
        if '# JAVA 학습 기록 📚' in content:
            content = re.sub(
                r'# JAVA 학습 기록 📚.*?(?=##\s+[^#]|\Z)',
                toc_content,
                content,
                flags=re.DOTALL
            )
        else:
            content = toc_content + "\n" + content
    except FileNotFoundError:
        content = ''.join(toc)

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    generate_toc()