from lxml import html
import requests
import time
import datetime
from random import randint
from slackclient import SlackClient
import os

SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL")

urls = ['https://www.ticketswap.nl/event/cigarettes-after-sex/b3171998-7d0c-415a-9390-74ba51a3a38b']
queries = 0
sc = SlackClient(SLACK_TOKEN)
SLEEP_INTERVAL = 10
MAX_SLEEP = 2000

def checkTickets(url):
  page = requests.get(url)
  tree = html.fromstring(page.content)
  buyers = tree.xpath('//div[@class="counter-value"]/text()')
  if len(buyers) > 0:
    result = int(buyers[0])
  else:
    result = 0
    notifyMe("They make me sleep boss :( Tell that I'm not a robot.")
    time.sleep(MAX_SLEEP)

  return result

def notifyMe(text):
  sc.api_call(
  "chat.postMessage", channel=SLACK_CHANNEL, text=text,
  username='Sumeyye', icon_emoji=':relieved:'
  )

while True:

  for u in urls:
    if checkTickets(u) > 0:
      notifyMe("I FOUND A TICKET!!11!BIR!BIR1!! %s" % u)

  SLEEP_INTERVAL = randint(10, 16)*20
  queries += 1
  taym = datetime.datetime.now() + datetime.timedelta(seconds = SLEEP_INTERVAL)

  if (queries % 50 == 0 and queries > 0):
    notifyMe("Still no tickets sir... It's my %dth try, but I will try again at %d:%d in %.2f minutes. Don't worry we will find a ticket..." % (queries,taym.hour,taym.minute,SLEEP_INTERVAL/60.0))

  print "It's my %dth try, but I will try again at %d:%d in %.2f minutes. Don't worry we will find a ticket sir..." % (queries,taym.hour,taym.minute,SLEEP_INTERVAL/60.0)
  time.sleep(SLEEP_INTERVAL)
