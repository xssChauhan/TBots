
import telegram , requests, json
from requests.auth import HTTPBasicAuth
Telegramkey = '125312758:AAFYqMOW_jcoB7lLGNXN0YHtFThpolAzYIM'
NewsURL = 'https://api.datamarket.azure.com/Bing/Search/News?Query='
NewsKey = '3+Rf+J35TdJOvBwVpdrwgLB/MSMgu9DibiX3kr6441g'
bot = telegram.Bot(Telegramkey)

LAST_UPDATE_ID = bot.getUpdates()[-1].update_id


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
rtj = ResponseToJson()
		
while True:
	for update in bot.getUpdates(offset = LAST_UPDATE_ID, timeout = 10):
		text = update.message.text
		chat_id = update.message.chat_id
		update_id = update.update_id

		if text:
			if len(text):
				if text.split()[0] == '/help':
					bot.sendMessage(chat_id = chat_id, text = 'Just Enter Your Search Term and get the top trending news about it')
				else:
					topic = '%20'.join([e for e in text.split()])
					try:
						queryURL = str(NewsURL+'%27'+str(topic)+'%27'+'&$top=1&$format=json')
						print queryURL
						news = requests.get(queryURL,auth = HTTPBasicAuth('',NewsKey))
						news = rtj.newsObj(news.text)
						print news
						message = 'Title : %s \nURL : %s'%(news['title'], news['url'])
						bot.sendMessage(chat_id = chat_id, text = message)
					except Exception as e:
						print e
			else:
				bot.sendMessage(chat_id = chat_id, text = 'Please specify a Topic')
			LAST_UPDATE_ID = update_id + 1



if __name__ == '__main__':
	main()