import telebot
from telebot import types
import pandas as pd
import random
# Load your Excel file
excel_file = 'idcard.xlsx'
df = pd.read_excel(excel_file)

# Initialize your bot with your bot token
bot = telebot.TeleBot("6859321838:AAHvDUPgTtFYkWqVUchvk5Gt3_hEVMT46wE")

# Dictionary to store user's current state
user_state = {}

package = 0 
# Dictionary to store pending payments awaiting confirmation
pending_payments = {}
# Administrator's user ID
ADMIN_ID = 1200237209 
user_id= 0



@bot.message_handler(commands=['start'])
def start(message):
    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("خرید", callback_data="buy"),
                 types.InlineKeyboardButton("پشتیبانی", callback_data="support"),
                 types.InlineKeyboardButton("کانال ما",url="t.me/pllusin")
                                  )
    bot.send_message(message.chat.id, "لطفاً یک گزینه را انتخاب کنید:", reply_markup=keyboard)
    user_state[message.chat.id] = 'main_menu'
    global user_id 
    user_id = message.chat.id
    
@bot.callback_query_handler(func=lambda call: call.data == "back")  
def main_menu_back(call) :
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("خرید", callback_data="buy"),
                 types.InlineKeyboardButton("پشتیبانی", callback_data="support"),
                 types.InlineKeyboardButton("کانال ما",url="t.me/pllusin")
                                  )
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="لطفاً یک گزینه را انتخاب کنید:", reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call: call.data == "main_menu")  
def main_menu(call) :
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("خرید", callback_data="buy"),
                 types.InlineKeyboardButton("پشتیبانی", callback_data="support"),
                 types.InlineKeyboardButton("کانال ما",url="t.me/pllusin")
                                  )
    bot.send_message(call.message.chat.id,"لطفاً یک گزینه را انتخاب کنید:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "buy")
def buy_menu(call):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
                 types.InlineKeyboardButton("بازگشت", row_width=3 , callback_data='back')
                 )
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="لطفاً تعداد مورد نظر را بنویسید:", reply_markup=keyboard)
    user_state[call.message.chat.id]="enter_serial_count"
    

@bot.message_handler(func=lambda message: user_state.get(message.chat.id) == "enter_serial_count")
def enter_pcs(message):
    print ("enter_")
    global package 
    package = int(message.text)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("بله", row_width=3, callback_data="Continue"),
                 types.InlineKeyboardButton("خیر",row_width=3,callback_data="back"))
    bot.send_message(message.chat.id,"آیا از عدد وارد شده اطمینان دارید ؟", reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call: call.data == "Continue")
def handle_buy_choice(call):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
                 types.InlineKeyboardButton("انصراف", row_width=3 , callback_data='back')
                 )
    global package
    cost= package * 25000
    CardNumber = "6280-2313-2337-4552"

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= f"<b>پک انتخاب شده : {package}\nهزینه : {cost}\nلطفا پس از انتقال هزینه به شماره کارت \n\n<code>{CardNumber}</code>\n\n رسید آن را ارسال کنید.</b>",parse_mode="HTML",reply_markup=keyboard)
    user_state[call.message.chat.id] = 'waiting_for_payment_proof'
  

@bot.message_handler(content_types=['photo'], func=lambda message: user_state.get(message.chat.id) == 'waiting_for_payment_proof')
def handle_payment_proof(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("تایید", callback_data=f't_approve,{message.chat.id},{message.message_id}'),
                 types.InlineKeyboardButton("رد", callback_data=f't_reject,{message.chat.id},{message.message_id}'))
    bot.send_message(message.chat.id,"تصویر پرداختی ارسال شد . لطفا تا تایید مدیر منتظر بمانید.")
    bot.send_message(ADMIN_ID, "تصویر پرداختی ارسال شده است. لطفاً تصویر را بررسی کنید و تصمیم خود را اعلام کنید.")
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(ADMIN_ID, "آیا تراکنش را تایید می‌کنید؟", reply_markup=keyboard)



@bot.callback_query_handler(func=lambda call: call.data.startswith('t_'))
def handle_admin_decision(call):
    action, chat_id, message_id = call.data.split(',')
    print(user_id)
    bot.delete_message(chat_id=ADMIN_ID,message_id=call.message.message_id)
    if action == 't_approve':
        global confirmed_id
        confirmed_id = user_id
        if (confirmed_id == user_id) :
            num = package
            rows = df.head(num)
            message = ''
            global index
            for index, row in rows.iterrows():
                message += "---------------------\n"
                for col, value in row.items():
                    message += f'{value}\n'
                        
            message += "---------------------\n"
            
            bot.send_message(chat_id, message , reply_to_message_id=message_id)
                # Remove sent rows from DataFrame (assuming index is unique identifier)
            df.drop(rows.index, inplace=True)
            df.reset_index(drop=True, inplace=True)
            bot.send_message(chat_id, "تراکنش شما توسط مدیر تایید شد." ,reply_to_message_id=message_id)
            
            main_menu(call)

    else:
        bot.send_message(chat_id, "تراکنش شما توسط مدیر رد شد." ,reply_to_message_id=message_id)
        main_menu(call)

@bot.callback_query_handler(func=lambda call: call.data == "back")
def back(call):
    print("Back")
    main_menu_back(call)
    user_state[call.message.chat.id] = 'main_menu'
    
    
    
    
bot.polling()
