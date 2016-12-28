from lxml import html
import requests
import time
import datetime
from random import randint
from slackclient import SlackClient

SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL")
print SLACK_CHANNEL
# urls = ['https://www.ticketswap.com/event/nicolas-jaar/681833ee-39ed-457d-b9a0-682bece0bdc4', 'https://www.ticketswap.com/event/four-tet-floating-points-ade/099895ad-cd05-435b-b34b-c099f64c466d']
urls = ['https://www.ticketswap.com/event/nicolas-jaar/681833ee-39ed-457d-b9a0-682bece0bdc4']
queries = 0
sc = SlackClient(SLACK_TOKEN)
SLEEP_INTERVAL = 10
MAX_SLEEP = 600

def checkTickets(url):
  page = requests.get(url)
  tree = html.fromstring(page.content)
  buyers = tree.xpath('//div[@class="counter-value"]/text()')
  if len(buyers) > 0:
    result = int(buyers[0])
  else:
    result = 0
    time.sleep(MAX_SLEEP)
    notifyMe("They make me sleep boss :(")

  SLEEP_INTERVAL = randint(20, 36)
  time.sleep(SLEEP_INTERVAL)

  return result

def notifyMe(url):
  print "Bilet geldi abiii"
  sc.api_call(
  "chat.postMessage", channel=SLACK_CHANNEL, text=url,
  username='pybot', icon_emoji=':stuck_out_tongue_winking_eye:'
  )

while True:

  for u in urls:
    if checkTickets(u) > 0:
      notifyMe(u)

  SLEEP_INTERVAL *= 20
  queries += 1
  taym = datetime.datetime.now() + datetime.timedelta(seconds = SLEEP_INTERVAL)
  print "No tickets sir",queries,"th try and waking up at",taym.hour,":",taym.minute,"in",round(SLEEP_INTERVAL / 60.0, 2),"minutes..."
  time.sleep(SLEEP_INTERVAL)
