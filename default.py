import sys
import xbmcaddon
import xbmcgui
import xbmcplugin
import httplib
import json

class Channel:
    def __init__(self, name, chId):
        self.name = name
        self.channelId = chId


addon = xbmcaddon.Addon()
serverIp = addon.getSetting("ipaddress")
profile = addon.getSetting("profile")
port = addon.getSetting("ipport")

if not serverIp:
    xbmcgui.Dialog().ok("PCTV", "IP not defined, go to configure and put the IP Address!")
    exit()

if not profile:
    profile = "500k.MR"

if not port:
    port = 80


channels = []

try:
    h1 = httplib.HTTPConnection(serverIp, port=80, timeout=1)
    h1.connect()
    h1.request("GET", "/TVC/user/data/tv/channels")
    r1 = h1.getresponse()
    data = r1.read()
    items = json.loads(data, encoding='utf-8')

    for item in items:
        name = item["DisplayName"]
        id = item["Id"]
        channels.append(Channel(name, id))

    if len(channels) == 0:
        raise Exception('Not loaded')

    #sort items
    channels.sort(key=lambda x: x.name)
except:
    xbmcgui.Dialog().ok("PCTV", "Unable to load channels!")
    exit()

addon_handle = int(sys.argv[1])

xbmcplugin.setContent(addon_handle, 'movies')

for item in channels:
    url = 'http://{0}:{3}/TVC/Preview.m3u8?channel={1}&mode=m3u8&profile=m2ts.{2}'.format(serverIp, item.channelId, profile, port)
    li = xbmcgui.ListItem(item.name, iconImage='DefaultVideo.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

xbmcplugin.endOfDirectory(addon_handle)
