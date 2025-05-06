import re
import os
import zipfile
from telethon.sync import TelegramClient
from telethon.tl.types import Document, DocumentAttributeFilename
from tqdm import tqdm
import time
import shutil
import json
import difflib
from datetime import datetime

# 配置信息
api_id = '27335138'
api_hash = '2459555ba95421148c682e2dc3031bb6'
phone = "+86 15896020219"
channel = 'https://t.me/PandaGroovePG'
group_username = '@pgzdsc'  # 修改为实际的群组用户名
download_path = '/www/xzqzy/lib1/pgdown'  # 下载路径
target_path = '/www/xzqzy/lib1'  # 目标路径
filter = r".*\.zip"  # 文件过滤规则

# 确保 session 文件路径正确
session_file = '/www/pgsc/pg.session'

client = TelegramClient(session_file, api_id, api_hash)

def progress_callback(current, total):
    if not hasattr(progress_callback, "pbar") or progress_callback.pbar is None:
        progress_callback.pbar = tqdm(total=total, unit="B", unit_scale=True, desc="Downloading")
    progress_callback.pbar.n = current
    progress_callback.pbar.refresh()

def close_progress_bar():
    if hasattr(progress_callback, "pbar") and progress_callback.pbar is not None:
        progress_callback.pbar.close()
        progress_callback.pbar = None

def get_file_mtime(file_path):
    """获取文件的最后修改时间"""
    return os.path.getmtime(file_path)

def extract_zip_with_timestamps(zip_path, extract_to):
    """解压文件并保留原始时间信息"""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for zip_info in zip_ref.infolist():
            # 解压文件
            zip_ref.extract(zip_info, extract_to)
            # 设置文件的修改时间和访问时间
            file_path = os.path.join(extract_to, zip_info.filename)
            mod_time = time.mktime(zip_info.date_time + (0, 0, -1))
            os.utime(file_path, (mod_time, mod_time))

async def download_and_extract_latest_file():
    messages = await client.get_messages(channel, limit=10)
    zip_files = []

    for message in messages:
        if message.document and isinstance(message.document, Document):
            if message.document.mime_type == 'application/zip':
                file_name = None
                for attribute in message.document.attributes:
                    if isinstance(attribute, DocumentAttributeFilename):
                        file_name = attribute.file_name

                if file_name and re.match(filter, file_name):
                    zip_files.append((message, file_name))

    zip_files.sort(key=lambda x: x[0].date, reverse=True)

    if zip_files:
        latest_message, latest_file_name = zip_files[0]
        latest_file_path = os.path.join(download_path, latest_file_name)

        print(f"检测到最新的压缩包文件名: {latest_file_name}")
        print(f"本地目标文件夹中的文件名: {os.path.basename(latest_file_path)}")

        # 检查文件是否已存在
        if os.path.exists(latest_file_path):
            print(f"文件 {latest_file_name} 已存在，检查时间戳...")
            existing_file_mtime = get_file_mtime(latest_file_path)
            latest_file_mtime = time.mktime(latest_message.date.timetuple())
            print(f"本地文件时间戳: {existing_file_mtime}")
            print(f"Telegram 频道内文件时间戳: {latest_file_mtime}")
            if existing_file_mtime >= latest_file_mtime:
                print(f"本地文件时间戳更新，跳过下载")
                return
            else:
                print(f"本地文件时间戳较旧，将重新下载")
        else:
            print(f"本地文件不存在，将下载新文件: {latest_file_name}")

        print(f"准备下载新文件: {latest_file_name}")
        try:
            await client.download_media(latest_message, latest_file_path, progress_callback=progress_callback)
            print(f"文件下载完成: {latest_file_path}")
        finally:
            close_progress_bar()

        # 解压文件到下载路径，并保留原始时间信息
        extract_zip_with_timestamps(latest_file_path, download_path)
        print(f"文件已解压到 {download_path}，保留了文件的原始修改日期")

        # 删除旧的压缩包（跳过最新的）
        await delete_all_zip_files(latest_file_name)

        # 比较文件时间信息并更新
        await update_files_with_time_comparison(latest_file_name, latest_message.text)
    else:
        print("没有符合条件的文件")

async def delete_all_zip_files(latest_file_name=None):
    print("开始清理旧的压缩包...")
    zip_files = [f for f in os.listdir(download_path) if f.endswith('.zip')]
    for old_zip in zip_files:
        if old_zip == latest_file_name:
            print(f"保留最新压缩包: {old_zip}")
            continue
        old_zip_path = os.path.join(download_path, old_zip)
        os.remove(old_zip_path)
        print(f"已删除旧压缩包: {old_zip}")

async def compare_and_upload_files(old_file, new_file):
    try:
        with open(old_file, 'r', encoding='utf-8') as f1, open(new_file, 'r', encoding='utf-8') as f2:
            old_lines = f1.readlines()
            new_lines = f2.readlines()
        added_lines = [line for line in new_lines if line not in old_lines]
        deleted_lines = [line for line in old_lines if line not in new_lines]
        if added_lines or deleted_lines:
            change_log = ""
            if added_lines:
                change_log += "新增内容如下：\n" + "\n".join([line.rstrip() for line in added_lines]) + "\n"
            if deleted_lines:
                change_log += "删除内容如下：\n" + "\n".join([line.rstrip() for line in deleted_lines]) + "\n"
            return change_log
        else:
            return None
    except Exception as e:
        print(f"对比文件时出错：{e}")
        return None

async def send_message_in_parts(client, entity, message, max_length=4096):
    while message:
        part = message[:max_length]
        message = message[max_length:]
        await client.send_message(entity, part)
        if message:
            time.sleep(1)  # 避免发送过快导致的限制

async def update_files_with_time_comparison(latest_file_name, message_text):
    print("开始对比文件时间信息并更新...")
    update_files = []
    jsm_diff = []
    jsm_updated = False

    # 遍历下载路径中的所有文件（包括子文件夹内的文件）
    for root, dirs, files in os.walk(download_path):
        for file in files:
            download_file_path = os.path.join(root, file)
            # 目标文件夹中的文件路径（不保留文件夹结构）
            target_file_path = os.path.join(target_path, os.path.basename(file))

            # 跳过最新的压缩包
            if file == latest_file_name:
                print(f"跳过最新压缩包 {latest_file_name}，不拷贝到目标文件夹")
                continue

            # 检查文件是否存在
            if not os.path.exists(download_file_path):
                print(f"文件不存在，跳过: {download_file_path}")
                continue

            # 检查目标文件是否存在并比较时间信息
            if os.path.exists(target_file_path):
                if get_file_mtime(download_file_path) != get_file_mtime(target_file_path):
                    # 时间信息有差异，记录文件名
                    update_files.append(file)
            else:
                # 文件不存在，直接记录
                update_files.append(file)

            # 特别处理 jsm.json 文件，记录内容差异
            if file == "jsm.json":
                old_jsm_path = os.path.join(target_path, "jsm.json")
                new_jsm_path = download_file_path
                diff_log = await compare_and_upload_files(old_jsm_path, new_jsm_path)
                if diff_log:
                    jsm_diff.append(diff_log)
                    jsm_updated = True

    # 如果 jsm.json 有更新，记录到更新文件列表中
    if jsm_updated:
        update_files.append("jsm.json")

    # 拷贝更新的文件到目标文件夹
    for file in update_files:
        # 重新计算下载文件的路径（考虑子文件夹）
        for root, dirs, files in os.walk(download_path):
            if file in files:
                download_file_path = os.path.join(root, file)
                target_file_path = os.path.join(target_path, file)
                if os.path.exists(download_file_path):
                    shutil.copy2(download_file_path, target_file_path)
                    print(f"文件 {file} 已更新到目标文件夹")
                else:
                    print(f"文件不存在，无法拷贝: {download_file_path}")
                break

    # 准备推送信息
    attachment_info = f"PG最新版本：{latest_file_name}\n"
    update_info = f"更新的文件有：{', '.join(update_files)}\n" if update_files else "无文件更新\n"
    content_info = message_text.split('今日更新内容', 1)[1] if '今日更新内容' in message_text else "无更新内容"
    if 'jsm.json' in update_files and jsm_diff:
        update_info += f"jsm.json文件变化内容：\n{''.join(jsm_diff)}\n"
    full_message = attachment_info + update_info + content_info

    # 推送信息到群组
    await send_message_in_parts(client, group_username, full_message)
    print(f"更新信息已转发到群组：{group_username}")

with client:
    client.start(phone=phone)
    if not client.is_user_authorized():
        print("用户未授权，需要手动输入验证码")
        client.send_code_request(phone)
        code = input('Please enter the code you received: ')
        client.sign_in(phone, code)
    else:
        print("用户已授权，直接使用 session 文件")
    client.loop.run_until_complete(download_and_extract_latest_file())