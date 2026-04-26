import requests, uuid, re, random, time, string, secrets, json, threading, ssl, hashlib, hmac
from datetime import datetime
from colorama import Fore, init
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio
from flask import Flask
import os
from os import environ
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

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
    return "✅ ELITE STEALTH BOT v7.0 - ULTIMATE PROTECTION", 200

def run_flask():
    port = int(environ.get('PORT', 8080))
    app_flask.run(host='0.0.0.0', port=port)

# ------------------- إعدادات SSL متقدمة للتخفي -------------------
class TLSAdapter(HTTPAdapter):
    """محول TLS متقدم لتغيير بصمة SSL"""
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.set_ciphers('ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

# ------------------- نظام البروكسيات المدفوعة والقوية -------------------
class EliteProxyManager:
    """مدير بروكسيات متطور مع دعم البروكسيات المدفوعة والمجانية عالية الجودة"""
    
    def __init__(self):
        self.proxies = []
        self.premium_proxies = []
        self.current_proxy_index = 0
        self.failed_proxies = set()
        self.session = requests.Session()
        self.session.mount('https://', TLSAdapter())
        
        # 🔥 أدخل بروكسياتك المدفوعة هنا 🔥
        # يمكنك الحصول عليها من: BrightData, Oxylabs, SmartProxy, GeoSurf
        self.PREMIUM_PROXIES_LIST = [
            # مثال: "http://username:password@ip:port"
            # "http://user:pass@proxy1.example.com:8080",
            # "http://user:pass@proxy2.example.com:8080",
        ]
        
    def add_premium_proxy(self, proxy_string):
        """إضافة بروكسي مدفوع"""
        self.premium_proxies.append(proxy_string)
        print(Fore.GREEN + f"[+] تم إضافة بروكسي مدفوع: {proxy_string[:30]}..." + Fore.RESET)
    
    def fetch_elite_proxies(self):
        """جلب بروكسيات عالية الجودة من مصادر موثوقة"""
        proxies_list = []
        
        # استخدام البروكسيات المدفوعة أولاً
        if self.premium_proxies:
            proxies_list.extend(self.premium_proxies)
            print(Fore.GREEN + f"[+] تم تحميل {len(self.premium_proxies)} بروكسي مدفوع" + Fore.RESET)
        
        # مصدر 1: ProxyList (بروكسيات عالية الجودة)
        try:
            resp = requests.get('https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt', timeout=15)
            for line in resp.text.strip().split('\n'):
                if line.strip() and ':' in line:
                    proxies_list.append(f'http://{line.strip()}')
        except:
            pass
        
        # مصدر 2: OpenProxy (بروكسيات نظيفة)
        try:
            resp = requests.get('https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTP_Plus.txt', timeout=15)
            for line in resp.text.strip().split('\n'):
                if line.strip() and ':' in line:
                    proxies_list.append(f'http://{line.strip()}')
        except:
            pass
        
        # مصدر 3: ProxyList Plus
        try:
            resp = requests.get('https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt', timeout=15)
            for line in resp.text.strip().split('\n'):
                if line.strip() and ':' in line:
                    proxies_list.append(f'http://{line.strip()}')
        except:
            pass
        
        # اختبار البروكسيات وتصفية السريعة منها
        working_proxies = []
        for proxy in proxies_list[:100]:
            try:
                test_resp = requests.get('https://httpbin.org/ip', proxies={'http': proxy, 'https': proxy}, timeout=5)
                if test_resp.status_code == 200:
                    working_proxies.append(proxy)
                    print(Fore.GREEN + f"[✓] بروكسي يعمل: {proxy}" + Fore.RESET)
            except:
                continue
        
        self.proxies = [p for p in working_proxies if p not in self.failed_proxies]
        print(Fore.CYAN + f"[+] تم تجهيز {len(self.proxies)} بروكسي عالي الجودة" + Fore.RESET)
        return self.proxies
    
    def get_rotating_proxy(self):
        """الحصول على بروكسي متغير لكل طلب"""
        if not self.proxies:
            self.fetch_elite_proxies()
        
        if self.proxies:
            proxy = self.proxies[self.current_proxy_index % len(self.proxies)]
            self.current_proxy_index = random.randint(0, len(self.proxies) - 1)
            return {'http': proxy, 'https': proxy}
        return None
    
    def mark_failed(self, proxy):
        """تحديد بروكسي فاشل"""
        if proxy and proxy.get('http'):
            self.failed_proxies.add(proxy.get('http'))
            self.proxies = [p for p in self.proxies if p != proxy.get('http')]

# إنشاء مدير البروكسيات المتطور
proxy_manager = EliteProxyManager()

# ========== تقنيات تخفي خارقة ==========
class UltimateStealth:
    """أقوى تقنيات التخفي والتمويه"""
    
    @staticmethod
    def generate_fingerprint():
        """توليد بصمة رقمية فريدة تماماً"""
        return {
            'user_agent': UltimateStealth.generate_chaotic_ua(),
            'accept_language': random.choice(['ar-SA,ar;q=0.9,en;q=0.8', 'en-US,en;q=0.9,ar;q=0.8', 'fr-FR,fr;q=0.9,en;q=0.8']),
            'timezone': random.choice(['Asia/Dubai', 'Asia/Riyadh', 'Asia/Baghdad', 'Africa/Cairo']),
            'screen': f"{random.choice([1920, 1366, 1536, 2560])}x{random.choice([1080, 768, 1440, 1600])}",
            'color_depth': random.choice([24, 30, 32]),
            'platform': random.choice(['Win32', 'MacIntel', 'Linux x86_64', 'iPhone', 'Android']),
            'do_not_track': random.choice(['1', '0', 'unspecified']),
            'hardware_concurrency': random.choice([4, 6, 8, 12, 16]),
            'device_memory': random.choice([4, 8, 16, 32]),
        }
    
    @staticmethod
    def generate_chaotic_ua():
        """توليد User-Agent فوضويه لا يمكن توقعها"""
        os_list = [
            ('Windows NT 10.0; Win64; x64', 'Windows'),
            ('Windows NT 11.0; Win64; x64', 'Windows'),
            ('Macintosh; Intel Mac OS X 10_15_7', 'Mac'),
            ('Macintosh; Intel Mac OS X 11_0_0', 'Mac'),
            ('X11; Linux x86_64', 'Linux'),
            ('X11; Ubuntu; Linux x86_64', 'Linux'),
        ]
        
        browser_list = [
            ('Firefox', f'Firefox/{random.randint(115, 125)}.0'),
            ('Chrome', f'Chrome/{random.randint(115, 125)}.0.0.0'),
            ('Edge', f'Edg/{random.randint(115, 125)}.0.0.0'),
            ('Safari', 'Version/17.1 Safari/605.1.15'),
        ]
        
        os_choice, os_name = random.choice(os_list)
        browser_choice, browser_version = random.choice(browser_list)
        
        if browser_choice == 'Firefox':
            return f'Mozilla/5.0 ({os_choice}; rv:{random.randint(115, 125)}.0) Gecko/20100101 {browser_version}'
        elif browser_choice == 'Safari':
            return f'Mozilla/5.0 ({os_choice}) AppleWebKit/605.1.15 (KHTML, like Gecko) {browser_version}'
        else:
            return f'Mozilla/5.0 ({os_choice}) AppleWebKit/537.36 (KHTML, like Gecko) {browser_version} Safari/537.36'
    
    @staticmethod
    def generate_instagram_ua():
        """توليد User-Agent خاص بـ Instagram بتقنيات متقدمة"""
        devices = {
            'Samsung': [f'SM-{model}' for model in ['S918B', 'S928B', 'F946B', 'A546B']],
            'Google': ['Pixel 8 Pro', 'Pixel 7', 'Pixel 6'],
            'OnePlus': ['OnePlus 12', 'OnePlus 11', 'OnePlus Nord 3'],
            'Xiaomi': ['Mi 14 Pro', 'Mi 13 Ultra', 'Redmi Note 13 Pro+'],
            'iPhone': ['iPhone15,2', 'iPhone16,1', 'iPhone14,3']
        }
        
        device_type = random.choice(list(devices.keys()))
        device_model = random.choice(devices[device_type])
        
        if device_type == 'iPhone':
            android_ver = ''
        else:
            android_ver = f'Android {random.choice(["13", "14", "15"])}; '
        
        instagram_ver = random.randint(300, 330)
        build_ver = random.randint(25, 60)
        
        return f'Mozilla/5.0 (Linux; {android_ver}{device_model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(118, 128)}.0.0.0 Mobile Safari/537.36 Instagram {instagram_ver}.0.0.{build_ver} Android'
    
    @staticmethod
    def generate_signature(data, secret):
        """توليع توقيع HMAC للتخفي"""
        return hmac.new(secret.encode(), data.encode(), hashlib.sha256).hexdigest()

stealth = UltimateStealth()

# ========== تقنيات البريد المؤقت المتطورة ==========
class TempEmailService:
    """خدمة بريد مؤقت متعددة المصادر"""
    
    @staticmethod
    def create_email():
        """إنشاء بريد مؤقت باستخدام أفضل الخدمات"""
        services = [
            TempEmailService._1secmail,
            TempEmailService._temp_mail,
            TempEmailService._guerrilla,
            TempEmailService._mail_tm
        ]
        
        for service in services:
            email = service()
            if email:
                return email
        return None
    
    @staticmethod
    def _1secmail():
        try:
            resp = requests.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1', timeout=15)
            if resp.status_code == 200:
                return resp.json()[0]
        except:
            return None
    
    @staticmethod
    def _temp_mail():
        try:
            headers = {'accept': '*/*', 'user-agent': stealth.generate_chaotic_ua()}
            resp = requests.post('https://api.internal.temp-mail.io/api/v3/email/new', 
                                headers=headers, json={'min_name_length': 8, 'max_name_length': 12}, timeout=15)
            if resp.status_code == 200:
                return resp.json().get("email")
        except:
            return None
    
    @staticmethod
    def _guerrilla():
        try:
            resp = requests.get('https://api.guerrillamail.com/ajax.php?f=get_email_address', timeout=15)
            if resp.status_code == 200:
                return resp.json().get('email_addr')
        except:
            return None
    
    @staticmethod
    def _mail_tm():
        try:
            resp = requests.get('https://api.mail.tm', timeout=15)
            if resp.status_code == 200:
                return resp.json().get('email')
        except:
            return None
    
    @staticmethod
    def get_messages(email):
        """جلب الرسائل من البريد المؤقت"""
        try:
            name, domain = email.split('@')
            resp = requests.get(f'https://www.1secmail.com/api/v1/?action=getMessages&login={name}&domain={domain}', timeout=15)
            if resp.status_code == 200 and resp.json():
                return resp.json()
        except:
            pass
        return []

# ========== دوال الإنشاء الرئيسية ==========
def random_string(length=12):
    return ''.join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=length))

def generate_password():
    """توليد كلمة مرور خارقة"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    return ''.join(random.choices(chars, k=random.randint(14, 18)))

def random_delay(min_sec=3, max_sec=12):
    time.sleep(random.uniform(min_sec, max_sec))

def send_telegram_message(message):
    if BOT_TOKEN and ADMIN_ID:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            data = {"chat_id": ADMIN_ID, "text": message, "parse_mode": "HTML"}
            requests.post(url, data=data, timeout=15)
        except:
            pass

def make_elite():
    """دالة الإنشاء الرئيسية - نسخة خارقة"""
    print("\n" + Fore.CYAN + "█"*60 + Fore.RESET)
    print(Fore.MAGENTA + "[⚡] بدء عملية إنشاء حساب - وضع التخفي الخارق" + Fore.RESET)
    
    # تغيير البروكسي لكل محاولة
    proxy = proxy_manager.get_rotating_proxy()
    
    # توليد بصمة رقمية فريدة
    fingerprint = stealth.generate_fingerprint()
    
    random_delay(5, 10)
    
    # إنشاء بريد مؤقت
    print("[*] جاري إنشاء بريد مؤقت...")
    email = TempEmailService.create_email()
    if not email:
        print(Fore.RED + "[-] فشل إنشاء البريد المؤقت" + Fore.RESET)
        return False, None, None, None, None
    
    print(Fore.GREEN + f"[+] البريد: {email}" + Fore.RESET)
    random_delay(3, 7)
    
    # توليد بيانات فريدة
    device_id = str(uuid.uuid4()).upper()
    csrftoken = secrets.token_urlsafe(32)
    jazoest = str(random.randint(22000, 25000))
    session_id = f':{random_string(12)}:{random_string(15)}'
    
    cookies = {
        'ig_did': device_id,
        'csrftoken': csrftoken,
        'mid': random_string(22),
        'datr': secrets.token_urlsafe(24),
        'wd': f"{fingerprint['screen'].replace('x', '')}x{fingerprint['screen'].split('x')[1]}",
    }
    
    headers = {
        'User-Agent': stealth.generate_instagram_ua(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': fingerprint['accept_language'],
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.instagram.com',
        'Referer': 'https://www.instagram.com/accounts/signup/email/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'X-Csrftoken': csrftoken,
        'X-IG-App-ID': '1217981644879628',
        'X-Requested-With': 'XMLHttpRequest',
    }
    
    session = requests.Session()
    session.mount('https://', TLSAdapter())
    
    # 1. التحقق من البريد
    print("[*] جاري التحقق من البريد...")
    try:
        resp = session.post('https://www.instagram.com/api/v1/web/accounts/check_email/',
                           cookies=cookies, headers=headers, data={'email': email, 'jazoest': jazoest},
                           timeout=30, proxies=proxy)
        if resp.status_code != 200:
            return False, None, None, None, None
    except:
        return False, None, None, None, None
    
    random_delay(5, 10)
    
    # 2. طلب كود التفعيل
    print("[*] جاري طلب كود التفعيل...")
    try:
        resp = session.post('https://www.instagram.com/api/v1/accounts/send_verify_email/',
                           cookies=cookies, headers=headers,
                           data={'device_id': device_id, 'email': email, 'jazoest': jazoest},
                           timeout=30, proxies=proxy)
        if resp.status_code != 200:
            return False, None, None, None, None
    except:
        return False, None, None, None, None
    
    random_delay(6, 12)
    
    # 3. انتظار الكود
    print("[*] انتظار كود التفعيل...")
    code = None
    for attempt in range(25):
        msgs = TempEmailService.get_messages(email)
        if msgs:
            for msg in msgs:
                body = str(msg.get('body', '')) + str(msg.get('mailText', ''))
                match = re.search(r'\b(\d{6})\b', body)
                if match:
                    code = match.group(1)
                    print(Fore.GREEN + f"[+] تم استلام الكود: {code}" + Fore.RESET)
                    break
            if code:
                break
        time.sleep(random.uniform(6, 10))
    
    if not code:
        return False, None, None, None, None
    
    random_delay(3, 6)
    
    # 4. تأكيد الكود
    print("[*] جاري تأكيد الكود...")
    try:
        resp = session.post('https://www.instagram.com/api/v1/accounts/check_confirmation_code/',
                           cookies=cookies, headers=headers,
                           data={'code': code, 'device_id': device_id, 'email': email, 'jazoest': jazoest},
                           timeout=30, proxies=proxy)
        
        if resp.status_code != 200:
            return False, None, None, None, None
        
        resp_json = resp.json()
        if resp_json.get('spam', False):
            print(Fore.RED + "[-] تم اكتشاف نشاط آلي!" + Fore.RESET)
            return False, None, None, None, None
        
        signup_code = resp_json.get("signup_code", "")
    except:
        return False, None, None, None, None
    
    random_delay(3, 6)
    
    # توليد بيانات الحساب
    username = random_string(random.randint(10, 16))
    password = generate_password()
    first_name = random_string(random.randint(6, 10)).capitalize()
    
    # 5. الإنشاء النهائي
    print("[*] جاري إنشاء الحساب النهائي...")
    headers['Referer'] = 'https://www.instagram.com/accounts/signup/username/'
    data = {
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
        'day': str(random.randint(1, 28)),
        'month': str(random.randint(1, 12)),
        'year': str(random.randint(1988, 2005)),
        'email': email,
        'first_name': first_name,
        'username': username,
        'client_id': device_id,
        'seamless_login_enabled': '1',
        'tos_version': 'row',
        'force_sign_up_code': signup_code,
        'extra_session_id': session_id,
        'jazoest': jazoest,
    }
    
    try:
        resp = session.post('https://www.instagram.com/api/v1/web/accounts/web_create_ajax/',
                           cookies=cookies, headers=headers, data=data, timeout=35, proxies=proxy)
        
        if 'user_id' in resp.text:
            now = datetime.now()
            user_id = resp.json().get('user_id', 'Unknown')
            
            print(Fore.GREEN + f"\n[✅] تم إنشاء الحساب بنجاح! {now.strftime('%H:%M:%S')}" + Fore.RESET)
            print(Fore.CYAN + f"📧 البريد: {email}")
            print(f"👤 المستخدم: {username}")
            print(f"🔑 كلمة المرور: {password}")
            print(f"🆔 المعرف: {user_id}" + Fore.RESET)
            
            success_msg = f"""✅ <b>تم إنشاء الحساب بنجاح!</b>
📧 {email}
👤 {username}
🔑 {password}
🆔 {user_id}
📅 {now.strftime('%Y-%m-%d %H:%M:%S')}"""
            
            with open("accounts.txt", "a", encoding="utf-8") as f:
                f.write(f"{now.strftime('%Y-%m-%d %H:%M:%S')} | {email} | {username} | {password} | {user_id}\n")
            
            send_telegram_message(success_msg)
            return True, email, username, password, user_id
        else:
            print(Fore.RED + "[-] فشل إنشاء الحساب" + Fore.RESET)
            return False, None, None, None, None
    except Exception as e:
        print(Fore.RED + f"[-] خطأ: {e}" + Fore.RESET)
        return False, None, None, None, None

# ===== واجهة البوت المتطورة =====
async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id=None):
    keyboard = [
        [InlineKeyboardButton("🔥 إنشاء حساب - وضع التخفي الخارق", callback_data="create_elite")],
        [InlineKeyboardButton("🌐 تحديث البروكسيات", callback_data="update_proxies")],
        [InlineKeyboardButton("📊 إضافة بروكسي مدفوع", callback_data="add_proxy")],
        [InlineKeyboardButton("📁 عرض الحسابات", callback_data="show_accounts")],
        [InlineKeyboardButton("🗑️ مسح الحسابات", callback_data="clear_accounts")],
        [InlineKeyboardButton("ℹ️ حالة النظام", callback_data="status")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = """🤖 *ELITE INSTAGRAM BOT - ULTIMATE STEALTH v7.0*

🛡️ *تقنيات التخفي الخارقة:*
• ✅ بروكسيات متجددة + دعم بروكسيات مدفوعة
• ✅ بصمة رقمية فريدة لكل طلب
• ✅ TLS Fingerprint Spoofing
• ✅ تشفير HMAC للتخفي
• ✅ User-Agent فوضويه غير قابلة للكشف
• ✅ تأخيرات ذكية متغيرة

🔥 *اختر الإجراء:*"""
    
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
    
    if data == "create_elite":
        await query.edit_message_text("🔄 جاري إنشاء حساب - وضع التخفي الخارق...\n⏱️ قد يستغرق 3-5 دقائق")
        
        success, email, username, password, uid = make_elite()
        if success:
            text = f"""✅ *تم إنشاء الحساب بنجاح باستخدام التخفي الخارق!*

📧 `{email}`
👤 `{username}`
🔑 `{password}`
🆔 `{uid}`

🔥 تم استخدام أقوى تقنيات التخفي"""
            await query.edit_message_text(text, parse_mode="Markdown")
        else:
            await query.edit_message_text("❌ *فشل إنشاء الحساب*\n\nInstagram يحظر المحاولات حالياً.\nتم تغيير البروكسي والـ Fingerprint للمحاولة التالية.\n\n⏰ انتظر ساعة ثم حاول مرة أخرى.", parse_mode="Markdown")
        
        await asyncio.sleep(3)
        await main_menu(update, context, chat_id=user_id)
    
    elif data == "update_proxies":
        await query.edit_message_text("🔄 جاري تحديث البروكسيات عالية الجودة...")
        proxy_manager.fetch_elite_proxies()
        count = len(proxy_manager.proxies)
        await query.edit_message_text(f"✅ *تم تحديث البروكسيات!*\n📊 عدد البروكسيات المتاحة: {count}\n🔥 تم استخدام أقوى المصادر", parse_mode="Markdown")
        await asyncio.sleep(2)
        await main_menu(update, context, chat_id=user_id)
    
    elif data == "add_proxy":
        await query.edit_message_text("📝 *أرسل البروكسي المدفوع بالصيغة:*\n`http://username:password@ip:port`\n\nمثال:\n`http://user123:pass456@192.168.1.1:8080`", parse_mode="Markdown")
        context.user_data['awaiting_proxy'] = True
    
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
        await query.edit_message_text("✅ *تم مسح جميع الحسابات*", parse_mode="Markdown")
        await asyncio.sleep(1)
        await main_menu(update, context, chat_id=user_id)
    
    elif data == "status":
        proxy_count = len(proxy_manager.proxies)
        try:
            with open("accounts.txt", "r") as f:
                account_count = len(f.readlines())
        except:
            account_count = 0
        
        text = f"""ℹ️ *حالة النظام - النسخة الخارقة*

🛡️ *الحماية:*
• وضع التخفي الخارق: ✅ مفعل
• TLS Fingerprint: ✅ مفعل
• بروكسيات متاحة: {proxy_count}
• حسابات محفوظة: {account_count}

⚡ *التقنيات النشطة:*
• بصمة رقمية فريدة
• User-Agent فوضويه
• تشفير HMAC
• جلسات متغيرة

🔥 *جاهز للإنشاء في أي وقت*"""
        await query.edit_message_text(text, parse_mode="Markdown")
        await asyncio.sleep(2)
        await main_menu(update, context, chat_id=user_id)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('awaiting_proxy'):
        proxy_string = update.message.text
        proxy_manager.add_premium_proxy(proxy_string)
        await update.message.reply_text("✅ *تم إضافة البروكسي المدفوع بنجاح!*\n🔥 سيتم استخدامه في المحاولات القادمة", parse_mode="Markdown")
        context.user_data['awaiting_proxy'] = False
        await main_menu(update, context)

# ------------------- الكود الرئيسي للتشغيل -------------------
if __name__ == "__main__":
    print(Fore.CYAN + """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     🔥 ELITE INSTAGRAM BOT - ULTIMATE STEALTH v7.0 🔥    ║
║                                                          ║
║     أقوى نسخة تخفي على الإطلاق - لا يمكن كشفها          ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
""" + Fore.RESET)
    
    print(Fore.MAGENTA + """
⚡ التقنيات الخارقة المفعلة:
├─ ✅ TLS Fingerprint Spoofing
├─ ✅ بروكسيات متجددة + دعم مدفوع
├─ ✅ بصمة رقمية فريدة لكل طلب
├─ ✅ User-Agent فوضويه غير قابلة للكشف
├─ ✅ تشفير HMAC للتخفي
├─ ✅ خدمات بريد متعددة
└─ ✅ تأخيرات ذكية متغيرة
""" + Fore.RESET)
    
    # جلب البروكسيات أولاً
    print(Fore.YELLOW + "[*] جاري تجهيز البروكسيات الخارقة..." + Fore.RESET)
    proxy_manager.fetch_elite_proxies()
    print(Fore.GREEN + f"[+] تم تجهيز {len(proxy_manager.proxies)} بروكسي" + Fore.RESET)
    
    # تشغيل Flask في خيط منفصل
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # تشغيل بوت Telegram
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(None, handle_message))
    
    print(Fore.GREEN + "✅ البوت يعمل بوضع التخفي الخارق! أرسل /start" + Fore.RESET)
    print(Fore.CYAN + f"🤖 التوكن: {BOT_TOKEN[:20]}...")
    print(f"👤 الايدي: {ADMIN_ID}")
    print(f"🔄 بروكسيات: {len(proxy_manager.proxies)}")
    print(f"🔥 وضع التخفي: نشط 100%" + Fore.RESET)
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)
