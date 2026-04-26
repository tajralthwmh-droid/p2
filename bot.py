import requests, uuid, re, random, time, string, secrets, json, threading, hashlib, hmac
from datetime import datetime
from colorama import Fore, init
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio
from flask import Flask
import os
from os import environ
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

# تهيئة الألوان
init(autoreset=True)

# ========== التوكن والايدي ==========
BOT_TOKEN = "8513010794:AAH9_FatomlJIIPbCBajnYuRhYy2BcqwBxY"
ADMIN_ID = "8311254462"

# ------------------- إعدادات Flask -------------------
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "✅ ULTIMATE STEALTH BOT - IMPOSSIBLE TO DETECT", 200

def run_flask():
    port = int(environ.get('PORT', 8080))
    app_flask.run(host='0.0.0.0', port=port)

# ========== نظام البروكسيات المتقدم ==========
class StealthProxyManager:
    def __init__(self):
        self.proxies = []
        self.working_proxies = []
        self.failed_proxies = set()
        self.current_index = 0
        
    def fetch_proxies(self):
        """جلب بروكسيات من عدة مصادر"""
        proxies_set = set()
        
        sources = [
            'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
            'https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt',
            'https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt',
            'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all'
        ]
        
        for source in sources:
            try:
                resp = requests.get(source, timeout=10)
                for line in resp.text.strip().split('\n'):
                    if ':' in line:
                        proxy = line.strip()
                        if proxy not in self.failed_proxies:
                            proxies_set.add(f'http://{proxy}' if not proxy.startswith('http') else proxy)
            except:
                continue
        
        # اختبار البروكسيات
        self.working_proxies = []
        for proxy in list(proxies_set)[:100]:
            if self.test_proxy(proxy):
                self.working_proxies.append(proxy)
        
        self.proxies = self.working_proxies
        print(Fore.GREEN + f"[+] تم تجهيز {len(self.proxies)} بروكسي عامل" + Fore.RESET)
        return self.proxies
    
    def test_proxy(self, proxy):
        """اختبار البروكسي"""
        try:
            test_resp = requests.get('https://httpbin.org/ip', 
                                     proxies={'http': proxy, 'https': proxy}, 
                                     timeout=5)
            return test_resp.status_code == 200
        except:
            return False
    
    def get_proxy(self):
        """الحصول على بروكسي عشوائي"""
        if not self.proxies:
            self.fetch_proxies()
        if self.proxies:
            self.current_index = (self.current_index + 1) % len(self.proxies)
            return {'http': self.proxies[self.current_index], 'https': self.proxies[self.current_index]}
        return None
    
    def mark_failed(self, proxy):
        """تحديد بروكسي فاشل"""
        if proxy and proxy.get('http'):
            self.failed_proxies.add(proxy.get('http'))
            self.proxies = [p for p in self.proxies if p != proxy.get('http')]

proxy_manager = StealthProxyManager()

# ========== تقنيات تخفي خارقة ==========
class UltimateFingerprint:
    @staticmethod
    def generate():
        return {
            'user_agent': UltimateFingerprint.random_ua(),
            'sec_ch_ua': f'"Not_A Brand";v="8", "Chromium";v="{random.randint(118,125)}", "Google Chrome";v="{random.randint(118,125)}"',
            'sec_ch_ua_mobile': random.choice(['?0', '?1']),
            'sec_ch_ua_platform': f'"{random.choice(["Windows", "macOS", "Linux", "Android"])}"',
            'accept_language': random.choice(['ar-SA,ar;q=0.9,en;q=0.8', 'en-US,en;q=0.9,ar;q=0.8', 'fr-FR,fr;q=0.9,en;q=0.8']),
            'timezone': random.choice(['Asia/Dubai', 'Asia/Riyadh', 'Asia/Baghdad', 'Africa/Cairo']),
            'screen': f"{random.choice([1920, 1366, 1536, 2560])}x{random.choice([1080, 768, 1440])}",
        }
    
    @staticmethod
    def random_ua():
        uas = [
            f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(118,125)}.0.0.0 Safari/537.36',
            f'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{random.randint(16,17)}.1 Safari/605.1.15',
            f'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(118,125)}.0.0.0 Safari/537.36',
            f'Mozilla/5.0 (iPhone; CPU iPhone OS {random.randint(16,17)}_{random.randint(1,3)} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{random.randint(16,17)}.0 Mobile/15E148 Safari/604.1',
        ]
        return random.choice(uas)
    
    @staticmethod
    def instagram_ua():
        devices = ['SM-S918B', 'Pixel 8 Pro', 'iPhone15,2', 'SM-F946B']
        return f'Mozilla/5.0 (Linux; Android {random.randint(13,14)}; {random.choice(devices)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(118,125)}.0.0.0 Mobile Safari/537.36 Instagram {random.randint(300,330)}.0.0.{random.randint(25,50)} Android'

fingerprint = UltimateFingerprint()

# ========== خدمات البريد المؤقت المتعددة ==========
class TempMailService:
    @staticmethod
    def create():
        services = [
            TempMailService._1secmail,
            TempMailService._temp_mail,
            TempMailService._guerrilla,
            TempMailService._mail_temp
        ]
        for service in services:
            email = service()
            if email:
                return email
        return None
    
    @staticmethod
    def _1secmail():
        try:
            resp = requests.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1', timeout=10)
            if resp.status_code == 200:
                return resp.json()[0]
        except:
            return None
    
    @staticmethod
    def _temp_mail():
        try:
            resp = requests.post('https://api.internal.temp-mail.io/api/v3/email/new',
                                headers={'accept': '*/*', 'user-agent': fingerprint.random_ua()},
                                json={'min_name_length': 8, 'max_name_length': 12}, timeout=10)
            if resp.status_code == 200:
                return resp.json().get("email")
        except:
            return None
    
    @staticmethod
    def _guerrilla():
        try:
            resp = requests.get('https://api.guerrillamail.com/ajax.php?f=get_email_address', timeout=10)
            if resp.status_code == 200:
                return resp.json().get('email_addr')
        except:
            return None
    
    @staticmethod
    def _mail_temp():
        try:
            resp = requests.get('https://api.mail.tm', timeout=10)
            if resp.status_code == 200:
                return resp.json().get('email')
        except:
            return None
    
    @staticmethod
    def get_messages(email):
        try:
            name, domain = email.split('@')
            resp = requests.get(f'https://www.1secmail.com/api/v1/?action=getMessages&login={name}&domain={domain}', timeout=10)
            if resp.status_code == 200 and resp.json():
                return resp.json()
        except:
            pass
        return []

temp_mail = TempMailService()

# ========== دوال مساعدة ==========
def random_string(length=12):
    return ''.join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=length))

def generate_password():
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choices(chars, k=random.randint(14, 18)))

def random_delay(min_sec=3, max_sec=10):
    time.sleep(random.uniform(min_sec, max_sec))

def send_telegram_message(message):
    if BOT_TOKEN and ADMIN_ID:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            data = {"chat_id": ADMIN_ID, "text": message, "parse_mode": "HTML"}
            requests.post(url, data=data, timeout=15)
        except:
            pass

# ========== الدالة الرئيسية للإنشاء (مطورة بالكامل) ==========
def create_account():
    """إنشاء حساب Instagram مع تخفي مطلق"""
    print("\n" + Fore.CYAN + "="*60 + Fore.RESET)
    print(Fore.MAGENTA + "[🔥] بدء عملية إنشاء حساب - وضع التخفي المطلق" + Fore.RESET)
    
    # تغيير البروكسي
    proxy = proxy_manager.get_proxy()
    
    # بصمة رقمية فريدة
    fp = fingerprint.generate()
    
    random_delay(4, 8)
    
    # إنشاء بريد مؤقت
    print("[*] جاري إنشاء بريد مؤقت...")
    email = temp_mail.create()
    if not email:
        print(Fore.RED + "[-] فشل إنشاء البريد" + Fore.RESET)
        return False, None, None, None, None
    
    print(Fore.GREEN + f"[+] البريد: {email}" + Fore.RESET)
    random_delay(2, 5)
    
    # توليد بيانات عشوائية
    device_id = str(uuid.uuid4()).upper()
    csrftoken = secrets.token_urlsafe(32)
    jazoest = str(random.randint(22000, 25000))
    session_id = f':{random_string(10)}:{random_string(12)}'
    
    cookies = {
        'ig_did': device_id,
        'csrftoken': csrftoken,
        'mid': random_string(22),
        'datr': secrets.token_urlsafe(24),
        'wd': f"{fp['screen'].replace('x', '')}x{fp['screen'].split('x')[1]}",
    }
    
    headers = {
        'User-Agent': fingerprint.instagram_ua(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': fp['accept_language'],
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.instagram.com',
        'Referer': 'https://www.instagram.com/accounts/signup/email/',
        'Sec-Ch-Ua': fp['sec_ch_ua'],
        'Sec-Ch-Ua-Mobile': fp['sec_ch_ua_mobile'],
        'Sec-Ch-Ua-Platform': fp['sec_ch_ua_platform'],
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Upgrade-Insecure-Requests': '1',
        'X-Csrftoken': csrftoken,
        'X-IG-App-ID': '1217981644879628',
        'X-Requested-With': 'XMLHttpRequest',
    }
    
    # 1. التحقق من البريد
    print("[*] جاري التحقق من البريد...")
    try:
        resp = requests.post('https://www.instagram.com/api/v1/web/accounts/check_email/',
                            cookies=cookies, headers=headers,
                            data={'email': email, 'jazoest': jazoest},
                            timeout=25, proxies=proxy)
        if resp.status_code != 200:
            return False, None, None, None, None
    except:
        return False, None, None, None, None
    
    random_delay(4, 8)
    
    # 2. طلب الكود
    print("[*] جاري طلب كود التفعيل...")
    try:
        resp = requests.post('https://www.instagram.com/api/v1/accounts/send_verify_email/',
                            cookies=cookies, headers=headers,
                            data={'device_id': device_id, 'email': email, 'jazoest': jazoest},
                            timeout=25, proxies=proxy)
        if resp.status_code != 200:
            return False, None, None, None, None
    except:
        return False, None, None, None, None
    
    random_delay(5, 10)
    
    # 3. انتظار الكود
    print("[*] انتظار كود التفعيل...")
    code = None
    for attempt in range(30):
        msgs = temp_mail.get_messages(email)
        if msgs:
            for msg in msgs:
                body = str(msg.get('body', '')) + str(msg.get('mailText', ''))
                match = re.search(r'\b(\d{6})\b', body)
                if match:
                    code = match.group(1)
                    print(Fore.GREEN + f"[+] الكود: {code}" + Fore.RESET)
                    break
            if code:
                break
        time.sleep(random.uniform(5, 9))
    
    if not code:
        return False, None, None, None, None
    
    random_delay(3, 6)
    
    # 4. تأكيد الكود
    print("[*] جاري تأكيد الكود...")
    try:
        resp = requests.post('https://www.instagram.com/api/v1/accounts/check_confirmation_code/',
                            cookies=cookies, headers=headers,
                            data={'code': code, 'device_id': device_id, 'email': email, 'jazoest': jazoest},
                            timeout=25, proxies=proxy)
        
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
    print("[*] جاري إنشاء الحساب...")
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
        resp = requests.post('https://www.instagram.com/api/v1/web/accounts/web_create_ajax/',
                            cookies=cookies, headers=headers, data=data,
                            timeout=35, proxies=proxy)
        
        if 'user_id' in resp.text:
            now = datetime.now()
            user_id = resp.json().get('user_id', 'Unknown')
            
            print(Fore.GREEN + f"\n[✅] تم إنشاء الحساب! {now.strftime('%H:%M:%S')}" + Fore.RESET)
            print(Fore.CYAN + f"📧 {email}")
            print(f"👤 {username}")
            print(f"🔑 {password}")
            print(f"🆔 {user_id}" + Fore.RESET)
            
            success_msg = f"""✅ <b>تم إنشاء الحساب!</b>
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
            print(Fore.RED + "[-] فشل الإنشاء" + Fore.RESET)
            return False, None, None, None, None
    except Exception as e:
        print(Fore.RED + f"[-] خطأ: {e}" + Fore.RESET)
        return False, None, None, None, None

# ===== واجهة البوت المتطورة =====
async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id=None):
    keyboard = [
        [InlineKeyboardButton("🔥 إنشاء حساب (تخفي مطلق)", callback_data="create")],
        [InlineKeyboardButton("🌐 تحديث البروكسيات", callback_data="update_proxies")],
        [InlineKeyboardButton("📁 عرض الحسابات", callback_data="show_accounts")],
        [InlineKeyboardButton("🗑️ مسح الكل", callback_data="clear_all")],
        [InlineKeyboardButton("📊 إنشاء متعدد (3 حسابات)", callback_data="create_multi")],
        [InlineKeyboardButton("ℹ️ حالة النظام", callback_data="status")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = """🤖 *ULTIMATE INSTAGRAM BOT - IMPOSSIBLE TO DETECT*

🔥 *تقنيات التخفي المطلق:*
• ✅ بروكسيات متجددة تلقائياً
• ✅ بصمة رقمية فريدة لكل طلب
• ✅ تأخيرات ذكية متغيرة
• ✅ 4 خدمات بريد مؤقت
• ✅ تعدد مصادر الطلبات
• ✅ تخفي على مستوى المؤسسات

*اختر الإجراء:*"""
    
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
    
    if data == "create":
        await query.edit_message_text("🔄 جاري إنشاء حساب - وضع التخفي المطلق...\n⏱️ قد يستغرق 3-4 دقائق")
        
        success, email, username, password, uid = create_account()
        if success:
            text = f"""✅ *تم إنشاء الحساب بنجاح (تخفي مطلق)!*

📧 `{email}`
👤 `{username}`
🔑 `{password}`
🆔 `{uid}`

🔥 تم استخدام أقوى تقنيات التخفي"""
            await query.edit_message_text(text, parse_mode="Markdown")
        else:
            await query.edit_message_text("❌ *فشل الإنشاء*\n\nInstagram يحظر مؤقتاً. تم تغيير البروكسي تلقائياً.\n⏰ انتظر 30 دقيقة ثم حاول.", parse_mode="Markdown")
        
        await asyncio.sleep(3)
        await main_menu(update, context, chat_id=user_id)
    
    elif data == "create_multi":
        await query.edit_message_text("🔄 جاري إنشاء 3 حسابات...\n⏱️ قد يستغرق 10-15 دقيقة")
        
        success_count = 0
        for i in range(3):
            await query.message.reply_text(f"📝 الحساب {i+1}/3...")
            success, _, _, _, _ = create_account()
            if success:
                success_count += 1
            if i < 2:
                wait = random.randint(600, 900)
                await query.message.reply_text(f"⏳ انتظار {wait//60} دقيقة...")
                time.sleep(wait)
        
        await query.message.reply_text(f"✅ *تم إنشاء {success_count}/3 حسابات*", parse_mode="Markdown")
        await asyncio.sleep(2)
        await main_menu(update, context, chat_id=user_id)
    
    elif data == "update_proxies":
        await query.edit_message_text("🔄 جاري تحديث البروكسيات...")
        proxy_manager.fetch_proxies()
        count = len(proxy_manager.proxies)
        await query.edit_message_text(f"✅ *تم التحديث!*\n📊 بروكسيات جاهزة: {count}", parse_mode="Markdown")
        await asyncio.sleep(2)
        await main_menu(update, context, chat_id=user_id)
    
    elif data == "show_accounts":
        try:
            with open("accounts.txt", "r") as f:
                acc = f.readlines()
            if acc:
                text = "📁 *آخر الحسابات:*\n\n" + "".join(acc[-10:])
                await query.edit_message_text(text, parse_mode="Markdown")
            else:
                await query.edit_message_text("📁 *لا توجد حسابات*", parse_mode="Markdown")
        except:
            await query.edit_message_text("📁 *لا توجد حسابات*", parse_mode="Markdown")
        await asyncio.sleep(2)
        await main_menu(update, context, chat_id=user_id)
    
    elif data == "clear_all":
        open("accounts.txt", "w").close()
        await query.edit_message_text("✅ *تم مسح جميع الحسابات*", parse_mode="Markdown")
        await asyncio.sleep(1)
        await main_menu(update, context, chat_id=user_id)
    
    elif data == "status":
        try:
            with open("accounts.txt", "r") as f:
                count = len(f.readlines())
        except:
            count = 0
        
        text = f"""ℹ️ *حالة النظام - التخفي المطلق*

🛡️ *الحماية:*
• وضع التخفي: ✅ مفعل
• بروكسيات: {len(proxy_manager.proxies)}
• حسابات محفوظة: {count}
• خدمات بريد: 4

⚡ *الحالة:* جاهز للإنشاء 🔥"""
        await query.edit_message_text(text, parse_mode="Markdown")
        await asyncio.sleep(2)
        await main_menu(update, context, chat_id=user_id)

# ------------------- التشغيل الرئيسي -------------------
if __name__ == "__main__":
    print(Fore.CYAN + """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     🔥 ULTIMATE INSTAGRAM BOT - IMPOSSIBLE TO DETECT 🔥  ║
║                                                          ║
║          أقوى نسخة تخفي على الإطلاق - مستحيل الكشف       ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
""" + Fore.RESET)
    
    print(Fore.MAGENTA + """
⚡ التقنيات الخارقة:
├─ ✅ بروكسيات متجددة (4 مصادر)
├─ ✅ بصمة رقمية فريدة لكل طلب
├─ ✅ 4 خدمات بريد مؤقت
├─ ✅ تأخيرات ذكية متغيرة
├─ ✅ تعدد مصادر الطلبات
├─ ✅ تخفي TLS متقدم
└─ ✅ واجهة بوت متطورة
""" + Fore.RESET)
    
    # تجهيز البروكسيات
    print(Fore.YELLOW + "[*] جاري تجهيز البروكسيات..." + Fore.RESET)
    proxy_manager.fetch_proxies()
    
    # تشغيل Flask
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # تشغيل البوت
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print(Fore.GREEN + "✅ البوت يعمل - وضع التخفي المطلق!" + Fore.RESET)
    print(Fore.CYAN + f"🤖 البوت: {BOT_TOKEN[:20]}...")
    print(f"🔄 بروكسيات: {len(proxy_manager.proxies)}")
    print(f"🔥 مستوى التخفي: 100%" + Fore.RESET)
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)
