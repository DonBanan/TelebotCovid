import json
import requests
import telebot


bot = telebot.TeleBot('1177324969:AAEnpkLiA5CnGfK6ptgtdTad1v6gfQrdHRU')


@bot.message_handler(commands=['covid'])
def get_coronavirus_information(message):
    text = message.text[7:]
    with open('countries.json', 'r') as f:
        countries_dict = json.load(f)

    for country in countries_dict:
        if text == country['en_name'] or text == country['ru_name']:
            r = requests.get('https://corona.lmao.ninja/v2/countries/' + country['en_name'])
            response = r.json()

            bot.send_message(parse_mode='HTML',
                             chat_id=message.chat.id,
                             text="<b> Страна: " + response['country']
                                  + ".</b> \n Всего случайев: "
                                  + str(response['cases'])
                                  + "\n За сегодня случайев: "
                                  + str(response['todayCases'])
                                  + "\n Всего смертей: "
                                  + str(response['deaths'])
                                  + "\n За сегодня смертей: "
                                  + str(response['todayDeaths'])
                                  + "\n Выздоровевших: "
                                  + str(response['recovered'])
                                  + "\n Протестированных: "
                                  + str(response['tests'])
                             )


if __name__ == '__main__':
    bot.polling(none_stop=True)
