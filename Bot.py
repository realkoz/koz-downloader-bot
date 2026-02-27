
import os
import logging
import re
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
import yt_dlp

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8764825754:AAFZhsT94Z3K8ON8lqNOEptqoirw2-0ppsQ")
OWNER_USERNAME = "@realkoz"
BOT_USERNAME = "@Kozdownloaderbot"
OWNER_ID = 7984931982  # Apna Telegram ID yahan daalo

# Force join channels
CHANNELS = [
    {"username": "@kozpy", "invite_link": "https://t.me/kozpy"},
    {"username": "@kozxmusic", "invite_link": "https://t.me/kozxmusic"},
    {"username": "@TeamDeath0", "invite_link": "https://t.me/TeamDeath0"},
    {"username": "@pikapikagc", "invite_link": "https://t.me/pikapikagc"},
    {"username": "@kozfreestore", "invite_link": "https://t.me/kozfreestore"},
    {"username": "@kozraw", "invite_link": "https://t.me/kozraw"},
]

# URL Regex
URL_RE = re.compile(r'(https?://[^\s]+)')

# ================= FORCE JOIN CHECK ================= #

async def check_force_join(user_id: int, context: ContextTypes.DEFAULT_TYPE):
    """Check if user has joined all channels"""
    unjoined = []
    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel["username"], user_id=user_id)
            if member.status in ['left', 'kicked']:
                unjoined.append(channel)
        except:
            unjoined.append(channel)
    return unjoined

# ================= FORCE JOIN MESSAGE ================= #

async def send_force_join(update: Update, unjoined):
    """Send force join message with inline join buttons"""
    text = "📛 𝘗𝘭𝘦𝘢𝘴𝘦 𝘑𝘰𝘪𝘯 𝘈𝘭𝘭 𝘔𝘺 𝘜𝘱𝘥𝘢𝘵𝘦 𝘊𝘩𝘢𝘯𝘯𝘦𝘭𝘴 𝘛𝘰 𝘜𝘴𝘦 𝘔𝘦 !"

    # Create inline buttons - sirf JOIN buttons
    keyboard = []
    row = []
    for i, ch in enumerate(unjoined):
        row.append(InlineKeyboardButton("📢 Join", url=ch['invite_link']))
        if len(row) == 2 or i == len(unjoined)-1:
            keyboard.append(row)
            row = []

    keyboard.append([InlineKeyboardButton("♻️ Try Again", callback_data="try_again")])

    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    else:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

# ================= WELCOME MESSAGE ================= #

async def send_welcome(update: Update, first_name: str):
    """Send welcome message with MIXED buttons:
    - Instagram, YouTube, Pinterest: INLINE buttons
    - Owner, About, Feedback: REPLY KEYBOARD buttons
    """
    welcome_text = (
        f"ʜᴇʏ 👋 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴍᴇᴅɪᴀ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ ʙᴏᴛ\n\n"
        f"ʏᴏᴜ ᴄᴀɴ ᴅᴏᴡɴʟᴏᴀᴅ ᴍᴇᴅɪᴀ ғʀᴏᴍ:\n\n"
        f"• ɪɴsᴛᴀɢʀᴀᴍ 📸\n"
        f"• ʏᴏᴜᴛᴜʙᴇ 🎥\n"
        f"• ᴘɪɴᴛᴇʀᴇsᴛ 📌\n\n"
        f"────────────\n\n"
        f"ʜᴏᴡ ᴛᴏ ᴜsᴇ:\n\n"
        f"1. ᴄᴏᴘʏ ᴛʜᴇ ʟɪɴᴋ 🔗\n"
        f"2. sᴇɴᴅ ɪᴛ ʜᴇʀᴇ 📩\n"
        f"3. ᴡᴀɪᴛ ᴀ ғᴇᴡ sᴇᴄᴏɴᴅs ⏳\n"
        f"4. ᴅᴏᴡɴʟᴏᴀᴅ ʏᴏᴜʀ ᴍᴇᴅɪᴀ ✅\n\n"
        f"────────────\n\n"
        f"✔ ғᴀsᴛ\n"
        f"✔ ʜɪɢʜ ǫᴜᴀʟɪᴛʏ\n"
        f"✔ sɪᴍᴘʟᴇ\n\n"
        f"⚠️ ᴘʀɪᴠᴀᴛᴇ ᴄᴏɴᴛᴇɴᴛ ɴᴏᴛ sᴜᴘᴘᴏʀᴛᴇᴅ\n\n"
        f"sᴇɴᴅ ᴀ ʟɪɴᴋ ᴀɴᴅ sᴛᴀʀᴛ 🚀"
    )

    # 🔥 INLINE BUTTONS for platforms (message ke ANDAR)
    inline_keyboard = [
        [
            InlineKeyboardButton("📸 Instagram", callback_data="show_instagram"),
            InlineKeyboardButton("🎥 YouTube", callback_data="show_youtube")
        ],
        [
            InlineKeyboardButton("📌 Pinterest", callback_data="show_pinterest")
        ]
    ]

    # 🔥 REPLY KEYBOARD for owner/about/feedback (keyboard PE)
    reply_keyboard = [
        [KeyboardButton("👑 Owner"), KeyboardButton("📌 About"), KeyboardButton("💬 Feedback")]
    ]

    if update.callback_query:
        await update.callback_query.edit_message_text(
            welcome_text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard),
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            welcome_text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard),
            parse_mode='Markdown'
        )

        # Reply keyboard alag se bhejo (niche dikhega)
        await update.message.reply_text(
            "📌 **Menu Options:**",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=False),
            parse_mode='Markdown'
        )

# ================= START COMMAND ================= #

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name

    context.user_data.clear()

    unjoined = await check_force_join(user_id, context)

    if unjoined:
        await send_force_join(update, unjoined)
    else:
        await send_welcome(update, first_name)

# ================= TRY AGAIN CALLBACK ================= #

async def try_again_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    user_id = q.from_user.id
    first_name = q.from_user.first_name

    unjoined = await check_force_join(user_id, context)

    if not unjoined:
        await send_welcome(update, first_name)
    else:
        await send_force_join(update, unjoined)

# ================= INLINE BUTTON HANDLER ================= #

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all inline button clicks (Instagram/YouTube/Pinterest)"""
    q = update.callback_query
    await q.answer()

    user_id = q.from_user.id
    first_name = q.from_user.first_name
    data = q.data

    # Check force join for every action
    unjoined = await check_force_join(user_id, context)
    if unjoined:
        await send_force_join(update, unjoined)
        return

    # Handle different button clicks
    if data == "show_instagram":
        text = (
            "• ✦ ɪɴsᴛᴀɢʀᴀᴍ ᴅᴏᴡɴʟᴏᴀᴅ ᴢᴏɴᴇ ✦\n"
            "ɢᴇᴛ ᴀɴʏ ᴘᴜʙʟɪᴄ ᴄᴏɴᴛᴇɴᴛ ɪɴ sᴇᴄᴏɴᴅs:\n"
            "➊ sᴇɴᴅ ᴜsᴇʀɴᴀᴍᴇ / ᴘʀᴏғɪʟᴇ ʟɪɴᴋ\n"
            "➋ sᴇɴᴅ ᴘᴏsᴛ / ʀᴇᴇʟ ʟɪɴᴋ\n"
            "➤ sɪᴍᴘʟᴇ, ғᴀsᴛ & ᴄᴏɴᴠᴇɴɪᴇɴᴛ"
        )
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back_to_main")]]
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif data == "show_youtube":
        text = (
            "• ✦ ʏᴏᴜᴛᴜʙᴇ ᴅᴏᴡɴʟᴏᴀᴅ ᴢᴏɴᴇ ✦\n"
            "ᴅᴏᴡɴʟᴏᴀᴅ ʏᴏᴜʀ ғᴀᴠᴏʀɪᴛᴇ ᴄᴏɴᴛᴇɴᴛ ɪɴ ᴍᴜʟᴛɪᴘʟᴇ ᴡᴀʏs:\n"
            "➊ sᴇɴᴅ ᴅɪʀᴇᴄᴛ ᴠɪᴅᴇᴏ ʟɪɴᴋ\n"
            "➋ sᴇɴᴅ ᴍᴜsɪᴄ ʟɪɴᴋ\n"
            "➌ sᴇɴᴅ ᴋᴇʏᴡᴏʀᴅs ғᴏʀ sᴇᴀʀᴄʜ\n"
            "➤ ᴘɪᴄᴋ ᴡʜᴀᴛ's ᴇᴀsɪᴇsᴛ ғᴏʀ ʏᴏᴜ"
        )
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back_to_main")]]
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif data == "show_pinterest":
        text = (
            "• ✦ ᴘɪɴᴛᴇʀᴇsᴛ ᴅᴏᴡɴʟᴏᴀᴅ ᴢᴏɴᴇ ✦\n"
            "ʏᴏᴜ ᴄᴀɴ ᴇᴀsɪʟʏ sᴀᴠᴇ ᴀɴʏ ᴘᴜʙʟɪᴄ ᴘɪɴᴛᴇʀᴇsᴛ ᴠɪᴅᴇᴏ ᴏʀ ɪᴍᴀɢᴇ\n"
            "➤ ᴊᴜsᴛ ᴅʀᴏᴘ ᴛʜᴇ ʟɪɴᴋ ᴀɴᴅ ɪ'ʟʟ ғᴇᴛᴄʜ ɪᴛ ғᴏʀ ʏᴏᴜ"
        )
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back_to_main")]]
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif data == "back_to_main":
        await send_welcome(update, first_name)

# ================= REPLY BUTTON HANDLER ================= #

async def handle_reply_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle reply keyboard buttons (Owner/About/Feedback)"""
    user_id = update.effective_user.id
    text = update.message.text
    first_name = update.effective_user.first_name

    # Check force join
    unjoined = await check_force_join(user_id, context)
    if unjoined:
        await send_force_join(update, unjoined)
        return

    if text == "👑 Owner":
        owner_text = (
            "╔═━───━─━─━─━─━─━─═╗\n"
            "👨‍💻 𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿 𝗣𝗿𝗼𝗳𝗶𝗹𝗲\n"
            "╚═━───━─━─━─━─━─━─═╝\n\n"
            "• 👤 ᴜꜱᴇʀɴᴀᴍᴇ : @realkoz\n"
            "• 🛠️ ʀᴏʟᴇ : ᴅᴇᴠᴇʟᴏᴘᴇʀ & ᴇᴛʜɪᴄᴀʟ ʜᴀᴄᴋᴇʀ\n"
            "• 🏴‍☠️ ꜰᴏᴜɴᴅᴇʀ : ᴛᴇᴀᴍ ᴅᴇᴀᴛʜ\n\n"
            "📪 ꜰᴏʀ ꜱᴜᴘᴘᴏʀᴛ ᴏʀ ʙᴜꜱɪɴᴇꜱꜱ ɪɴQᴜɪʀɪᴇꜱ, ᴅɪʀᴇᴄᴛ ᴍᴇꜱꜱᴀɢᴇ"
        )
        await update.message.reply_text(owner_text, parse_mode='Markdown')

    elif text == "📌 About":
        about_text = (
            "╔═━───━─━─━─━─━─━─═╗\n"
            "🤖 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺 𝗠𝗲𝗱𝗶𝗮 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗲𝗿\n"
            "╚═━───━─━─━─━─━─━─═╝\n\n"
            "🔗 ᴅᴏᴡɴʟᴏᴀᴅ ɪɴꜱᴛᴀɢʀᴀᴍ ʀᴇᴇʟꜱ ᴘᴏꜱᴛꜱ ꜱᴛᴏʀɪᴇꜱ ᴀɴᴅ ʜɪɢʜʟɪɢʜᴛꜱ\n"
            "🖇️ ꜱᴇɴᴅ ᴀɴʏ ɪɴꜱᴛᴀɢʀᴀᴍ ʟɪɴᴋ ᴛᴏ ɪɴɪᴛɪᴀᴛᴇ ᴘʀᴏᴄᴇꜱꜱɪɴɢ\n"
            "🎧 ᴄʜᴏᴏꜱᴇ ᴀᴜᴅɪᴏ ᴏʀ 🎬 ᴠɪᴅᴇᴏ ꜰᴏʀᴍᴀᴛ\n\n"
            "════════════════════\n\n"
            "🚀 𝗡𝗲𝗲𝗱 𝗮 𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝗕𝗼𝘁?\n\n"
            "• ⚙️ ᴄᴜꜱᴛᴏᴍ ʙᴏᴛ ᴅᴇᴠᴇʟᴏᴘᴍᴇɴᴛ\n"
            "• 💎 ᴀᴅᴠᴀɴᴄᴇᴅ & ᴘʀᴇᴍɪᴜᴍ ꜰᴇᴀᴛᴜʀᴇꜱ\n"
            "• ⚡ ꜰᴀꜱᴛ ᴅᴇᴘʟᴏʏᴍᴇɴᴛ & ꜱᴇᴄᴜʀᴇ ꜱᴇᴛᴜᴘ\n"
            "• 📪 24/7 ᴅᴇᴅɪᴄᴀᴛᴇᴅ ꜱᴜᴘᴘᴏʀᴛ\n\n"
            "🖇️ ᴄᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ ꜰᴏʀ ᴄᴏʟʟᴀʙᴏʀᴀᴛɪᴏɴ & ʙᴜꜱɪɴᴇꜱꜱ"
        )
        await update.message.reply_text(about_text, parse_mode='Markdown')

    elif text == "💬 Feedback":
        await update.message.reply_text(
            "📝 **Send your feedback**\n\nType your message below and I'll forward it to the owner.",
            parse_mode='Markdown'
        )
        context.user_data['awaiting_feedback'] = True

# ================= FEEDBACK HANDLER ================= #

async def handle_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user feedback messages"""
    if context.user_data.get('awaiting_feedback'):
        user = update.effective_user
        feedback_text = update.message.text

        owner_message = (
            f"📬 **New Feedback**\n\n"
            f"**From:** {user.first_name}\n"
            f"**Username:** @{user.username if user.username else 'N/A'}\n"
            f"**User ID:** `{user.id}`\n\n"
            f"**Message:**\n{feedback_text}"
        )

        try:
            await context.bot.send_message(OWNER_ID, owner_message, parse_mode='Markdown')
            await update.message.reply_text("✅ Feedback sent successfully!")
        except:
            await update.message.reply_text("❌ Failed to send feedback.")

        context.user_data['awaiting_feedback'] = False

# ================= MESSAGE HANDLER ================= #

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all messages with force join check"""
    user_id = update.effective_user.id
    text = update.message.text

    # Check feedback first
    if context.user_data.get('awaiting_feedback'):
        await handle_feedback(update, context)
        return

    # Check force join
    unjoined = await check_force_join(user_id, context)
    if unjoined:
        await send_force_join(update, unjoined)
        return

    # Check for URLs
    match = URL_RE.search(text)

    if match:
        context.user_data['link'] = match.group(1)

        link_lower = match.group(1).lower()
        platform = "Unknown"
        if "youtube.com" in link_lower or "youtu.be" in link_lower:
            platform = "YouTube"
        elif "instagram.com" in link_lower:
            platform = "Instagram"
        elif "pinterest.com" in link_lower or "pin.it" in link_lower:
            platform = "Pinterest"

        keyboard = [[
            InlineKeyboardButton("🔊 Audio (MP3)", callback_data="audio"),
            InlineKeyboardButton("🎥 Video (MP4)", callback_data="video")
        ]]
        await update.message.reply_text(
            f"📥 **{platform} Link Detected!**\n\nChoose format:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            "❌ **Invalid link!**\n\n"
            "Please send a valid link from:\n"
            "• YouTube\n"
            "• Instagram\n"
            "• Pinterest",
            parse_mode='Markdown'
        )

# ================= FORMAT CALLBACK ================= #

async def format_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle audio/video selection"""
    q = update.callback_query
    await q.answer()

    user_id = q.from_user.id
    first_name = q.from_user.first_name

    # Check force join
    unjoined = await check_force_join(user_id, context)
    if unjoined:
        await send_force_join(update, unjoined)
        return

    link = context.user_data.get('link')

    if not link:
        await q.edit_message_text("❌ Link expired. Send again.")
        return

    await q.edit_message_text("⏬ **Downloading...**\n\nPlease wait...", parse_mode='Markdown')

    try:
        loop = asyncio.get_event_loop()

        if q.data == "audio":
            path = await loop.run_in_executor(None, download_audio, link)
            await context.bot.send_audio(
                q.from_user.id,
                open(path, 'rb'),
                caption="✅ Downloaded by @Kozdownloaderbot"
            )
        else:
            path = await loop.run_in_executor(None, download_video, link)
            await context.bot.send_video(
                q.from_user.id,
                open(path, 'rb'),
                supports_streaming=True,
                caption="✅ Downloaded by @Kozdownloaderbot"
            )

        share_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📤 Share Bot", url=f"https://t.me/share/url?url=https://t.me/{BOT_USERNAME[1:]}")],
        ])

        await context.bot.send_message(
            q.from_user.id,
            "✅ **Download Completed!**\n\nShare this bot with friends  👇",
            reply_markup=share_keyboard,
            parse_mode='Markdown'
        )

        os.remove(path)

    except Exception as e:
        error_msg = str(e)
        if "Pinterest" in error_msg:
            await context.bot.send_message(
                q.from_user.id,
                "❌ **Pinterest video unavailable**\n\nTry audio format instead.",
                parse_mode='Markdown'
            )
        else:
            await context.bot.send_message(
                q.from_user.id,
                f"❌ **Download Failed**\n\nError: {error_msg[:200]}",
                parse_mode='Markdown'
            )

# ================= DOWNLOAD FUNCTIONS ================= #

def download_audio(link):
    os.makedirs("downloads", exist_ok=True)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=True)
        return os.path.splitext(ydl.prepare_filename(info))[0] + ".mp3"

def download_video(link):
    os.makedirs("downloads", exist_ok=True)
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': True,
        'noplaylist': True,
    }
    if 'pinterest' in link.lower() or 'pin.it' in link.lower():
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        ydl_opts['ignoreerrors'] = True
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(link, download=True)
            return ydl.prepare_filename(info)
        except Exception as e:
            if 'pinterest' in link.lower():
                raise Exception("Pinterest video format not available. Try audio instead.")
            raise e

# ================= MAIN ================= #

def main():
    os.makedirs("downloads", exist_ok=True)
    app = Application.builder().token(BOT_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))

    # Reply button handlers (Owner/About/Feedback)
    app.add_handler(MessageHandler(
        filters.Regex('^(👑 Owner|📌 About|💬 Feedback)$'),
        handle_reply_buttons
    ))

    # Callback handlers - INLINE buttons ke liye
    app.add_handler(CallbackQueryHandler(try_again_callback, pattern="try_again"))
    app.add_handler(CallbackQueryHandler(button_callback, pattern="^(show_|back_to_main)"))
    app.add_handler(CallbackQueryHandler(format_callback, pattern="^(audio|video)$"))

    # Message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ KOZ Downloader Bot Running...")
    print("📱 Platforms: INLINE Buttons | 👑 Owner/About: Reply Keyboard")
    app.run_polling()

if __name__ == "__main__":
    main()