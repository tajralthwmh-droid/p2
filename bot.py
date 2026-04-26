import requests, uuid, re, random, time, string, secrets, json, threading
from datetime import datetime
from colorama import Fore, init
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio
from flask import Flask
import os
from os import environ

# تهيئة الألوان
init(autoreset=True)

# ========== التوكن والايدي مثبتين هنا ==========
BOT_TOKEN = "8513010794:AAH9_FatomlJIIPbCBajnYuRhYy2BcqwBxY"
ADMIN_ID = "8311254462"
# =============================================

# ------------------- إعدادات Flask الأساسية -------------------
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "✅ البوت يعمل بنجاح! (نسخة التخفي القصوى)", 200

def run_flask():
    port = int(environ.get('PORT', 8080))
    app_flask.run(host='0.0.0.0', port=port)

# ------------------- نظام البروكسيات المتقدم -------------------
class ProxyManager:
    """مدير متقدم للبروكسيات مع تجديد تلقائي"""
    
    def __init__(self):
        self.proxies = []
        self.current_proxy_index = 0
        self.failed_proxies = set()
        self.last_update = 0
        
    def fetch_free_proxies(self):
        """جلب بروكسيات مجانية من عدة مصادر"""
        proxies_list = []
        
        # مصدر 1: FreeProxyList
        try:
            resp = requests.get('https://free-proxy-list.net/', timeout=10)
            matches = re.findall(r'(\d+\.\d+\.\d+\.\d+):(\d+)', resp.text)
            for ip, port in matches[:50]:
                proxies_list.append(f'http://{ip}:{port}')
        except:
            pass
        
        # مصدر 2: ProxyScrape
        try:
            resp = requests.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all', timeout=10)
            for line in resp.text.strip().split('\n'):
                if ':' in line:
                    proxies_list.append(f'http://{line.strip()}')
        except:
            pass
        
        # مصدر 3: PubProxy
        try:
            resp = requests.get('https://pubproxy.com/api/proxy?limit=20&format=txt&http=true', timeout=10)
            for line in resp.text.strip().split('\n'):
                if line.strip():
                    proxies_list.append(f'http://{line.strip()}')
        except:
            pass
        
        # تصفية البروكسيات الفاشلة سابقاً
        self.proxies = [p for p in proxies_list if p not in self.failed_proxies]
        print(Fore.GREEN + f"[+] تم جلب {len(self.proxies)} بروكسي" + Fore.RESET)
        return self.proxies
    
    def get_next_proxy(self):
        """الحصول على البروكسي التالي (Round Robin)"""
        if not self.proxies:
            self.fetch_free_proxies()
        
        if self.proxies:
            proxy = self.proxies[self.current_proxy_index % len(self.proxies)]
            self.current_proxy_index += 1
            return {'http': proxy, 'https': proxy}
        return None
    
    def mark_failed(self, proxy):
        """تحديد بروكسي فاشل لتجنبه مستقبلاً"""
        if proxy:
            self.failed_proxies.add(proxy.get('http', ''))
            self.proxies = [p for p in self.proxies if p != proxy.get('http', '')]
            print(Fore.YELLOW + f"[!] تم استبعاد بروكسي فاشل" + Fore.RESET)
    
    def rotate_proxy(self):
        """تغيير البروكسي بشكل إجباري"""
        self.current_proxy_index += random.randint(1, 5)
        return self.get_next_proxy()

# إنشاء مدير البروكسيات
proxy_manager = ProxyManager()

# ========== تقنيات تخفي متطورة جداً ==========
try:
    from user_agent import generate_user_agent
    USE_ADVANCED_UA = True
except ImportError:
    USE_ADVANCED_UA = False

# قائمة واسعة من User-Agent الحقيقية
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
    'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
]

def get_stealth_user_agent():
    """توليد User-Agent متطور مع تفضيل استخدام المكتبة المتقدمة"""
    if USE_ADVANCED_UA and random.random() > 0.3:
        try:
            return generate_user_agent()
        except:
            pass
    return random.choice(USER_AGENTS)

def generate_instagram_ua():
    """توليد User-Agent خاص بـ Instagram يشبه تماماً التطبيق الحقيقي"""
    models = ['SM-S918B', 'Pixel 8 Pro', 'iPhone15,2', 'SM-F946B', 'Redmi Note 13 Pro+', 'OnePlus 12', 'Xiaomi 14 Pro']
    android_versions = ['13', '14', '15']
    instagram_versions = [297, 298, 299, 300, 301, 302, 303, 304, 305]
    
    return f'Mozilla/5.0 (Linux; Android {random.choice(android_versions)}; {random.choice(models)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(118,125)}.0.0.0 Mobile Safari/537.36 Instagram {random.choice(instagram_versions)}.0.0.{random.randint(25,45)} Android'

def generate_csrf_token():
    """توليد CSRF Token آمن جداً"""
    return secrets.token_urlsafe(32)

def random_device_id():
    return str(uuid.uuid4()).upper()

def random_mid():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=22))

def random_jazoest():
    return str(random.randint(22000, 24500))

def generate_password():
    """توليد كلمة مرور قوية جداً (12-16 حرف)"""
    letters = string.ascii_letters
    digits = string.digits
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    password = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice(symbols),
    ]
    password += random.choices(letters + digits + symbols, k=random.randint(12, 16))
    random.shuffle(password)
    return ''.join(password)

def send_telegram_message(message):
    """إرسال رسالة للتليجرام"""
    if BOT_TOKEN and ADMIN_ID:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            data = {"chat_id": ADMIN_ID, "text": message, "parse_mode": "HTML"}
            requests.post(url, data=data, timeout=15)
        except:
            pass

def random_delay(min_sec=2, max_sec=8):
    """تأخير عشوائي بشري"""
    time.sleep(random.uniform(min_sec, max_sec))

# ========== دوال البريد المؤقت المتقدمة ==========
def create_temp_email():
    """إنشاء بريد مؤقت مع عدة مصادر"""
    # مصدر 1: 1secmail
    try:
        resp = requests.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1', timeout=15)
        if resp.status_code == 200:
            return resp.json()[0]
    except:
        pass
    
    # مصدر 2: Temp-Mail
    try:
        headers = {
            'accept': '*/*',
            'application-name': 'web',
            'content-type': 'application/json',
            'user-agent': get_stealth_user_agent(),
        }
        json_data = {'min_name_length': 10, 'max_name_length': 10}
        resp = requests.post('https://api.internal.temp-mail.io/api/v3/email/new', 
                            headers=headers, json=json_data, timeout=15)
        if resp.status_code == 200:
            return resp.json().get("email")
    except:
        pass
    
    # مصدر 3: Guerrilla Mail (بديل)
    try:
        resp = requests.get('https://api.guerrillamail.com/ajax.php?f=get_email_address', timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            if data.get('email_addr'):
                return data.get('email_addr')
    except:
        pass
    
    return None

def get_messages(email_address):
    """الحصول على الرسائل من عدة خدمات بريد"""
    # محاولة 1secmail
    try:
        name, domain = email_address.split('@')
        resp = requests.get(f'https://www.1secmail.com/api/v1/?action=getMessages&login={name}&domain={domain}', timeout=15)
        if resp.status_code == 200 and resp.json():
            return resp.json()
    except:
        pass
    
    # محاولة Temp-Mail
    try:
        headers = {'accept': '*/*', 'user-agent': get_stealth_user_agent()}
        resp = requests.get(f'https://api.internal.temp-mail.io/api/v3/email/{email_address}/messages', 
                           headers=headers, timeout=15)
        if resp.status_code == 200 and resp.json():
            return resp.json()
    except:
        pass
    
    return []

def wait_for_verification_code(email_address, max_wait=210):
    """انتظار كود التفعيل مع تأخيرات ذكية"""
    print(f"[ * ] انتظار كود التفعيل على {email_address} ...")
    start_time = time.time()
    attempts = 0
    
    while time.time() - start_time < max_wait:
        attempts += 1
        messages = get_messages(email_address)
        
        if messages:
            for msg in messages:
                subject = str(msg.get('subject', '')).lower()
                body = msg.get('body', '') or msg.get('body_text', '') or msg.get('mailText', '')
                
                if any(x in subject for x in ["verify", "code", "instagram", "confirmation", "activate"]):
                    matches = re.findall(r'\b(\d{6})\b', body)
                    if matches:
                        code = matches[0]
                        print(f"[ + ] تم استلام الكود: {code}")
                        return code
        
        # تأخير ذكي يزداد مع كل محاولة
        delay = min(6 + (attempts // 2), 12)
        time.sleep(random.uniform(delay, delay + 3))
    
    print("[ - ] لم يتم استلام الكود")
    return ""

def random_string(length=12):
    return ''.join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=length))

def make_with_proxy():
    """دالة الإنشاء الرئيسية مع دعم البروكسيات وتقنيات تخفي متطورة"""
    print("\n" + Fore.CYAN + "="*50 + Fore.RESET)
    print(Fore.CYAN + "[ * ] بدء عملية إنشاء حساب جديدة..." + Fore.RESET)
    
    # تغيير البروكسي لكل محاولة
    proxy = proxy_manager.get_next_proxy()
    if proxy:
        print(Fore.CYAN + f"[ * ] استخدام بروكسي جديد" + Fore.RESET)
    
    random_delay(4, 8)
    
    print("[ * ] جاري إنشاء بريد مؤقت...")
    random_delay(2, 4)
    
    email = create_temp_email()
    if not email:
        print(Fore.RED + "[ - ] فشل إنشاء البريد المؤقت" + Fore.RESET)
        return False, None, None, None, None
    
    print(Fore.GREEN + f"[ + ] البريد الإلكتروني: {email}" + Fore.RESET)
    random_delay(3, 6)
    
    # توليد بيانات فريدة تماماً
    device_id = random_device_id()
    mid = random_mid()
    csrftoken = generate_csrf_token()
    jazoest1 = random_jazoest()
    jazoest2 = random_jazoest()
    session_id = f':{random_string(10)}:{random_string(12)}'
    
    cookies = {
        'ig_did': device_id,
        'dpr': str(random.randint(1, 3)),
        'mid': mid,
        'csrftoken': csrftoken,
        'datr': generate_csrf_token()[:24],
        'wd': f'{random.randint(360, 414)}x{random.randint(600, 900)}',
        'sessionid': session_id,
    }
    
    headers = {
        'User-Agent': generate_instagram_ua(),
        'Content-Type': 'application/x-www-form-urlencoded',
        'x-ig-app-id': '1217981644879628',
        'x-requested-with': 'XMLHttpRequest',
        'x-csrftoken': csrftoken,
        'x-web-session-id': session_id,
        'origin': 'https://www.instagram.com',
        'referer': 'https://www.instagram.com/accounts/signup/email/',
        'accept-language': 'ar-IQ,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'accept-encoding': 'gzip, deflate, br',
        'sec-ch-ua': f'"Not_A Brand";v="8", "Chromium";v="{random.randint(118,124)}", "Google Chrome";v="{random.randint(118,124)}"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': f'"{random.choice(["Windows", "macOS", "Linux"])}"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
    }
    
    # 1. التحقق من البريد
    print("[ * ] جاري التحقق من البريد...")
    data = {'email': email, 'jazoest': jazoest1}
    
    try:
        response = requests.post('https://www.instagram.com/api/v1/web/accounts/check_email/', 
                                cookies=cookies, headers=headers, data=data, timeout=25, proxies=proxy)
        if response.status_code != 200:
            print(Fore.RED + "[ - ] فشل التحقق من البريد" + Fore.RESET)
            if proxy:
                proxy_manager.mark_failed(proxy)
            return False, None, None, None, None
    except Exception as e:
        print(Fore.RED + f"[ - ] خطأ في التحقق: {e}" + Fore.RESET)
        if proxy:
            proxy_manager.mark_failed(proxy)
        return False, None, None, None, None
    
    random_delay(4, 8)
    
    # 2. طلب الكود
    print("[ * ] جاري طلب كود التفعيل...")
    data = {'device_id': device_id, 'email': email, 'jazoest': jazoest1}
    
    try:
        response = requests.post('https://www.instagram.com/api/v1/accounts/send_verify_email/', 
                                cookies=cookies, headers=headers, data=data, timeout=25, proxies=proxy)
        if response.status_code != 200:
            print(Fore.RED + "[ - ] فشل طلب الكود" + Fore.RESET)
            return False, None, None, None, None
    except Exception as e:
        print(Fore.RED + f"[ - ] خطأ في طلب الكود: {e}" + Fore.RESET)
        return False, None, None, None, None
    
    random_delay(5, 10)
    
    # 3. انتظار الكود
    code = wait_for_verification_code(email)
    if not code:
        return False, None, None, None, None
    
    random_delay(3, 6)
    
    # 4. تأكيد الكود
    print("[ * ] جاري تأكيد الكود...")
    headers['referer'] = 'https://www.instagram.com/accounts/signup/emailConfirmation/'
    data = {'code': code, 'device_id': device_id, 'email': email, 'jazoest': jazoest1}
    
    try:
        response = requests.post('https://www.instagram.com/api/v1/accounts/check_confirmation_code/', 
                                cookies=cookies, headers=headers, data=data, timeout=25, proxies=proxy)
        
        if response.status_code != 200:
            print(Fore.RED + "[ - ] فشل تأكيد الكود" + Fore.RESET)
            return False, None, None, None, None
        
        response_json = response.json()
        
        if response_json.get('spam'):
            print(Fore.RED + f"[ - ] ❌ تم اكتشاف نشاط آلي (Spam)" + Fore.RESET)
            print(Fore.YELLOW + f"     السبب: {response_json.get('feedback_message', 'غير معروف')}" + Fore.RESET)
            return False, None, None, None, None
        
        rc = response_json.get("signup_code", "")
        
    except Exception as e:
        print(Fore.RED + f"[ - ] خطأ في تأكيد الكود: {e}" + Fore.RESET)
        return False, None, None, None, None
    
    random_delay(3, 6)
    
    # توليد بيانات عشوائية
    username = random_string(random.randint(10, 16))
    password = generate_password()
    first_name = random_string(random.randint(6, 10)).capitalize()
    day = random.randint(1, 28)
    month = random.randint(1, 12)
    year = random.randint(1988, 2005)
    
    # 5. محاولة إنشاء أولية
    headers['referer'] = 'https://www.instagram.com/accounts/signup/name/'
    data = {
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
        'email': email,
        'failed_birthday_year_count': '{}',
        'first_name': first_name,
        'username': username,
        'seamless_login_enabled': '1',
        'use_new_suggested_user_name': 'true',
        'jazoest': jazoest2,
    }
    
    try:
        requests.post('https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/', 
                     cookies=cookies, headers=headers, data=data, timeout=20, proxies=proxy)
    except:
        pass
    
    random_delay(3, 5)
    
    # 6. التحقق من العمر
    headers['referer'] = 'https://www.instagram.com/accounts/signup/birthday/'
    data = {'day': str(day), 'month': str(month), 'year': str(year), 'jazoest': jazoest2}
    
    try:
        requests.post('https://www.instagram.com/api/v1/web/consent/check_age_eligibility/', 
                     cookies=cookies, headers=headers, data=data, timeout=20, proxies=proxy)
    except:
        pass
    
    random_delay(3, 5)
    
    # 7. طلب اقتراحات اسم المستخدم
    data = {'email': email, 'name': first_name, 'jazoest': jazoest2}
    
    try:
        requests.post('https://www.instagram.com/api/v1/web/accounts/username_suggestions/', 
                     cookies=cookies, headers=headers, data=data, timeout=20, proxies=proxy)
    except:
        pass
    
    random_delay(3, 5)
    
    # 8. الإنشاء النهائي
    print("[ * ] جاري إنشاء الحساب...")
    headers['referer'] = 'https://www.instagram.com/accounts/signup/username/'
    data = {
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
        'day': str(day),
        'email': email,
        'failed_birthday_year_count': '{}',
        'first_name': first_name,
        'month': str(month),
        'username': username,
        'year': str(year),
        'client_id': device_id,
        'seamless_login_enabled': '1',
        'tos_version': 'row',
        'force_sign_up_code': rc,
        'extra_session_id': session_id,
        'jazoest': jazoest2,
    }
    
    try:
        response = requests.post('https://www.instagram.com/api/v1/web/accounts/web_create_ajax/', 
                                cookies=cookies, headers=headers, data=data, timeout=35, proxies=proxy)
        
        try:
            response_json = response.json()
        except:
            response_json = {}
        
        if 'user_id' in response.text or response_json.get('user_id'):
            now = datetime.now()
            user_id = response_json.get('user_id', 'Unknown')
            
            print(Fore.GREEN + f"\n[ + ] ✅ تم إنشاء الحساب بنجاح! {now.strftime('%H:%M:%S')}")
            print(f"[ + ] 📧 البريد: {email}")
            print(f"[ + ] 👤 المستخدم: {username}")
            print(f"[ + ] 🔑 كلمة المرور: {password}")
            print(f"[ + ] 🆔 المعرف: {user_id}" + Fore.RESET)
            
            success_message = f"""✅ <b>تم إنشاء الحساب!</b>
📧 {email}
👤 {username}
🔑 {password}
🆔 {user_id}
📅 {now.strftime('%Y-%m-%d %H:%M:%S')}"""
            
            with open("accounts.txt", "a", encoding="utf-8") as f:
                f.write(f"{now.strftime('%Y-%m-%d %H:%M:%S')} | {email} | {username} | {password} | {user_id}\n")
            
            send_telegram_message(success_message)
            return True, email, username, password, user_id
        else:
            error_msg = response.text[:200]
            if 'spam' in error_msg.lower() or 'limit' in error_msg.lower():
                print(Fore.RED + f"\n[ - ] ❌ فشل الإنشاء - تم اكتشاف نشاط آلي" + Fore.RESET)
                print(Fore.YELLOW + "     السبب: Instagram يحظر المحاولات حالياً" + Fore.RESET)
                if proxy:
                    proxy_manager.mark_failed(proxy)
            else:
                print(Fore.RED + f"\n[ - ] ❌ فشل الإنشاء - سبب غير معروف" + Fore.RESET)
            return False, None, None, None, None
            
    except Exception as e:
        print(Fore.RED + f"[ - ] خطأ: {e}" + Fore.RESET)
        if proxy:
            proxy_manager.mark_failed(proxy)
        return False, None, None, None, None

# ===== واجهة البوت المتطورة =====
async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id=None):
    keyboard = [
        [InlineKeyboardButton("📝 إنشاء حساب (مع بروكسي)", callback_data="create_one")],
        [InlineKeyboardButton("📊 تحديث البروكسيات", callback_data="update_proxies")],
        [InlineKeyboardButton("ℹ️ معلومات البروكسيات", callback_data="proxy_info")],
        [InlineKeyboardButton("📁 عرض الحسابات", callback_data="show_accounts")],
        [InlineKeyboardButton("🗑️ مسح الحسابات", callback_data="clear_accounts")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = """🤖 *بوت إنشاء حسابات Instagram - النسخة المتطورة*

🛡️ *تقنيات التخفي:*
• ✅ بروكسيات متجددة تلقائياً
• ✅ بصمة رقمية فريدة لكل محاولة
• ✅ User-Agent متطورة جداً
• ✅ تأخيرات ذكية متغيرة
• ✅ خدمات بريد متعددة

اختر الإجراء المناسب:"""
    
    if chat_id:
        await context.bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown", reply_markup=reply_markup)
    else:
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await main_menu(update, context)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id
    
    if data == "create_one":
        msg = await query.edit_message_text("🔄 جاري إنشاء حساب مع بروكسي جديد...\n⏱️ قد يستغرق 2-3 دقائق")
        
        # تغيير البروكسي قبل البدء
        proxy_manager.rotate_proxy()
        
        success, email, username, password, uid = make_with_proxy()
        if success:
            text = f"""✅ *تم إنشاء الحساب بنجاح!*

📧 البريد: `{email}`
👤 المستخدم: `{username}`
🔑 كلمة المرور: `{password}`
🆔 المعرف: `{uid}`

📁 تم حفظ الحساب في ملف accounts.txt"""
            await query.edit_message_text(text, parse_mode="Markdown")
        else:
            await query.edit_message_text("❌ *فشل إنشاء الحساب*\n\nInstagram يحظر المحاولات حالياً.\nتم تغيير البروكسي تلقائياً للمحاولة التالية.\n\n⏰ انتظر 30 دقيقة ثم حاول مرة أخرى.", parse_mode="Markdown")
        
        await asyncio.sleep(3)
        await main_menu(update, context, chat_id=user_id)
    
    elif data == "update_proxies":
        await query.edit_message_text("🔄 جاري تحديث قائمة البروكسيات...")
        proxy_manager.fetch_free_proxies()
        count = len(proxy_manager.proxies)
        await query.edit_message_text(f"✅ *تم تحديث البروكسيات!*\n📊 عدد البروكسيات المتاحة: {count}", parse_mode="Markdown")
        await asyncio.sleep(2)
        await main_menu(update, context, chat_id=user_id)
    
    elif data == "proxy_info":
        count = len(proxy_manager.proxies)
        text = f"""ℹ️ *معلومات البروكسيات*

📊 *الإحصائيات:*
• عدد البروكسيات المتاحة: {count}
• البروكسي الحالي: {proxy_manager.current_proxy_index % max(1, count) if count > 0 else 0}

🔄 *آلية العمل:*
• يتم تغيير البروكسي لكل محاولة
• يتم استبعاد البروكسيات الفاشلة تلقائياً
• يتم تحديث القائمة كل 30 محاولة

💡 *نصيحة:* 
• استخدم زر تحديث البروكسيات قبل البدء
• انتظر 5-10 ثواني بين المحاولات"""
        await query.edit_message_text(text, parse_mode="Markdown")
        await asyncio.sleep(3)
        await main_menu(update, context, chat_id=user_id)
    
    elif data == "show_accounts":
        try:
            with open("accounts.txt", "r") as f:
                acc = f.readlines()
            if acc:
                text = "📁 *آخر الحسابات المحفوظة:*\n\n" + "".join(acc[-10:])
                await query.edit_message_text(text, parse_mode="Markdown")
            else:
                await query.edit_message_text("📁 *لا توجد حسابات محفوظة*", parse_mode="Markdown")
        except:
            await query.edit_message_text("📁 *لا توجد حسابات محفوظة*", parse_mode="Markdown")
        await asyncio.sleep(2)
        await main_menu(update, context, chat_id=user_id)
    
    elif data == "clear_accounts":
        open("accounts.txt", "w").close()
        await query.edit_message_text("✅ *تم مسح جميع الحسابات بنجاح*", parse_mode="Markdown")
        await asyncio.sleep(1)
        await main_menu(update, context, chat_id=user_id)

# ------------------- الكود الرئيسي للتشغيل -------------------
if __name__ == "__main__":
    print(Fore.CYAN + """
╔══════════════════════════════════════════════════╗
║     Instagram Account Creator Bot                ║
║         النسخة المتطورة v6.0                    ║
║     مع دعم البروكسيات والتخفي القصوى            ║
╚══════════════════════════════════════════════════╝
""" + Fore.RESET)
    
    # جلب البروكسيات أولاً
    print(Fore.YELLOW + "[ * ] جاري جلب البروكسيات..." + Fore.RESET)
    proxy_manager.fetch_free_proxies()
    print(Fore.GREEN + f"[ + ] تم تجهيز {len(proxy_manager.proxies)} بروكسي" + Fore.RESET)
    
    # تشغيل Flask في خيط منفصل
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # تشغيل بوت Telegram
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print(Fore.GREEN + "✅ البوت يعمل! أرسل /start" + Fore.RESET)
    print(Fore.CYAN + f"🤖 التوكن: {BOT_TOKEN[:20]}...")
    print(f"👤 الايدي: {ADMIN_ID}")
    print(f"🔄 عدد البروكسيات: {len(proxy_manager.proxies)}" + Fore.RESET)
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)
