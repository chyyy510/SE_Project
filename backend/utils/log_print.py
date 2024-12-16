import sys
import datetime
from decouple import config


def log_print(text_to_print):
    # 保存当前的标准输出
    original_stdout = sys.stdout

    file_path = config("LOGFILE_PATH")

    try:
        # 打开文件并将 sys.stdout 重定向到文件
        with open(file_path, "a") as f:
            sys.stdout = f
            print(datetime.datetime.now())
            print(text_to_print)  # 这部分输出会写入文件
    finally:
        # 恢复标准输出流，确保后续 print 语句仍输出到控制台
        sys.stdout = original_stdout
