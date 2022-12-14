from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


API_ID = # 1234567
API_HASH = # "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
BOT_TOKEN = # "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
LOG_GROUP = # -111111111
MAIN_CHANNEL = # -1111111111111


Client = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

MarkupForApprove=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Accept", callback_data="accept"),
                    InlineKeyboardButton(
                        "Decline", callback_data="decline")
                ]
            ]
        )


@Client.on_message(filters.sticker & filters.private)
async def SendSticker(client, message):
    await client.send_sticker(
        message.chat.id,
        "CAACAgIAAxkBAAIEYWOaKtt5BTKaR52yuLi3llEBLHzKAAJPAANBtVYMVdCIyu7r_pgeBA"
    )


@Client.on_message(filters.text & filters.private)
async def TextMessage(client, message):
    mes = "{mes}\n\n Shared by - [{user}](tg://user?id={id})"
    mes=mes.format(
        mes=message.text,
        user=message.chat.first_name,
        id=message.chat.id
    )
    await client.send_message(
        LOG_GROUP,
        mes
    )


@Client.on_message(filters.media & filters.private)
async def SendToApprove(client, message):
    if message.caption == None:
        cap=""
    else:
        cap=message.caption
    caption = "{caption}\n\n Shared by - [{user}](tg://user?id={id})"
    caption = caption.format(
        caption=cap,
        user=message.from_user.first_name,
        id=message.from_user.id
    )
    await client.copy_message(
        LOG_GROUP,
        message.chat.id,
        message.id,
        caption=caption,
        reply_markup=MarkupForApprove
    )


@Client.on_callback_query(filters.regex("accept"))
async def AcceptTheContent(client, query):
    if query.message.chat.id == LOG_GROUP:
        await client.copy_message(
            MAIN_CHANNEL,
            LOG_GROUP,
            query.message.id
        )
        mess = await client.get_messages(
            LOG_GROUP,
            query.message.id
        )
        caption = "{old_cap} [{user}](tg://user?id={id}) \n Accepted by - [{user2}](tg://user?id={id2})"
        caption = caption.format(
            old_cap=mess.caption,
            user=mess.caption_entities[0].user.first_name,
            id=mess.caption_entities[0].user.id,
            user2=query.from_user.first_name,
            id2=query.from_user.id
        )
        await query.edit_message_text(caption)


@Client.on_callback_query(filters.regex("decline"))
async def RefuseTheContent(client, query):
    if query.message.chat.id == LOG_GROUP:
        mess = await client.get_messages(
            LOG_GROUP,
            query.message.id
        )
        caption = "{old_cap} [{bywhom}](tg://user?id={id}) \n Declined by - [{bywhom2}](tg://user?id={id2})"
        caption = caption.format(
            old_cap=mess.caption,
            bywhom=mess.caption_entities[0].user.first_name,
            id=mess.caption_entities[0].user.id,
            bywhom2=query.from_user.first_name,
            id2=query.from_user.id
        )
        await query.edit_message_text(caption)


if __name__ == "__main__":
    Client.run()
