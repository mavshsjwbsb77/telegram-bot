from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

# توكن البوت
TOKEN = '8470735691:AAEXDGQ6Fi_abvRxpp52Plld38Gshc15GSw'
# معرف الدردشة مع المدير
ADMIN_CHAT_ID = 7078757412

# تهيئة التطبيق
application = Application.builder().token(TOKEN).build()

# معالجة الأمر /report
async def report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text[len('/report '):]  # النص بعد الأمر
    if not message:
        await update.message.reply_text('يرجى كتابة رسالة بعد /report!')
        return

    # إرسال الرسالة إلى المدير
    bot_message = await application.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f'تقرير من {update.message.from_user.username}: {message}')

    # حذف رسالة البوت بعد 2 دقيقة
    await asyncio.sleep(120)
    await application.bot.delete_message(chat_id=ADMIN_CHAT_ID, message_id=bot_message.message_id)

    # حذف رسالة المستخدم (اختياري)
    await update.message.delete()

# إضافة معالج الأوامر
application.add_handler(CommandHandler("report", report))

# تشغيل البوت
application.run_polling()
