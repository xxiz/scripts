import discord, os, requests

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

ntfy_id = os.environ['NTFY_ID']

def send_ntfy_message(url, chapter_number):
    requests.post("https://ntfy.sh/" + ntfy_id,
                  data=f"One Piece Chapter {chapter_number} Released @ {url}",
                  headers={
                      "Click": url,
                      "Title": f"One Piece Chapter {chapter_number} Release",
                      "Action": f"http, Open Link, {url}, clear=true"
                  })

def get_link_from_message(message):
    for word in message.content.split():
        if word.startswith("https://"):
            return word

def get_chapter_number_from_message(message):
    for word in message.content.split():
        if word.isdigit() and len(word) == 4:
            return word

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.channel.id == 1041159396518015088:
        if message.guild.id == "164970986284777473" and message.channel.id == "164975746144534529":
            if "Chapter" in message.content and "Release" in message.content and "@everyone" in message.content and "BREAK" in message.content and "NEXT" in message.content and "WEEK" in message.content:
                url = get_link_from_message(message)
                chapter_number = get_chapter_number_from_message(message)
                send_ntfy_message(url, chapter_number)

client.run(os.environ['DISCORD_TOKEN'])
