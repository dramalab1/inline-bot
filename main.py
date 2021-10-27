import asyncio
import re
from logging import INFO, basicConfig

from telethon import Button, TelegramClient, events
from telethon.errors.rpcerrorlist import (
    PeerIdInvalidError,
    UserAlreadyParticipantError,
    UserIsBlockedError,
)
from telethon.sessions import StringSession
from telethon.tl.functions.messages import ImportChatInviteRequest

from var import Var

basicConfig(format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=INFO)

try:
    tgbot = TelegramClient(None, Var.API_ID, Var.API_HASH)
    bot = TelegramClient(StringSession(Var.SESSION), Var.API_ID, Var.API_HASH)
except Exception as ap:
    print(f"ERROR - {ap}")
    exit(1)

try:
    tgbot.start(bot_token=Var.BOT_TOKEN)
    bot.start()
except Exception as er:
    print(str(er))


@tgbot.on(events.NewMessage(incoming=True, pattern="/start"))
async def helpp(e):
    if e.fwd_from:
        return
    button = Button.switch_inline("Search inline", same_peer=True)
    text = "Use Inline And Confirm, So Bot will send all data in your pm."
    await e.reply(text, buttons=button)


@tgbot.on(events.NewMessage(incoming=True, pattern="/ping$"))
async def pingg(e):
    if e.fwd_from:
        return
    await e.reply("`Pong!!!`")


Dic = {}


@tgbot.on(events.InlineQuery)
async def _(e):
    zzz = e.text
    Dic.update({len(Dic): [e.query.user_id, zzz]})
    button = Button.inline("Confirm", data=f"v_{len(Dic)-1}")
    sur = e.builder.article(
        title=f"Search key : {zzz}",
        description="click here",
        text="click button to confirm",
        buttons=button,
    )
    await e.answer([sur])


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"v_(.*)")))
async def _(e):
    key = int(e.pattern_match.group(1).decode("UTF-8"))
    if e.sender_id != Dic[key][0]:
        return await e.answer("Not for you")
    sh = Dic[key][1].split("|")
    if len(sh) == 2:
        search, in_ch = sh[0], int(sh[1]) if sh[1].isdigit() else sh[1]
    else:
        search, in_ch = sh[0], Var.CHANNEL_ID
    bun = (await tgbot.get_me()).username
    button = [
        [Button.url("Go To Bot", url=f"https://t.me/{bun}")],
        [Button.switch_inline("Search again", same_peer=True)],
    ]
    await e.edit(
        "Transferring Files Related to query in your personal chat.", buttons=button
    )
    cc = 0
    user = e.sender_id
    if e.sender.username:
        user = e.sender.username
    async for x in bot.iter_messages(in_ch, search=search, reverse=True, wait_time=10):
        await asyncio.sleep(1)
        if not x.media:
            await tgbot.send_message(user, x)
            cc += 1
        else:
            ok = await bot.send_message(Var.RANDOM_CHANNEL, x)
            link = f"https://t.me/{ok.chat.username}/{ok.id}"
            file, text = link, x.text
            await asyncio.sleep(0.6)
            try:
                await tgbot.send_file(user, file=file, caption=text)
                cc += 1
            except PeerIdInvalidError:
                await ok.delete()
                button = Button.url("Start Bot", url=f"https://t.me/{bun}?start=heh")
                return await e.edit(
                    "You Must `/start` bot once, So That You can you It.",
                    buttons=button,
                )
            except UserIsBlockedError:
                await ok.delete()
                button = Button.url("Start Bot", url=f"https://t.me/{bun}?start=heh")
                return await e.edit(
                    "You Blocked The Bot, Please Unblock It.",
                    buttons=button,
                )
            except Exception as er:
                print(er)
            await ok.delete()
    await e.edit(
        f"Done Sended Total `{cc}` files in your private chat,\nRelated to keyword: `{search}`",
        buttons=button,
    )


async def join():
    if Var.INVITE_LINK:
        try:
            await bot(ImportChatInviteRequest(Var.INVITE_LINK.split("/")[-1]))
        except UserAlreadyParticipantError:
            pass
        except Exception as er:
            print(er)
            print("invite link expired, please change it")
            exit(1)


print("Bot started")
bot.loop.run_until_complete(join())
tgbot.run_until_disconnected()
