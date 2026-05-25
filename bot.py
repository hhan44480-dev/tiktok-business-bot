import re
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Logging ဆက်တင် (Bot အခြေအနေ စောင့်ကြည့်ရန်)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# မိမိရဲ့ Bot Token 
TOKEN = "8634598434:AAH_oI7h-zXrR1ha-gKubsZHsw32ILaYbMo"

# စျေးနှုန်းသတ်မှတ်ချက်များ (1k အတွက် စျေးနှုန်း)
LIKE_PRICE_PER_K = 4500
VIEW_PRICE_PER_K = 1000

# မီနူးစာသား
MENU_TEXT = """
✨ TikTok Like & View ဝန်ဆောင်မှုများ ✨

🔹 Like 1k - 4500 ks [ ပြန်မကျ ✅ ]
🔹 View 1k - 1000 ks [ ပြန်မကျ ✅ ]

ကိုယ်ကြိုက်နှစ်သက်ရာပမာဏ Like 100 / View 1000 အနည်းဆုံးဖြင့် ရွေးချယ်ဝယ်ယူနိုင်ပါတယ်ရှင့်။

📌 Like & view နှစ်မျိုးဝယ်ယူလိုပါက
Like..k 
View..k    ဟုရေးပါ

📌 တစ်မျိုးထဲဝယ်ယူလိုပါက 
Like..k      ဟုရေးပါ
"""

# Payment အချက်အလက်
PAYMENT_TEXT = """
💰 ကျသင့်ငွေကို အောက်ပါ Account သို့ လွှဲပေးပါရန် -

💳 09403095335 [ Kpay ] [ Wave ]
👤 Name: Han Htoo Aung

ငွေလွှဲပြီးပါက အောက်တွင် ငွေလွှဲပြေစာ (Screenshot) နဲ့ ဝန်ဆောင်မှုယူမယ့် TikTok ဗီဒီယို Link (Vd Link) တို့ကို ပို့ပေးပါနော် 🙏။
"""

# အပြီးသတ် ပြသမည့်စာသား
DONE_TEXT = "အချက်အလက်များနှင့် ဗီဒီယို Link ကို စစ်ဆေးပြီး ပြန်လည်ပြောကြားပါမည် စောင့်ဆိုင်းပေးပါနော်။ hana အား ယုံကြည်စိတ်ချစွာ ဝယ်ယူအားပေးတဲ့အတွက် ကျေးဇူးတင်ပါတယ်ရှင် 🙏"

# /start ပို့ရင် သို့မဟုတ် ခလုတ်နှိပ်ရင် ပြမယ့် Function
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['has_photo'] = False
    context.user_data['has_link'] = False
    
    keyboard = [[KeyboardButton("🛒 ဝယ်ယူမည်")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    
    await update.message.reply_text("မင်္ဂလာပါရှင် 🙏\nTikTok Like & View ဝန်ဆောင်မှုများ ရယူလိုပါက အောက်က '🛒 ဝယ်ယူမည်' ခလုတ်ကို နှိပ်ပါ သို့မဟုတ် စာရိုက်၍ မှာယူနိုင်ပါတယ်ရှင့်။", reply_markup=reply_markup)

# စာသားများကို ဖတ်ပြီး စျေးနှုန်းတွက်ချက်ပေးမယ့် Function
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text.lower().strip()
    
    if 'has_photo' not in context.user_data: context.user_data['has_photo'] = False
    if 'has_link' not in context.user_data: context.user_data['has_link'] = False
    
    # ၁။ 'ဝယ်ယူမည်' ခလုတ်နှိပ်ရင် စျေးနှုန်းစာရင်းပြမယ်
    if user_text == "🛒 ဝယ်ယူမည်":
        await update.message.reply_text(MENU_TEXT)
        return

    # ၂။ ဗီဒီယို Link ပို့လာရင် စစ်ဆေးခြင်း
    if "http" in user_text or "tiktok" in user_text:
        context.user_data['has_link'] = True
        
        if context.user_data['has_photo']:
            await update.message.reply_text(DONE_TEXT)
            context.user_data['has_photo'] = False
            context.user_data['has_link'] = False
        else:
            await update.message.reply_text("Vd link လက်ခံရရှိပါပြီ ငွေလွှဲပြေစာအားဆက်လက်ပို့ဆောင်ပေးပါနော် 🙏")
        return

    # ၃။ Like နှင့် View ပမာဏကို စာသားထဲကနေ ရှာဖွေတွက်ချက်ခြင်း (Regex)
    like_match = re.search(r'like\s*([\d\.]+)\s*(k?)', user_text)
    view_match = re.search(r'view\s*([\d\.]+)\s*(k?)', user_text)
    
    if not like_match and not view_match:
        keyboard = [[KeyboardButton("🛒 ဝယ်ယူမည်")]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("TikTok Like & View ဝန်‌ေဆာင်မှုများ ဖြစ်ပါတယ်ရှင့်။ အသေးစိတ်ကြည့်ရန် အောက်က '🛒 ဝယ်ယူမည်' ခလုတ်ကို နှိပ်ပေးပါရန်။", reply_markup=reply_markup)
        return

    total_price = 0
    reply_bill = "📝 **သင်ဝယ်ယူလိုသော ပမာဏ ပြေစာ**\n\n"

    # Like ရှိရင် တွက်မယ်
    if like_match:
        val = float(like_match.group(1))
        has_k_like = like_match.group(2) == 'k'
        like_amount = val if has_k_like else val / 1000
        
        if like_amount < 0.1:
            await update.message.reply_text("❌ စိတ်မရှိပါနဲ့ရှင့်၊ Like ဝယ်ယူမှုသည် အနည်းဆုံး 100 Like ဖြစ်ရပါမယ်။")
            return
            
        price = like_amount * LIKE_PRICE_PER_K
        total_price += price
        reply_bill += f"❤️ Like: {like_match.group(1)}{'k' if has_k_like else ''} = {int(price)} ks\n"

    # View ရှိရင် တွက်မယ်
    if view_match:
        val = float(view_match.group(1))
        has_k_view = view_match.group(2) == 'k'
        view_amount = val if has_k_view else val / 1000
        
        if view_amount < 1.0:
            await update.message.reply_text("❌ စိတ်မရှိပါနဲ့ရှင့်၊ View ဝယ်ယူမှုသည် အနည်းဆုံး 1000 View ဖြစ်ရပါမယ်။")
            return
            
        price = view_amount * VIEW_PRICE_PER_K
        total_price += price
        reply_bill += f"👁️ View: {view_match.group(1)}{'k' if has_k_view else ''} = {int(price)} ks\n"

    # စုစုပေါင်းပြေစာ ပို့ပေးမယ်
    reply_bill += f"💰 **စုစုပေါင်းကျသင့်ငွေ: {int(total_price)} ကျပ်**\n"
    await update.message.reply_text(reply_bill)
    await update.message.reply_text(PAYMENT_TEXT)

# ပုံ (ငွေလွှဲပြေစာ Screenshot) ပို့လာရင်
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if 'has_photo' not in context.user_data: context.user_data['has_photo'] = False
    if 'has_link' not in context.user_data: context.user_data['has_link'] = False
    
    context.user_data['has_photo'] = True
    
    if context.user_data['has_link']:
        await update.message.reply_text(DONE_TEXT)
        context.user_data['has_photo'] = False
        context.user_data['has_link'] = False
    else:
        await update.message.reply_text("ငွေလွှဲပြေစာလက်ခံရရှိပါပြီ vd link အားဆက်လက်ပို့ဆောင်ပေးပါနော် 🙏")

def main():
    app = Application.builder().token(TOKEN).read_timeout(30).write_timeout(30).connect_timeout(30).pool_timeout(30).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Business Bot စတင်အလုပ်လုပ်နေပါပြီ...")
    app.run_polling()

if __name__ == '__main__':
    main()
      
