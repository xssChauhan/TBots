import telegram
import requests
from requests.auth import HTTPBasicAuth
import json

Telegramkey = '125312758:AAFYqMOW_jcoB7lLGNXN0YHtFThpolAzYIM'
NewsURL = 'https://api.datamarket.azure.com/Bing/Search/News?Query='
TranslateURL = 'https://api.datamarket.azure.com/Bing/MicrosoftTranslator/v1/Translate?Text='
NewsKey = '3+Rf+J35TdJOvBwVpdrwgLB/MSMgu9DibiX3kr6441g'
bot = telegram.Bot(Telegramkey)
langs = ['french', 'italian', 'german', 'klingon']
langCodes = ['fr','it','de','tlh']
ups = bot.getUpdates()
if len(ups):
	LAST_UPDATE_ID = ups[-1].update_id
else:
	LAST_UPDATE_ID = 0

class ResponseToJson():
	def __init__(self):
		pass
	def newsObj(self, string):
		response = dict()
		r = json.loads(string)
		r = r.values()[0]['results'][0]
		response['title'] = r['Title']
		response['url'] = r['Url']
		return response
	def translateObj(self, string):
		r = json.loads(string)
		return r.values()[0]['results'][0]['Text']

rtj = ResponseToJson()


while True:
	for update in bot.getUpdates(offset = LAST_UPDATE_ID, timeout = 10):
		text = update.message.text
		chat_id = update.message.chat_id
		update_id = update.update_id
		arg = text.split()[0]
		if arg == '/help':
			bot.sendMessage(chat_id = chat_id, text = 'Translation: french/italian/german Sentence to be translated \nNews : news Topic ')
		elif arg in langs:
			try:
				arg = langCodes[langs.index(arg)]
				message = '%20'.join(text.split()[1:])
				queryUrl = TranslateURL + '%27' + message + '%27&To=%27' + arg + '%27&$format=json'
				translation = requests.get(queryUrl, auth=HTTPBasicAuth('',NewsKey))
				translation = rtj.translateObj(translation.text)
				bot.sendMessage(chat_id = chat_id , text = translation)
			except Exception as e:
				print e
		elif arg == 'news':
			topic = '%20'.join([e for e in text.split()])
			try:
				queryURL = str(NewsURL+'%27'+str(topic)+'%27'+'&$top=1&$format=json')
				news = requests.get(queryURL,auth = HTTPBasicAuth('',NewsKey))
				news = rtj.newsObj(news.text)
				message = 'Title : %s \nURL : %s'%(news['title'], news['url'])
				bot.sendMessage(chat_id = chat_id, text = message)
			except Exception as e:
				print e
		else:
			bot.sendMessage(chat_id = chat_id, text = 'Please specify a Topic')
		LAST_UPDATE_ID = update_id + 1

if __name__ =='__main__':
	main()





