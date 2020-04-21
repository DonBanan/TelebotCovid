import json
import requests
import telebot


bot = telebot.TeleBot('')

OFFSET = 127462 - ord('A')


def flag(code):
    code = code.upper()
    return chr(ord(code[0]) + OFFSET) + chr(ord(code[1]) + OFFSET)


@bot.message_handler(commands=['help'])
def get_help(message):
    bot.send_message(parse_mode='HTML',
                     chat_id=message.chat.id,
                     text="<b>Все страны: /covid</b> \n<b>Конкретная страны: /covid country_name </b>")


@bot.message_handler(commands=['covid'])
def get_coronavirus_information(message):
    text = message.text[7:]
    if len(text) == 0:
        r = requests.get(
            'https://corona.lmao.ninja/v2/all')
        response = r.json()
        bot.send_message(parse_mode='HTML',
                         chat_id=message.chat.id,
                         text="Всего случайев: "
                              + str(response['cases'])
                              + "\n За сегодня случайев: "
                              + str(response['todayCases'])
                              + "\n Всего смертей: "
                              + str(response['deaths'])
                              + "\n За сегодня смертей: "
                              + str(response['todayDeaths'])
                              + "\n Выздоровевших: "
                              + str(response['recovered'])
                              + "\n Активных: "
                              + str(response['active'])
                              + "\n Критичных: "
                              + str(response['critical'])
                              + "\n Протестированных: "
                              + str(response['tests'])
                              + "\n Пострадавших стран: "
                              + str(response['affectedCountries'])
                         )
    else:
        with open('countries.json', 'r') as f:
            countries_dict = json.load(f)
        try:
            country = [obj for obj in countries_dict if text == obj['en_name'] or text == obj['ru_name']]
            r = requests.get(
                'https://corona.lmao.ninja/v2/countries/' + country[0]['en_name'])
            response = r.json()
            bot.send_message(parse_mode='HTML',
                             chat_id=message.chat.id,
                             text="<b> Страна: "
                                  + flag(response['countryInfo']['iso2'])
                                  + " " + text
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
        except:
            bot.send_message(message.chat.id, text="Такой страны нет в базе.")


if __name__ == '__main__':
    bot.polling(none_stop=True)
