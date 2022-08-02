from re import I
import telegram
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os


telegram_bot_token = os.environ.get('TOKEN')

updater = Updater(
    token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher

# Welcome message


def welcome(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_photo(
        chat_id=chat_id, photo=open('./Images/welcome.jpg', 'rb'))


# Method for generating the RDJ meme
def generate_rdj(update, context):
    # Grab the user message
    msg = update.message.text
    chat_id = update.effective_chat.id
    img = Image.open('./Images/template.jpg')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('./Fonts/arial.ttf', 40)
    msg_len = len(msg)
    # Determine wether multiple lines are needed or not
    if msg_len < 21:
        text_size = font.getsize(msg)
        # Draw text on the picture using pillow
        draw.text((240 - text_size[0]/2, 194 - text_size[1]),
                  msg, (0, 0, 0), font=font)
        # Image is saved with chat_id as name to guarantee uniqueneness
        img.save(f'{chat_id}.jpg')
        # Send picture to the user
        context.bot.send_photo(
            chat_id=chat_id, photo=open(f'{chat_id}.jpg', 'rb'))
        # Remove picture from server
        os.remove(f'{chat_id}.jpg')
    else:
        # Split the message on blanks
        strings = msg.split(' ')
        # Reset message before reconstruction
        msg = ''
        # Counter for characters per line
        count = 0
        # Counter for lines in message
        lines = 2
        for index, item in enumerate(strings):
            if len(item) > 20:
                strings.insert(index + 1, item[20:])
                strings[index] = item[:20] + '-'
            # If line surpasses 20 characters when adding the next word, add a newline,
            # then the word and set count to the amount of characters in word
            if count + len(strings[index]) > 20:
                count = len(strings[index]) + 1
                msg = msg + '\n' + strings[index]
                lines += 1
            # Otherwise add characters in word  and blank space to current line and count
            else:
                count += len(item) + 1
                msg = msg + ' ' + strings[index]
        # Only return an image if theres less than 10 lines
        if lines < 10:
            text_size_line = font.getsize(msg[:20])
            text_height = 180 if text_size_line[1]*(lines -
                                                    2) > 194 else text_size_line[1]*(lines - 2)
            draw.text((240 - text_size_line[0]/2, 194 - text_height),
                      msg, (0, 0, 0), font=font, align='center')
            img.save(f'{chat_id}.jpg')
            context.bot.send_photo(
                chat_id=chat_id, photo=open(f'{chat_id}.jpg', 'rb'))
            os.remove(f'{chat_id}.jpg')
        else:
            context.bot.send_message(
                chat_id=chat_id, text='Your message is too long.')


# Runs the wolcome function when user starts the bot
dispatcher.add_handler(CommandHandler("start", welcome))

# Use generate_rdj method for any message thats not a command
dispatcher.add_handler(MessageHandler(Filters.text, generate_rdj))
updater.start_polling()
updater.idle()
