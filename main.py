from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime
import asyncio

# توكن البوت (استبدلته بالقيمة التي قدمتها)
TOKEN = '8470735691:AAEXDGQ6Fi_abvRxpp52Plld38Gshc15GSw'
# معرف الدردشة الخاص بالمدير (استبدلته بالقيمة التي قدمتها)
MANAGER_CHAT_ID = '7078757412'

# قائمة لتخزين الرسائل المرسلة وأوقاتها
messages = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("مرحبًا! أرسل رسالة، وسأنقلها للمدير وأحذفها بعد دقيقتين.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    if user_message:
        # إرسال الرسالة إلى المدير
        sent_message = await context.bot.send_message(chat_id=MANAGER_CHAT_ID, text=f"رسالة من {update.message.from_user.username}: {user_message}")
        # تخزين معرف الرسالة ووقت الإرسال
        messages[sent_message.message_id] = datetime.now()
        # جدولة الحذف بعد دقيقتين
        context.job_queue.run_once(delete_message, 120, data=sent_message.message_id)

async def delete_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    message_id = context.job.data
    if message_id in messages:
        try:
            await context.bot.delete_message(chat_id=MANAGER_CHAT_ID, message_id=message_id)
            del messages[message_id]
        except Exception as e:
            print(f"خطأ في الحذف: {e}")

def main() -> None:
    # إنشاء تطبيق البوت
    application = Application.builder().token(TOKEN).build()

    # إضافة المعالجات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # بدء البوت
    application.run_polling()

if __name__ == '__main__':
    main()
