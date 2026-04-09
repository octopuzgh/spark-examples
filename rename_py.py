import os
import re


def camel_to_snake(name):
    """驼峰转下划线"""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def rename_py_files(directory):
    """批量重命名目录下的所有 .py 文件"""
    renamed_files = []

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.py'):
                old_path = os.path.join(root, filename)

                # 去掉 .py 后缀，转换命名，再加回来
                name_without_ext = filename[:-3]  # 去掉 .py
                new_name = camel_to_snake(name_without_ext) + '.py'
                new_path = os.path.join(root, new_name)

                if old_path != new_path:
                    try:
                        os.rename(old_path, new_path)
                        renamed_files.append((filename, new_name))
                        print(f"✅ {filename} -> {new_name}")
                    except Exception as e:
                        print(f"❌ {filename} 重命名失败: {e}")

    return renamed_files


if __name__ == '__main__':
    target_dir = "/mnt/hgfs/share_files/pyspark_learn"

    print("=" * 60)
    print("开始批量重命名 .py 文件（驼峰 -> 下划线）")
    print("=" * 60)

    renamed = rename_py_files(target_dir)

    print("\n" + "=" * 60)
    print(f"重命名完成！共修改 {len(renamed)} 个文件")
    print("=" * 60)

    if renamed:
        print("\n修改列表：")
        for old, new in renamed:
            print(f"  {old} -> {new}")
