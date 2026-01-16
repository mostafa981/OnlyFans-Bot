#!/usr/bin/env python3
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

# دالة إرسال الإيميل
def send_email(subject, body):
    sender_email = "sasa0messi@gmail.com"
    receiver_email = "sasa0messi@gmail.com"
    password = "xlle qadv prjf wega"
    
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = Header(subject, 'utf-8')
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        
        print(f"✅ تم إرسال إيميل: {subject}")
        return True
        
    except Exception as e:
        print(f"❌ فشل إرسال الإيميل: {e}")
        return False

# دالة فحص الصفحات
def check_for_updates(url, keyword):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    service = Service('/usr/local/bin/chromedriver')
    
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        print(f"🌐 تم فتح: {url}")

        try:
            subscribe_button = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".b-offer-join__btn, .m-rounded.m-flex.m-space-between.m-lg.g-btn")
                )
            )
            print(f"✅ وجد زر الاشتراك في {url}")

            button_text = subscribe_button.text.lower()
            print(f"📝 نص الزر: {button_text}")

            if keyword.lower() in button_text:
                send_email(f"Update Found on {url}", f"أنا\n\nThere's a free offer available on {url}")
                driver.quit()
                return True
            else:
                driver.quit()
                return False
                
        except Exception as e:
            print(f"❌ لم يتم العثور على زر الاشتراك في {url}: {e}")
            driver.quit()
            return False
            
    except Exception as e:
        print(f"💥 خطأ في فتح المتصفح لـ {url}: {e}")
        return False

# قراءة الروابط من ملف
def load_urls_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            urls = file.readlines()
        urls = [url.strip() for url in urls if url.strip()]
        print(f"📋 تم تحميل {len(urls)} رابط من {filename}")
        return urls
    except Exception as e:
        print(f"❌ خطأ في قراءة الملف {filename}: {e}")
        return []

# التشغيل الرئيسي
if __name__ == "__main__":
    print("🚀 بدء فحص العروض...")
    print(f"⏰ الوقت: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    urls = load_urls_from_file('urls.txt')
    
    if not urls:
        print("❌ لا توجد روابط للفحص")
        exit()
    
    keyword = "free for"
    print(f"🔍 البحث عن كلمة: '{keyword}'")
    
    offers_found = 0
    for url in urls:
        print(f"\n📡 جاري فحص {url}...")
        if check_for_updates(url, keyword):
            offers_found += 1
        time.sleep(2)
    
    print(f"\n🎉 انتهى الفحص. وجد {offers_found} عرض مجاني.")
    print(f"⏰ وقت الانتهاء: {time.strftime('%Y-%m-%d %H:%M:%S')}")
