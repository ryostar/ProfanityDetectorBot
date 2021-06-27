from telethon import TelegramClient, events, Button, types
from decouple import config
from ProfanityDetector import detector
import logging
from telethon.tl.functions.channels import GetParticipantRequest

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.INFO
)

log = logging.getLogger(__name__)

# vars
apiid = 6
apihash = "eb06d4abfb49dc3eeb1aeb98ae0f581e"
BOT_TOKEN = config("BOT_TOKEN", default=None)

log.info("Starting Bot...")

bot = TelegramClient("bot", apiid, apihash).start(bot_token=BOT_TOKEN)

# check admins
async def check_if_admin(message):
    result = await bot(
        GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(
        p, (types.ChannelParticipantCreator, types.ChannelParticipantAdmin)
    )


@bot.on(
    events.NewMessage(incoming=True, pattern="^/start$", func=lambda e: e.is_private)
)
async def start_msg(event):
    sender = await bot.get_entity(event.sender_id)
    await event.reply(
        f"Hi {sender.first_name}!\nTôi là một bot phát hiện ngôn từ tục tĩu.\n\nĐặt tôi làm quản trị viên trong nhóm của bạn với quyền `xóa tin nhắn` và tôi sẽ xóa các tin nhắn có chứa nội dung lạm dụng!",
        buttons=[
            [Button.inline("Help 🆘", data="helpme")],
            [
                Button.url(
                    "Add me to a group ➕",
                    url=f"http://t.me/{(await bot.get_me()).username}?startgroup=botstart",
                )
            ],
            [
                Button.url("📥 Channel", url="https://t.me/Kenhsex"),
                Button.url(
                    "Admin 📦", url="https://t.me/cunongdan"
                ),
            ],
        ],
    )


@bot.on(events.NewMessage(incoming=True, pattern="^/start", func=lambda e: e.is_group))
async def start_grp(event):
    sender = await bot.get_entity(event.sender_id)
    await event.reply(
        f"Hey {sender.first_name}!\n__Tôi đứng lên, bảo vệ nhóm này!__\n**Dương tính giả?** Báo cáo họ với @cunongdan!"
    )


@bot.on(events.callbackquery.CallbackQuery(data="helpme"))
async def helper_(event):
    sender = await bot.get_entity(event.sender_id)
    await event.edit(
        f"""
{sender.first_name}, đây là menu trợ giúp.\n
**How to use?**
- Thêm tôi vào một nhóm và đặt tôi làm quản trị viên, với quyền \"delete messages\" .
- Nếu bot không phải là quản trị viên, nó sẽ không xóa các tin nhắn chứa các từ nằm trong danh sách đen.\n
**Báo cáo khẳng định sai:**
- Bạn có thể tự do báo cáo Phát hiện sai trong @cunongdan.""",
        buttons=[[Button.inline("Back", data="start")]],
    )


@bot.on(events.callbackquery.CallbackQuery(data="start"))
async def start_msg(event):
    sender = await bot.get_entity(event.sender_id)
    await event.edit(
        f"Hi {sender.first_name}!\nI am a profanity detector bot.\n\nMake me admin in your group with `delete messages` permission and I'll delete messsages containing abuses!",
        buttons=[
            [Button.inline("Help 🆘", data="helpme")],
            [
                Button.url(
                    "Add me to a group ➕",
                    url=f"http://t.me/{(await bot.get_me()).username}?startgroup=botstart",
                )
            ],
            [
                Button.url("📥 Channel", url="https://t.me/BotzHub"),
                Button.url(
                    "Package 📦", url="https://pypi.org/project/ProfanityDetector/"
                ),
            ],
        ],
    )


@bot.on(events.NewMessage(incoming=True, func=lambda e: e.is_group))
async def deleter_(event):
    try:
        if await check_if_admin(event):
            return
    except:
        return
    sentence = event.raw_text
    sender = await bot.get_entity(event.sender_id)
    word, detected = detector(sentence)
    if detected:
        try:
            await event.reply(
                f"Hey {sender.first_name}, you used a blacklisted word and so your message has been deleted!"
            )
            await event.delete()
        except:
            log.info(f"Cannot delete messages in {(await event.get_chat()).title}.")


log.info("Bot has started!")
bot.run_until_disconnected()
