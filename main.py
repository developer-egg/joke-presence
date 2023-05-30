from jokeapi import Jokes
from pypresence import Presence
import asyncio
import time

client_id = "1112892105598177310"
RPC = Presence(client_id)
RPC.connect()


async def get_joke():
    joke_class = await Jokes()
    joke = await joke_class.get_joke(
        blacklist=["nsfw", "religious", "sexist", "political", "racist"]
    )

    if joke["type"] == "single":
        return joke["joke"]
    else:
        return (joke["setup"], joke["delivery"])


while True:

    def update_status(joke):
        joke = asyncio.run(get_joke())

        buttons = [
            {
                "label": "View Source Code",
                "url": "https://github.com/developer-egg/joke-presence",
            }
        ]

        image = "https://funny-presence.netlify.app/icon.png"

        try:
            if type(joke) == tuple:
                RPC.update(
                    details=f"{joke[0]}",
                    state=f"{joke[1]}",
                    buttons=buttons,
                    small_image=image
                )
            elif type(joke) == str:
                RPC.update(details=f"{joke}", buttons=buttons, small_image=image)
        except:
            joke = asyncio.run(get_joke())
            update_status(joke)

    joke = asyncio.run(get_joke())
    update_status(joke)

    time.sleep(3600)
