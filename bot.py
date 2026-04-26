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
    return "✅ البوت يعمل بنجاح!", 200

def run_flask():
    port = int(environ.get('PORT', 8080))
    app_flask.run(host='0.0.0.0', port=port)

# ------------------- الكود الأصلي للبوت -------------------
print(Fore.CYAN + """
╔══════════════════════════════════════════════════╗
║     Instagram Account Creator Bot                ║
║         نسخة التخفي المتطورة v5.0               ║
║              مثبت عليها التوكن ✅                 ║
╚══════════════════════════════════════════════════╝
""" + Fore.RESET)

# ========== تقنيات تخفي متطورة ==========
try:
    from user_agent import generate_user_agent
    USE_ADVANCED_UA = True
except ImportError:
    USE_ADVANCED_UA = False

def get_stealth_user_agent():
    if USE_ADVANCED_UA:
        return generate_user_agent()
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
        'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
    ]
    return random.choice(user_agents)

def generate_instagram_ua():
    models = ['SM-S918B', 'Pixel 8 Pro', 'iPhone15,2', 'SM-F946B']
    return f'Mozilla/5.0 (Linux; Android {random.randint(13,14)}; {random.choice(models)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(118,124)}.0.0.0 Mobile Safari/537.36 Instagram {random.randint(290,310)}.0.0.{random.randint(25,40)} Android'

def generate_csrf_token():
    return secrets.token_urlsafe(32)

def random_device_id():
    return str(uuid.uuid4()).upper()

def random_mid():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=22))

def random_jazoest():
    return str(random.randint(22000, 24500))

def generate_password():
    letters = string.ascii_letters
    digits = string.digits
    symbols = "!@#$%^&*"
    password = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice(symbols),
    ]
    password += random.choices(letters + digits + symbols, k=random.randint(10, 14))
    random.shuffle(password)
    return ''.join(password)

def send_telegram_message(message):
    if BOT_TOKEN and ADMIN_ID:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            data = {"chat_id": ADMIN_ID, "text": message, "parse_mode": "HTML"}
            requests.post(url, data=data, timeout=15)
        except:
            pass

# ========== دوال البريد المؤقت ==========
def create_temp_email():
    try:
        resp = requests.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1', timeout=15)
        if resp.status_code == 200:
            return resp.json()[0]
    except:
        pass
    
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
    return None

def get_messages(email_address):
    try:
        name, domain = email_address.split('@')
        resp = requests.get(f'https://www.1secmail.com/api/v1/?action=getMessages&login={name}&domain={domain}', timeout=15)
        if resp.status_code == 200 and resp.json():
            return resp.json()
    except:
        pass
    
    try:
        headers = {'accept': '*/*', 'user-agent': get_stealth_user_agent()}
        resp = requests.get(f'https://api.internal.temp-mail.io/api/v3/email/{email_address}/messages', 
                           headers=headers, timeout=15)
        if resp.status_code == 200 and resp.json():
            return resp.json()
    except:
        pass
    return []

def wait_for_verification_code(email_address, max_wait=180):
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
                
                if any(x in subject for x in ["verify", "code", "instagram", "confirmation"]):
                    matches = re.findall(r'\b(\d{6})\b', body)
                    if matches:
                        code = matches[0]
                        print(f"[ + ] تم استلام الكود: {code}")
                        return code
        
        delay = min(5 + (attempts // 3), 10)
        time.sleep(random.uniform(delay, delay + 2))
    
    print("[ - ] لم يتم استلام الكود")
    return ""

def random_string(length=12):
    return ''.join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=length))

def make():
    print("\n[ * ] جاري إنشاء بريد مؤقت...")
    time.sleep(random.uniform(3, 6))
    
    email = create_temp_email()
    if not email:
        print("[ - ] فشل إنشاء البريد المؤقت")
        return False, None, None, None, None
    
    print(f"[ + ] البريد الإلكتروني: {email}")
    time.sleep(random.uniform(2, 5))
    
    device_id = random_device_id()
    mid = random_mid()
    csrftoken = generate_csrf_token()
    jazoest1 = random_jazoest()
    jazoest2 = random_jazoest()
    session_id = f':{random_string(8)}:{random_string(8)}'
    
    cookies = {
        'ig_did': device_id,
        'dpr': str(random.randint(1, 3)),
        'mid': mid,
        'csrftoken': csrftoken,
        'datr': generate_csrf_token()[:20],
        'wd': f'{random.randint(360, 414)}x{random.randint(600, 900)}',
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
    }
    
    print("[ * ] جاري التحقق من البريد...")
    data = {'email': email, 'jazoest': jazoest1}
    
    try:
        response = requests.post('https://www.instagram.com/api/v1/web/accounts/check_email/', 
                                cookies=cookies, headers=headers, data=data, timeout=20)
        if response.status_code != 200:
            print("[ - ] فشل التحقق من البريد")
            return False, None, None, None, None
    except Exception as e:
        print(f"[ - ] خطأ في التحقق: {e}")
        return False, None, None, None, None
    
    time.sleep(random.uniform(3, 7))
    
    print("[ * ] جاري طلب كود التفعيل...")
    data = {'device_id': device_id, 'email': email, 'jazoest': jazoest1}
    
    try:
        response = requests.post('https://www.instagram.com/api/v1/accounts/send_verify_email/', 
                                cookies=cookies, headers=headers, data=data, timeout=20)
        if response.status_code != 200:
            print("[ - ] فشل طلب الكود")
            return False, None, None, None, None
    except Exception as e:
        print(f"[ - ] خطأ في طلب الكود: {e}")
        return False, None, None, None, None
    
    time.sleep(random.uniform(4, 9))
    
    code = wait_for_verification_code(email)
    if not code:
        return False, None, None, None, None
    
    time.sleep(random.uniform(2, 5))
    
    print("[ * ] جاري تأكيد الكود...")
    headers['referer'] = 'https://www.instagram.com/accounts/signup/emailConfirmation/'
    data = {'code': code, 'device_id': device_id, 'email': email, 'jazoest': jazoest1}
    
    try:
        response = requests.post('https://www.instagram.com/api/v1/accounts/check_confirmation_code/', 
                                cookies=cookies, headers=headers, data=data, timeout=20)
        
        if response.status_code != 200:
            print("[ - ] فشل تأكيد الكود")
            return False, None, None, None, None
        
        response_json = response.json()
        
        if response_json.get('spam'):
            print(Fore.RED + f"[ - ] تم اكتشاف نشاط آلي (Spam)" + Fore.RESET)
            print(Fore.YELLOW + f"     السبب: {response_json.get('feedback_message', 'غير معروف')}" + Fore.RESET)
            return False, None, None, None, None
        
        rc = response_json.get("signup_code", "")
        
    except Exception as e:
        print(f"[ - ] خطأ في تأكيد الكود: {e}")
        return False, None, None, None, None
    
    time.sleep(random.uniform(2, 5))
    
    username = random_string(random.randint(10, 15))
    password = generate_password()
    first_name = random_string(random.randint(6, 9)).capitalize()
    day = random.randint(1, 28)
    month = random.randint(1, 12)
    year = random.randint(1988, 2002)
    
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
                     cookies=cookies, headers=headers, data=data, timeout=20)
    except:
        pass
    
    time.sleep(random.uniform(2, 4))
    
    headers['referer'] = 'https://www.instagram.com/accounts/signup/birthday/'
    data = {'day': str(day), 'month': str(month), 'year': str(year), 'jazoest': jazoest2}
    
    try:
        requests.post('https://www.instagram.com/api/v1/web/consent/check_age_eligibility/', 
                     cookies=cookies, headers=headers, data=data, timeout=20)
    except:
        pass
    
    time.sleep(random.uniform(2, 4))
    
    data = {'email': email, 'name': first_name, 'jazoest': jazoest2}
    
    try:
        requests.post('https://www.instagram.com/api/v1/web/accounts/username_suggestions/', 
                     cookies=cookies, headers=headers, data=data, timeout=20)
    except:
        pass
    
    time.sleep(random.uniform(2, 4))
    
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
                                cookies=cookies, headers=headers, data=data, timeout=30)
        
        try:
            response_json = response.json()
        except:
            response_json = {}
        
        if 'user_id' in response.text:
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
            print(Fore.RED + f"\n[ - ] ❌ فشل الإنشاء" + Fore.RESET)
            return False, None, None, None, None
            
    except Exception as e:
        print(Fore.RED + f"[ - ] خطأ: {e}" + Fore.RESET)
        return False, None, None, None, None

# ===== واجهة البوت =====
async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id=None):
    keyboard = [
        [InlineKeyboardButton("📝 إنشاء حساب", callback_data="create_one")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "🤖 *بوت إنشاء حسابات Instagram*\nاختر الإجراء:"
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
        await query.edit_message_text("🔄 جاري الإنشاء...\n⏱️ قد يستغرق 2-3 دقائق")
        success, email, username, password, uid = make()
        if success:
            text = f"✅ *تم الإنشاء!*\n📧 `{email}`\n👤 `{username}`\n🔑 `{password}`"
            await query.edit_message_text(text, parse_mode="Markdown")
        else:
            await query.edit_message_text("❌ *فشل الإنشاء*\nInstagram يحظر المحاولات حالياً.\nانتظر 24 ساعة وحاول مرة أخرى.", parse_mode="Markdown")
        await asyncio.sleep(3)
        await main_menu(update, context, chat_id=user_id)
    
    elif data == "show_accounts":
        try:
            with open("accounts.txt", "r") as f:
                acc = f.readlines()
            if acc:
                text = "📁 *الحسابات:*\n" + "".join(acc[-10:])
                await query.edit_message_text(text, parse_mode="Markdown")
            else:
                await query.edit_message_text("📁 *لا توجد حسابات*", parse_mode="Markdown")
        except:
            await query.edit_message_text("📁 *لا توجد حسابات*", parse_mode="Markdown")
        await asyncio.sleep(2)
        await main_menu(update, context, chat_id=user_id)
    
    elif data == "clear_accounts":
        open("accounts.txt", "w").close()
        await query.edit_message_text("✅ *تم المسح*", parse_mode="Markdown")
        await asyncio.sleep(1)
        await main_menu(update, context, chat_id=user_id)
    
    elif data == "back_to_menu":
        await main_menu(update, context, chat_id=user_id)

# ------------------- الكود الرئيسي للتشغيل -------------------
if __name__ == "__main__":
    # تشغيل Flask في خيط منفصل
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # تشغيل بوت Telegram
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print(Fore.GREEN + "✅ البوت يعمل! أرسل /start" + Fore.RESET)
    print(Fore.CYAN + f"🤖 التوكن: {BOT_TOKEN[:20]}...")
    print(f"👤 الايدي: {ADMIN_ID}" + Fore.RESET)
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)
