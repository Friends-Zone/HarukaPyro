from pyrogram.types import InlineKeyboardButton, Message


class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text


def paginate_modules(_page_n, module_dict, prefix, chat=None):
    modules = (
        sorted(
            [
                EqInlineKeyboardButton(
                    x.__mod_name__,
                    callback_data=f"{prefix}_module({chat},{x.__mod_name__.lower()})",
                )
                for x in module_dict.values()
            ]
        )
        if chat
        else sorted(
            [
                EqInlineKeyboardButton(
                    x.__mod_name__,
                    callback_data=f"{prefix}_module({x.__mod_name__.lower()})",
                )
                for x in module_dict.values()
            ]
        )
    )

    pairs = []
    pair = []

    for module in modules:
        pair.append(module)
        if len(pair) > 2:
            pairs.append(pair)
            pair = []

    if pair:
        pairs.append(pair)

    return pairs


def ReplyCheck(message: Message):
    reply_id = None

    if message.reply_to_message:
        reply_id = message.reply_to_message.message_id

    elif not message.from_user.is_self:
        reply_id = message.message_id

    return reply_id


def build_keyboard(buttons):
    keyb = []
    for btn in buttons:
        if btn.same_line and keyb:
            keyb[-1].append(InlineKeyboardButton(btn.name, url=btn.url))
        else:
            keyb.append([InlineKeyboardButton(btn.name, url=btn.url)])

    return keyb


def revert_buttons(buttons):
    return "".join(
        "\n[{}](buttonurl://{}:same)".format(btn.name, btn.url)
        if btn.same_line
        else "\n[{}](buttonurl://{})".format(btn.name, btn.url)
        for btn in buttons
    )
