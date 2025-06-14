import os
import sys
import json
import base64
import uuid
import time
import socket
import random
import string
from datetime import datetime, timedelta
from random import randint
from time import sleep, strftime
import requests
import cloudscraper
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
from pystyle import Write, Colors
from rich.console import Console
from rich.text import Text
import pytz  # Thêm module pytz để xử lý múi giờ

init(autoreset=True)
os.system('cls' if os.name == 'nt' else 'clear')
red = "\033[1;31m"
luc = "\033[1;32m"
vang = "\033[1;33m"
cam = "\033[38;5;208m"
tim = "\033[1;35m"
lam = "\033[1;36m"
trang = "\033[1;37m"
listck = []
listjob = []

# Kiểm tra kết nối mạng
def kiem_tra_mang():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=10)
    except OSError:
        print("Mạng không ổn định hoặc bị mất kết nối. Vui lòng kiểm tra lại mạng.")
kiem_tra_mang()

# Hàm hiển thị banner
def banner():
    print(f"""{Fore.YELLOW}╔══════════════════════════════════════════════════════╗
{Fore.YELLOW}║                                                      {Fore.YELLOW}║
{Fore.YELLOW}║  {Fore.WHITE}██████╗░██╗░░░██╗░█████╗░░██████╗██╗░░██║           {Fore.YELLOW}║
{Fore.YELLOW}║  {Fore.WHITE}██╔══██╗██║░░░██║██╔══██╗██╔════╝██║░░██║           {Fore.YELLOW}║
{Fore.YELLOW}║  {Fore.WHITE}██████╦╝██║░░░██║███████║╚█████╗░███████║           {Fore.YELLOW}║
{Fore.YELLOW}║  {Fore.WHITE}██╔══██╗██║░░░██║██╔══██║░╚═══██╗██╔══██║           {Fore.YELLOW}║
{Fore.YELLOW}║  {Fore.WHITE}██████╦╝╚██████╔╝██║░░██║██████╔╝██║░░██║           {Fore.YELLOW}║
{Fore.YELLOW}║  {Fore.WHITE}╚═════╝░░╚═════╝░╚═╝░░╚═╝╚═════╝░╚═╝░░╚═╝           {Fore.YELLOW}║
{Fore.YELLOW}║                                                      {Fore.YELLOW}║             
{Fore.YELLOW}║  {Fore.WHITE}          ░█████╗░███╗░░██║░██████╗░                {Fore.YELLOW}║
{Fore.YELLOW}║  {Fore.WHITE}          ██╔══██╗████╗░██║██╔════╝░                {Fore.YELLOW}║
{Fore.YELLOW}║  {Fore.WHITE}          ███████║██╔██╗██║██║░░██╗░                {Fore.YELLOW}║
{Fore.YELLOW}║  {Fore.WHITE}          ██╔══██║██║╚████║██║░░╚██╗                {Fore.YELLOW}║
{Fore.YELLOW}║  {Fore.WHITE}          ██║░░██║██║░╚███║╚██████╔╝                {Fore.YELLOW}║
{Fore.YELLOW}║  {Fore.WHITE}          ╚═╝░░╚═╝╚═╝░░╚══╝░╚═════╝░                {Fore.YELLOW}║
{Fore.YELLOW}║                                                      {Fore.YELLOW}║
{Fore.YELLOW}║                                                      {Fore.YELLOW}║
{Fore.YELLOW}║                                                      {Fore.YELLOW}║
{Fore.YELLOW}║              {Fore.YELLOW}Ngày: {datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime('%d/%m/%Y %H:%M:%S')}               {Fore.YELLOW}║
{Fore.YELLOW}╚══════════════════════════════════════════════════════╝
""")    
banner()

console = Console()

# Hàm lấy link rút gọn từ YeuMoney
def get_shortened_link_yeumoney(url):
    token = "e08f033dc21da1dbc122f1bc883f61ba343fa5ff0b2816de7c32ab137b44e112"  # Thay bằng token của bạn
    api_url = f"https://yeumoney.com/QL_api.php?token={token}&format=text&url={url}"
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            return response.text.strip()  # Lấy link rút gọn
        else:
            return "Lỗi khi kết nối API!"
    except Exception as e:
        return f"Lỗi"

# Hàm tạo key ngẫu nhiên
def generate_random_key(length=8):
    """Tạo chuỗi ngẫu nhiên với chữ cái + số."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))

# Hàm tạo key
def generate_key(is_admin=False):
    """Tạo key, admin key không hết hạn."""
    if is_admin:
        return "BUASHANGKEYVIP"  # Key admin không có ngày hết hạn
    else:
        return f"BUASHANGDZAI-{generate_random_key(10)}"  # Key user

# Hàm lấy thời gian từ module datetime và pytz
def get_current_time_from_api():
    """Lấy thời gian hệ thống cục bộ với múi giờ Việt Nam (Asia/Ho_Chi_Minh)."""
    try:
        # Lấy thời gian hệ thống với múi giờ Việt Nam (+07:00)
        tz = pytz.timezone("Asia/Ho_Chi_Minh")
        current_time = datetime.now(tz)
        return current_time.replace(tzinfo=None)  # Loại bỏ thông tin múi giờ để tương thích với code hiện tại
    except Exception as e:
        print(f"Lỗi khi lấy thời gian hệ thống: {e}")
        return datetime.now()  # Dự phòng nếu có lỗi

# Hàm mã hóa thời gian thành base64
def encode_time(dt):
    """Chuyển thời gian thành epoch (số giây) và mã hóa base64."""
    epoch = int(dt.timestamp())
    return base64.b64encode(str(epoch).encode()).decode()

# Hàm giải mã thời gian từ base64
def decode_time(encoded):
    """Giải mã base64 và chuyển epoch thành datetime."""
    epoch = int(base64.b64decode(encoded).decode())
    return datetime.fromtimestamp(epoch)

# Hàm lưu key vào file (ẩn thời gian)
def save_key_to_file(key):
    """Lưu key vào file với thời gian tạo và hết hạn mã hóa base64."""
    timestamp = get_current_time_from_api()  # Thời gian từ hệ thống
    expiry_time = timestamp + timedelta(hours=12)  # Hết hạn sau 12 tiếng
    encoded_timestamp = encode_time(timestamp)
    encoded_expiry = encode_time(expiry_time)
    with open("key.txt", "w") as f:  # Ghi đè file
        f.write(f"{key} | {encoded_timestamp} | {encoded_expiry}\n")

# Hàm kiểm tra và xóa key nếu đã hết hạn
def clean_expired_key():
    """Xóa key nếu đã hết hạn (sau 12 tiếng)."""
    if not os.path.exists("key.txt"):
        return    
    updated_lines = []
    current_time = get_current_time_from_api()  # Thời gian từ hệ thống    
    with open("key.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            try:
                key, encoded_timestamp, encoded_expiry = line.strip().split(" | ")
                expiry = decode_time(encoded_expiry)
                # Nếu key là admin hoặc chưa hết hạn, giữ lại
                if key.startswith("BUASHANGKEYVIP") or current_time <= expiry:
                    updated_lines.append(line)
            except:
                continue    
    # Ghi lại key còn hiệu lực
    with open("key.txt", "w") as f:
        f.writelines(updated_lines)

# Hàm kiểm tra key đã lưu và còn hạn không
def check_stored_key():
    """Kiểm tra xem có key nào còn hạn trong file không, trả về key và thời gian hết hạn nếu hợp lệ."""
    clean_expired_key()  # Dọn dẹp key hết hạn trước    
    if not os.path.exists("key.txt"):
        return None, None, None    
    current_time = get_current_time_from_api()  # Thời gian từ hệ thống
    with open("key.txt", "r") as f:
        for line in f:
            try:
                stored_key, encoded_timestamp, encoded_expiry = line.strip().split(" | ")
                stored_key = stored_key.strip()
                expiry = decode_time(encoded_expiry)
                if stored_key == "BUASHANGKEYVIP":
                    return stored_key, stored_key, None  # Key admin không có thời gian hết hạn
                elif stored_key.startswith("BUASHANGDZAI-") and current_time <= expiry:
                    return stored_key, stored_key, expiry  # Key còn hạn, trả về thời gian hết hạn
            except:
                continue
    return None, None, None

# Hàm kiểm tra key hợp lệ
def is_valid_key(key, expected_key):
    """Kiểm tra key có hợp lệ không."""
    clean_expired_key()  # Dọn dẹp key hết hạn trước    
    if key == "BUASHANGKEYVIP":
        return True  # Key admin hợp lệ mọi lúc
    elif key == expected_key:  # So sánh với key đã tạo
        return True
    return False

# Hàm tính thời gian còn lại dưới dạng giờ, phút, giây
def format_time_remaining(expiry, current_time):
    """Tính thời gian còn lại và định dạng thành giờ, phút, giây."""
    time_diff = expiry - current_time
    total_seconds = int(time_diff.total_seconds())
    if total_seconds <= 0:
        return "Hết hạn"
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours} giờ {minutes} phút {seconds} giây"

# ======= Chạy Tool =======
try:
    admin_key = "BUASHANGKEYVIP"    
    # Kiểm tra xem có key nào còn hạn trong file không
    stored_key, user_key, expiry = check_stored_key()    
    # Nếu không có key còn hạn, tạo key mới và yêu cầu người dùng vượt link
    if not stored_key:
        user_key = generate_key(is_admin=False)
        # Tạo link YeuMoney chứa key
        link_can_rut = f"https://flowing-silo-450510-e1.web.app/key/?ma={user_key}"  # Thay bằng URL mới của bạn
        short_link = get_shortened_link_yeumoney(link_can_rut)
        console.print(f"[bold red][bold yellow]LINK[/bold yellow] [bold white]|[/bold white] [bold magenta]VƯỢT LINK ĐỂ LẤY KEY[/bold magenta][/bold red] [bold green]: {short_link}[/bold green]")        
        while True:
            nhap_key = console.input("[bold blue][[bold red]NHẬP KEY[/bold red]][/bold blue][bold yellow]==>> [/bold yellow]").strip()           
            if is_valid_key(nhap_key, user_key):
                # Lưu key vừa nhập thành công vào file (ghi đè key cũ)
                save_key_to_file(nhap_key)
                print("\nKey hợp lệ! Đang vào Tool...", end="\r")
                time.sleep(3)  # Chờ 3 giây trước khi vào tool
                print("\033[F\033[K" * 3, end="")  # Xóa 3 dòng vừa in
                break  
            else:
                print("\nKey không hợp lệ. Vui lòng vượt link để lấy key!", end="\r")
                time.sleep(2)
                print("\033[F\033[K" * 2, end="")  # Xóa 2 dòng vừa in
    else:
        # Nếu có key còn hạn, hiển thị link YeuMoney và thời gian còn lại
        link_can_rut = f"https://flowing-silo-450510-e1.web.app/key/?ma={user_key}"
        short_link = get_shortened_link_yeumoney(link_can_rut)
        if expiry:  # Nếu key không phải key admin (có thời gian hết hạn)
            current_time = get_current_time_from_api()
            time_remaining = format_time_remaining(expiry, current_time)
            console.print(f"[bold green]Key [bold blue]{stored_key}[/bold blue] còn hạn (Thời gian còn lại: [bold yellow]{time_remaining}[/bold yellow]). Đang vào Tool...[/bold green]")
        else:  # Nếu là key admin (không có thời gian hết hạn)
            console.print(f"[bold green]Key [bold blue]{stored_key}[/bold blue] là key vĩnh viễn. Đang vào Tool...[/bold green]")
        time.sleep(6)  # Chờ 2 giây trước khi vào tool
        print("\033[F\033[K" * 4, end="")
except Exception as e:
    console.print(f"[bold red]ErrolKey: {e}[/bold red]")
os.system("cls" if os.name == "nt" else "clear")