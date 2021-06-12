NAME = 'WWDC 2021 Videos'
ICON = 'icon-default.png'
WWDC_ROOT = 'https://developer.apple.com/videos/wwdc2021/'
# WWDC URL: https://developer.apple.com/videos/play/wwdc2021/10021/

def Start():
	ObjectContainer.title1 = NAME
	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8'

@handler('/video/wwdc', NAME, thumb=ICON)
def MainMenu():
	try:
		oc = ObjectContainer()
		html = HTML.ElementFromURL(WWDC_ROOT, cacheTime=CACHE_1DAY)
		for channel in html.xpath('//ul[contains(@class, "collection-items")]/li'):
			title = channel.xpath('.//img/@alt')[0]
			thumb = channel.xpath('.//img/@src')[0]
			summary = channel.xpath('.//p/text()')[0]
			video_path = channel.xpath('.//a/@href')[0]
			video_url = "https://developer.apple.com%s" % (video_path)
			oc.add(VideoClipObject(
				url = video_url,
				title = title,
				summary = summary,
				originally_available_at = None,
				thumb = Callback(Thumb, url=thumb)
			))
		return oc
	except Exception as ex:
		return ObjectContainer(header="Failure", message=ex)

@route('/video/wwdc/thumb')
def Thumb(url):
	try:
		data = HTTP.Request(url, cacheTime = CACHE_1MONTH).content
		return DataObject(data, 'image/jpeg')
	except:
		return Redirect(R(ICON))
