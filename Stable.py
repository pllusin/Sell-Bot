import telebot
from telebot import types
import pandas as pd
import time
from persiantools.jdatetime import JalaliDateTime

# Load appleid Excel file
excel_file = "idcard.xlsx"
df = pd.read_excel(excel_file)
# Load User Database
user_excel = "users.xlsx"
ubank = pd.read_excel(user_excel)
# Initialize your bot with your bot token
bot = telebot.TeleBot("YOUR_BOT TOKEN"
)

# Dictionary to store user's current state
user_state = {}

package = 0
# Dictionary to store pending payments awaiting confirmation
pending_payments = {}
# Administrator's user ID
ADMIN_ID = "ADMIN_ID"
user_id = 0
total = 0
cost = 0
newbalance = 0
curred = 0
cost_curred = 0
balance_curred = 0
find_user_excel = 0
balance_row = 0
info_text = "🔱Apple ID Card🔱\nبا استفاده از دکمه خرید و انتخاب تعداد موردنیاز و پرداخت مبلغ، اپل‌آیدی بصورت خودکار برای شما ارسال میشود🍏\nپس از دریافت اکانت با استفاده از آموزش زیر همه اطلاعات را تغییر دهید✔️\n🛑 وظیفه‌ی تغییر اطلاعات اپل‌آیدی برعهده مشتری است و هرگونه تبعات ناشی از عدم تغییر متوجه خودتان میشود\n🔴 در صورت وجود هرگونه مشکل در اپل‌آیدی خریداری شده به پشتیبانی پیام دهید\n\n‼️آموزش تغییر اطلاعات اکانت:\n\n1- از طریق مرورگر خود وارد سایت appleid.apple.com بشوید 🧭.\n\n2- پس از ورود روی دکمه sign in کلیک کرده و آیدی و رمز اپل ایدی خریداری شده را وارد و  در مرحله بعد به سوالات امنیتی پاسخ دهید و روی continue‌ بزنید و بعد گزینه other option را انتخاب کرده و Do not upgrade را بزنید و  سپس continue را فشار دهید✍️\n\n3- در صفحه باز شده میتوانید آیدی و پسورد و سوالات امنیتی را تغییر دهید، درصورت تمایل برای تغییر نام و تاریخ تولد اکانت از طریق علامت کنار گزینه sign out وارد قسمت personal information شوید و نام و تاریخ تولد را تغییر دهید🧑‍💻\n"
main_text = "به ربات فروش اپل‌آیدی خوش آمدید.\nتمامی اپل‌‌آیدی های فروخته شده شامل ضمانت 💯  نات اکتیو نشدن و در سلامت کامل به مشتری تحویل داده میشود.\n❗️قبل از خرید حتما راهنمای ربات را کامل مطالعه کنید\n\n🍎 جهت همکاری و یا هرگونه راهنمایی میتوانید با فشردن دکمه پشتیبانی با ما در ارتباط باشید."
f_u = 0
LM = ""
button_clicked = False


def newuser(message):
    global ubank
    global find_user_excel
    global user_id
    user_id = message.chat.id
    find_user_excel = ubank.loc[ubank["User ID"] == user_id]
    global balance_row
    ubank = pd.read_excel(user_excel)
    global balance
    global balance_curred
    balance_row = ubank.loc[ubank["User ID"] == user_id]

    if not balance_row.empty:
        balance = balance_row["Balance"].iloc[0]

    else:
        balance = 0

        new_row = {
            "User ID": user_id,
            "Balance": balance,
            "SignUpDate": JalaliDateTime.now().strftime("%y/%m/%d | %H:%M:%S"),
            "Total Amount": total,
        }
        ubank = ubank._append(new_row, ignore_index=True)

    balance_curred = "{:,}".format(balance)


@bot.message_handler(commands=["start"])
def start(message):
    global balance
    global user_id
    user_id = message.chat.id
    newuser(message)

    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 4
    keyboard.add(types.InlineKeyboardButton("خرید", callback_data="buy"))
    keyboard.add(types.InlineKeyboardButton("راهنما", callback_data="info"))
    keyboard.add(types.InlineKeyboardButton(" کیف پول", callback_data="wallet"))
    keyboard.add(
        types.InlineKeyboardButton("پشتیبانی", url="t.me/The_erphwn"),
        types.InlineKeyboardButton("کانال ما", url="t.me/idcard1"),
    )

    global LM
    LM = bot.send_message(message.chat.id, main_text, reply_markup=keyboard)

    user_state[message.chat.id] = "main_menu"

    save_excel()


@bot.message_handler(commands=["help"])
@bot.message_handler(commands=["info"])
def info(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton("منوی اصلی", row_width=3, callback_data="back")
    )
    global LM
    LM = bot.send_message(message.chat.id, info_text, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "info")
def info(call):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton("بازگشت", row_width=3, callback_data="back")
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=info_text,
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda call: call.data == "back")
def main_menu_back(call):
    newuser(call.message)

    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 4
    keyboard.add(types.InlineKeyboardButton("خرید", callback_data="buy"))
    keyboard.add(types.InlineKeyboardButton("راهنما", callback_data="info"))
    keyboard.add(types.InlineKeyboardButton(" کیف پول", callback_data="wallet"))
    keyboard.add(
        types.InlineKeyboardButton("پشتیبانی", url="t.me/The_erphwn"),
        types.InlineKeyboardButton("کانال ما", url="t.me/idcard1"),
    )

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=main_text,
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda call: call.data == "main_menu")
def main_menu(call):
    newuser(call.message)

    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 4
    keyboard.add(types.InlineKeyboardButton("خرید", callback_data="buy"))
    keyboard.add(types.InlineKeyboardButton("راهنما", callback_data="info"))
    keyboard.add(types.InlineKeyboardButton("کیف پول", callback_data="wallet"))
    keyboard.add(
        types.InlineKeyboardButton("پشتیبانی", url="t.me/The_erphwn"),
        types.InlineKeyboardButton("کانال ما", url="t.me/idcard1"),
    )

    global LM
    LM = bot.send_message(call.message.chat.id, main_text, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "buy")
def buy_menu(call):
    global package
    package = 0
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton("بازگشت", row_width=3, callback_data="back")
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="لطفاً تعداد اپل‌آیدی مورد نیاز را بنویسید:\n\n⚠️با کیبورد انگلیسی و به صورت عدد ارسال کنید",
        reply_markup=keyboard,
    )
    user_state[call.message.chat.id] = "enter_serial_count"


@bot.message_handler(
    func=lambda message: user_state.get(message.chat.id) == "enter_serial_count"
)
def enter_serial_count(message):
    global package
    keyboard = types.InlineKeyboardMarkup()
    if package == 0:
        if message.text.isdigit():
            package = int(message.text)
            bot.edit_message_reply_markup(
                message.chat.id, message.message_id - 1, None, None
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    "تایید", row_width=3, callback_data="serial_handle"
                ),
                types.InlineKeyboardButton("بازگشت", row_width=3, callback_data="buy"),
            )
            global LM
            LM = bot.send_message(
                message.chat.id,
                f"تعداد وارد شده : {package}\n\n",
                reply_markup=keyboard,
            )
        else:
            bot.send_message(
                message.chat.id, "لطفا با کیبورد انگلیسی و بدون کاما یا اسلش وارد کنید."
            )

    else:
        bot.delete_message(message.chat.id, message.message_id)


@bot.callback_query_handler(func=lambda call: call.data == "serial_handle")
def enter_pcs(call):
    newuser(call.message)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    check = len(df[df["User ID"].isna()].head(package + 1))
    keyboard = types.InlineKeyboardMarkup()
    keyboard_e = types.InlineKeyboardMarkup()
    msg = bot.send_message(
        call.message.chat.id,
        "در حال چک کردن موجودی...",
        reply_markup=keyboard_e,
    )
    time.sleep(1.5)

    if check < package:
        keyboard.add(
            types.InlineKeyboardButton(
                "بازگشت", row_width=3, column_width=1, callback_data="buy"
            )
        )
        bot.edit_message_text(
            chat_id=msg.chat.id,
            message_id=msg.message_id,
            text=f"عدم موجودی❌\nتعداد کمتری را انتخاب کنید یا با پشتیبانی درتماس باشید❗️\n تعداد موجودی حاضر {check} ",
            reply_markup=keyboard,
        )

    else:
        keyboard.add(
            types.InlineKeyboardButton(
                "ادامه", row_width=3, callback_data="PeymentMethod"
            ),
            types.InlineKeyboardButton("بازگشت", row_width=3, callback_data="buy"),
        )

        bot.edit_message_text(
            chat_id=msg.chat.id,
            message_id=msg.message_id,
            text="موجودی تایید شد✅",
            reply_markup=keyboard,
        )


@bot.callback_query_handler(func=lambda call: call.data == "PeymentMethod")
def peyment_methode(call):
    newuser(call.message)
    global package
    global cost
    global cost_curred
    cost = package * 50000
    cost_curred = "{:,}".format(cost)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 4
    keyboard.add(
        types.InlineKeyboardButton(
            f"موجودی : {balance_curred} تومان", callback_data="MOJODI"
        ),
        types.InlineKeyboardButton("برداشت از کیف پول", callback_data=f"C_KIFPOOL"),
    )
    keyboard.add(types.InlineKeyboardButton("کارت به کارت", callback_data=f"C_CARD"))
    keyboard.add(types.InlineKeyboardButton("بازکشت", callback_data="buy"))
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"تعداد درخواستی : {package} \n\n پرداختی:  {cost_curred} تومان \n\n روش پرداخت خود را انتخاب کنید.",
        reply_markup=keyboard,
    )
    user_state[call.message.chat.id] = "enter_serial_count"


@bot.callback_query_handler(func=lambda call: call.data == "wallet")
def wallet(call):
    newuser(call.message)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 4
    keyboard.add(
        types.InlineKeyboardButton(
            "شارژ کیف پول", row_width=3, callback_data=f"enter_wallet_R"
        )
    )
    keyboard.add(
        types.InlineKeyboardButton("بازگشت", row_width=3, callback_data="back")
    )
    LM = bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"\nشناسه کاربری : {user_id}\n\nموجودی کیف پول شما : {balance_curred} تومان \n\n.",
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda call: call.data == "enter_wallet_R")
def enter_wallet_R(call):
    global LM
    global newbalance
    newbalance = 0
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton("بازگشت", row_width=3, callback_data="wallet")
    )
    LM = bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=" لطفاً مقدار شارژ کیف پول رابنویسید: (تومان)\n\n⚠️با کیبورد انگلیسی و به صورت عدد ارسال کنید",
        reply_markup=keyboard,
    )
    user_state[call.message.chat.id] = "WalletCharge_h"


@bot.message_handler(
    func=lambda message: user_state.get(message.chat.id) == "WalletCharge_h"
)
def handle_Charge(message):
    global newbalance
    global curred
    global LM

    keyboard = types.InlineKeyboardMarkup()
    if newbalance == 0:
        if message.text.isdigit():
            newbalance = int(message.text)
            curred = "{:,}".format(newbalance)
            bot.edit_message_reply_markup(LM.chat.id, LM.message_id, None, None)
            keyboard.add(
                types.InlineKeyboardButton(
                    "بله", row_width=3, callback_data="WalletCharge"
                ),
                types.InlineKeyboardButton(
                    "خیر", row_width=3, callback_data=f"enter_wallet_R"
                ),
            )
            LM = bot.send_message(
                message.chat.id,
                f" مقدار وارد شده : {curred} تومان\nآیا از عدد وارد شده اطمینان دارید ؟",
                reply_markup=keyboard,
            )
        else:
            bot.send_message(
                message.chat.id, "لطفا به عدد و بدون کاما یا اسلش وارد کنید."
            )
    else:
        bot.delete_message(message.chat.id, message.message_id)


@bot.callback_query_handler(func=lambda call: call.data == "WalletCharge")
def walletCharge(call):

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton("بازگشت", row_width=3, callback_data="wallet")
    )
    CardNumber = "6104–3374-8868-2178 \nدهقانی-ملت"
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"<b>میزان شارژ درخواست شده : {curred} تومان\n\nلطفا پس از انتقال هزینه به شماره کارت \n\n<code>{CardNumber}</code>\n\n رسید آن را ارسال کنید\n\n تصویر رسید مورد تایید است . .</b>",
        parse_mode="HTML",
        reply_markup=keyboard,
    )
    user_state[call.message.chat.id] = "waiting_for_approve_charge"


@bot.message_handler(
    content_types=["photo"],
    func=lambda message: user_state.get(message.chat.id)
    == "waiting_for_approve_charge",
)
def handle_payment_proof(message):
    newuser(message)
    time_EX = JalaliDateTime.now().strftime("%y/%m/%d | %H:%M:%S")
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            "تایید",
            callback_data=f"J_approve,{message.chat.id},{message.message_id},{newbalance}",
        ),
        types.InlineKeyboardButton(
            "رد",
            callback_data=f"J_reject,{message.chat.id},{message.message_id},{newbalance}",
        ),
    )
    global LM
    LM = bot.send_message(
        message.chat.id,
        "تصویر پرداختی برای ادمین ارسال شد . لطفا تا تایید مدیر منتظر بمانید.",
    )
    global f_u
    f_u = ""
    f_u = ubank.loc[ubank["User ID"] == message.chat.id]

    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(
        ADMIN_ID,
        f"WALLET CHARGE REQUEST\n\n User ID : \n\n {message.chat.id} \n\n Requested Charge :\n\n {curred}T\n\n Time : {time_EX} ",
    )
    bot.send_message(ADMIN_ID, "آیا تراکنش را تایید می‌کنید؟", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith("J_"))
def handle_admin_Charge_decision(call):
    action, chat_id, message_id, nb = call.data.split(",")
    if action == "J_approve":
        bot.edit_message_reply_markup(ADMIN_ID, call.message.message_id, None, None)
        bot.edit_message_text(
            chat_id=ADMIN_ID,
            message_id=call.message.message_id,
            text="تراکنش تایید شد.",
        )

        print(chat_id)
        ubank.loc[f_u.index, "Balance"] += int(nb)
        currednb = "{:,}".format(int(nb))
        save_excel()
        global LM
        LM = bot.send_message(
            chat_id,
            f"پرداخت توسط مدیر تایید شد و مقدار {currednb} تومان به کیف پول شما اضافه شد. برای شروع مجدد دستور /start را ارسال کنید",
            reply_to_message_id=message_id,
        )

    elif action == "J_reject":
        bot.edit_message_reply_markup(ADMIN_ID, call.message.message_id, None, None)
        bot.edit_message_text(
            chat_id=ADMIN_ID,
            message_id=call.message.message_id,
            text="تراکنش رد شد.",
        )
        LM = bot.send_message(
            chat_id,
            "تراکنش شما توسط مدیر رد شد. لطفا با پشتیبانی در ارتباط باشید.",
            reply_to_message_id=message_id,
        )


@bot.callback_query_handler(func=lambda call: call.data == "MOJODI")
def show_MSG(call):
    newuser(call.message)
    bot.answer_callback_query(
        call.id, f"موجودی کیف پول شما  {balance_curred} تومان است.", show_alert=True
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("C_"))
def handle_buy_choice(call):
    newuser(call.message)
    global package

    action = call.data
    if action == "C_CARD":
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                "بازگشت", row_width=3, callback_data="PeymentMethod"
            )
        )
        CardNumber = "6104–3374-8868-2178 \nدهقانی-ملت"
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"<b>تعداد درخواستی : {package}\n\nهزینه : {cost_curred} تومان \n\nلطفا پس از انتقال هزینه به شماره کارت \n\n<code>{CardNumber}</code>\n\n  رسید آن را ارسال کنید.\n\n تصویر رسید مورد تایید است </b>",
            parse_mode="HTML",
            reply_markup=keyboard,
        )
        user_state[call.message.chat.id] = "waiting_for_payment_proof"
    elif action == "C_KIFPOOL":
        if balance >= cost:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(
                types.InlineKeyboardButton(
                    "انصراف", row_width=3, callback_data="PeymentMethod"
                ),
                types.InlineKeyboardButton(
                    "پرداخت",
                    row_width=3,
                    callback_data=f"t_approve_kifpool,{call.message.chat.id},{call.message.message_id}",
                ),
            )
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"برداشت {cost_curred} از کیف پول برای خرید {package} اپل ایدی\n\n.",
                reply_markup=keyboard,
            )

        else:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(
                types.InlineKeyboardButton(
                    "شارژ کیف پول", row_width=3, callback_data="wallet"
                ),
                types.InlineKeyboardButton(
                    "بازگشت", row_width=3, callback_data="PeymentMethod"
                ),
            )
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="موجودی کیف پول برای خرید کافی نیست. لطفا از منوی اصلی کیف پول خود را شارژ کنید.",
                reply_markup=keyboard,
            )


@bot.message_handler(
    content_types=["photo"],
    func=lambda message: user_state.get(message.chat.id) == "waiting_for_payment_proof",
)
def handle_payment_proof(message):
    newuser(message)
    time_EX = JalaliDateTime.now().strftime("%y/%m/%d | %H:%M:%S")
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            "تایید", callback_data=f"t_approve,{message.chat.id},{message.message_id}"
        ),
        types.InlineKeyboardButton(
            "رد", callback_data=f"t_reject,{message.chat.id},{message.message_id}"
        ),
    )
    global LM
    LM = bot.send_message(
        message.chat.id, "تصویر پرداختی ارسال شد . لطفا تا تایید مدیر منتظر بمانید."
    )
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(
        ADMIN_ID,
        f"NEW TRANSFER \n\n User ID : \n\n   {message.chat.id} \n\n Amount Of AppleID's : \n\n {package} Cost : \n\n {cost_curred} \n\n Time : \n\n {time_EX} \n\n . ",
    )
    bot.send_message(ADMIN_ID, "آیا تراکنش را تایید می‌کنید؟", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith("t_"))
def handle_admin_decision(call):
    newuser(call.message)
    action, chat_id, message_id = call.data.split(",")
    print(user_id)
    emptys = df[df["User ID"].isna()].head(package)
    if action == "t_approve":
        bot.edit_message_reply_markup(ADMIN_ID, call.message.message_id, None, None)
        bot.edit_message_text(
            chat_id=ADMIN_ID,
            message_id=call.message.message_id,
            text="تراکنش تایید شد.",
        )
        time_EX = JalaliDateTime.now().strftime("%y/%m/%d | %H:%M:%S")
        bot.send_message(
            ADMIN_ID,
            f"گزارش خرید🟢 \n\n\n  {time_EX} \n\n تعداد 🔢:\n {package} \n\nروش پرداخت :کارت به کارت\n\n ایدی کاربر خریدار 👤: \n {chat_id} \n\n.",
        )
        global LM
        LM = bot.send_message(
            chat_id, "تراکنش شما توسط مدیر تایید شد.", reply_to_message_id=message_id
        )
        last_column_index = df.shape[0]
        find_user_excel = ubank.loc[ubank["User ID"] == user_id]
        ubank.loc[find_user_excel.index, "Total Amount"] += package
        message = ""
        i = 1
        for index, row in emptys.iterrows():
            df.at[index, "User ID"] = user_id
            df.at[index, "BuyDate"] = time_EX
            save_excel()

            message = ""
            message += f"-----------{i}-----------\n"
            i += 1
            message += f"Apple ID 🆔:\n{row.iloc[0]}\n\n"
            message += f"Password 🔐:\n{row.iloc[1]}\n\n"
            message += f"Birthday Date 📅:\n {row.iloc[2]}\n\n"
            message += "Security Questions❓:\n\n"
            message += f"Q1️⃣:best friend at teenager?\n\n{row.iloc[3]}\n\n"
            message += f"Q2️⃣:dream job?\n\n{row.iloc[4]}\n\n"
            message += f"Q3️⃣:parents meet?\n\n{row.iloc[5]}\n\n"
            LM = bot.send_message(chat_id, message, reply_to_message_id=message_id)

        LM = bot.send_message(
            chat_id,
            "برای دسترسی به پنل دستور /start را ارسال کنید.",
            reply_to_message_id=message_id,
        )
        save_excel()

    elif action == "t_approve_kifpool":
        time_EX = JalaliDateTime.now().strftime("%y/%m/%d | %H:%M:%S")
        bot.send_message(
            ADMIN_ID,
            f"گزارش خرید🟢 \n\n\n  {time_EX} \n\n تعداد 🔢:\n {package} \n\nروش پرداخت :کیف پول\n\n ایدی کاربر خریدار 👤: \n {chat_id} \n\n.",
        )
        find_user_excel = ubank.loc[ubank["User ID"] == user_id]
        ubank.loc[find_user_excel.index, "Balance"] -= cost
        # balance = balance_row["Balance"].iloc[0]
        ubank.loc[find_user_excel.index, "Total Amount"] += package
        save_excel()

        message = ""
        i = 1
        for index, row in emptys.iterrows():
            df.at[index, "User ID"] = user_id
            df.at[index, "BuyDate"] = time_EX

            save_excel()
            message = ""
            message += f"-----------{i}-----------\n"
            i += 1
            message += f"Apple ID 🆔:\n{row.iloc[0]}\n\n"
            message += f"Password 🔐:\n{row.iloc[1]}\n\n"
            message += f"Birthday Date 📅:\n {row.iloc[2]}\n\n"
            message += "Security Questions❓:\n\n"
            message += f"Q1️⃣:best friend at teenager?\n\n{row.iloc[3]}\n\n"
            message += f"Q2️⃣:dream job?\n\n{row.iloc[4]}\n\n"
            message += f"Q3️⃣:parents meet?\n\n{row.iloc[5]}\n\n"
            LM = bot.send_message(chat_id, message, reply_to_message_id=message_id)

        newuser(call.message)

        keyboard = types.InlineKeyboardMarkup()
        keyboard.row_width = 4
        keyboard.add(types.InlineKeyboardButton("خرید", callback_data="buy"))
        keyboard.add(types.InlineKeyboardButton("راهنما", callback_data="info"))
        keyboard.add(types.InlineKeyboardButton("کیف پول", callback_data="wallet"))
        keyboard.add(
            types.InlineKeyboardButton("پشتیبانی", url="t.me/The_erphwn"),
            types.InlineKeyboardButton("کانال ما", url="t.me/idcard1"),
        )

        LM = bot.send_message(chat_id, main_text, reply_markup=keyboard)

    else:
        bot.edit_message_reply_markup(ADMIN_ID, call.message.message_id, None, None)
        bot.edit_message_text(
            chat_id=ADMIN_ID,
            message_id=call.message.message_id,
            text="تراکنش رد شد.",
        )
        LM = bot.send_message(
            chat_id, "تراکنش شما توسط مدیر رد شد.", reply_to_message_id=message_id
        )
        save_excel()

        newuser(call.message)

        keyboard = types.InlineKeyboardMarkup()
        keyboard.row_width = 4
        keyboard.add(types.InlineKeyboardButton("خرید", callback_data="buy"))
        keyboard.add(types.InlineKeyboardButton("راهنما", callback_data="info"))
        keyboard.add(types.InlineKeyboardButton("کیف پول", callback_data="wallet"))
        keyboard.add(
            types.InlineKeyboardButton("پشتیبانی", url="t.me/The_erphwn"),
            types.InlineKeyboardButton("کانال ما", url="t.me/idcard1"),
        )

        LM = bot.send_message(chat_id, main_text, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "back")
def back(call):
    newuser(call.message)
    print("Back")
    main_menu_back(call)
    user_state[call.message.chat.id] = "main_text_menu"


def save_excel():
    df.to_excel("idcard.xlsx", index=False)
    ubank.to_excel(user_excel, index=False)


bot.infinity_polling()
