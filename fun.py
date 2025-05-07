import os
import subprocess
import random
import datetime

# 5x7点阵字母库（优化版）
LETTER_PATTERNS = {
    'B': [
        [1,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,1,1,1,0],
    ],
    'E': [
        [1,1,1,1,1],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,1,1,1,1],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,1,1,1,1],
    ],
    'R': [
        [1,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
    ],
    'N': [
        [1,0,0,0,1],
        [1,1,0,0,1],
        [1,0,0,0,1],
        [1,0,1,0,1],
        [1,0,0,0,1],
        [1,0,0,1,1],
        [1,0,0,0,1],
    ],
    'I': [
        [1,1,1,1,1],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [1,1,1,1,1],
    ],
    'E': [  # 重复E
        [1,1,1,1,1],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,1,1,1,1],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,1,1,1,1],
    ],
}

def combine_letters(word):
    """拼接字母点阵，每个字母间隔1列空白"""
    rows = 7
    combined = []
    for r in range(rows):
        row = []
        for ch in word.upper():
            pattern = LETTER_PATTERNS.get(ch, [[0]*5]*7)  # 未定义字母用空白代替
            row.extend(pattern[r])
            row.append(1)  # 字母间空白列
        combined.append(row[:-1])  # 移除最后一个空白列
    return combined

def generate_commit_dates(start_date, pattern):
    """生成提交日期映射表"""
    schedule = {}
    cols = len(pattern[0])  # 获取列数
    for col in range(cols):
        for row in range(7):
            current_date = start_date + datetime.timedelta(weeks=col, days=row)
            try:
                # if pattern[row][col] == 1:
                #     schedule[current_date] = random.randint(1, 5)
                if pattern[row][col] == 1:
                    schedule[current_date] = 10
                if pattern[row][col] == 0:
                    schedule[current_date] = 2
            except IndexError:
                continue  # 忽略越界点
    return schedule

def make_commits(schedule):
    """执行提交操作"""
    if not os.path.exists('.git'):
        subprocess.run(['git', 'init'], check=True, stdout=subprocess.DEVNULL)
    
    file_path = "green_art.txt"
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:  # 首次创建文件
            f.write("GitHub Green Art Generator\n")
    
    for date, count in schedule.items():
        for i in range(count):
            # 生成带时区的时间戳
            timestamp = f"{date.strftime('%Y-%m-%d')} 12:{i:02}:00 +0800"
            env = os.environ.copy()
            env.update({
                'GIT_AUTHOR_DATE': timestamp,
                'GIT_COMMITTER_DATE': timestamp
            })
            
            # 追加内容
            with open(file_path, 'a') as f:
                f.write(f"Commit at {timestamp}\n")
            
            # 执行Git操作
            subprocess.run(['git', 'add', file_path], env=env, check=True, stdout=subprocess.DEVNULL)
            subprocess.run(
                ['git', 'commit', '-m', f'Art commit at {timestamp}'],
                env=env,
                check=True,
                stdout=subprocess.DEVNULL
            )

if __name__ == "__main__":
    # 配置参数
    start_date = datetime.date(2022, 1, 2)  # 必须是周日
    while start_date.weekday() != 6:
        start_date -= datetime.timedelta(days=1)
    
    # 生成图案
    pattern = combine_letters("BERNIE")  # 注意E重复使用
    schedule = generate_commit_dates(start_date, pattern)
    
    # 执行提交
    make_commits(schedule)
    print("提交完成！执行以下命令推送到GitHub：")
    print("git remote add origin <你的仓库地址>")
    print("git push -u origin main")
