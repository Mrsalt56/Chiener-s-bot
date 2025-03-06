import discord
from discord.ext import commands
import yt_dlp
import asyncio
import logging

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

FFMPEG_OPTIONS = {'options': '-vn'}
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': True}

class Musicbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []

    @discord.app_commands.command(name="play", description="Play a song from YouTube")
    async def play(self, interaction: discord.Interaction, search: str):
        voice_channel = interaction.user.voice.channel if interaction.user.voice else None
        if not voice_channel:
            return await interaction.response.send_message("You're not in a voice channel!", ephemeral=True)

        if not interaction.guild.voice_client:
            await voice_channel.connect()

        await interaction.response.defer()
        
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(f"ytsearch:{search}", download=False)
            if 'entries' in info:
                info = info['entries'][0]
            url = info['url']
            title = info['title']
            self.queue.append((url, title))
            await interaction.followup.send(f'Added to queue: **{title}**')

        if not interaction.guild.voice_client.is_playing():
            await self.play_next(interaction)

    async def play_next(self, interaction: discord.Interaction):
        if self.queue:
            url, title = self.queue.pop(0)
            source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
            
            def after_playing(_):
                coro = self.play_next(interaction)
                fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
                try:
                    fut.result()
                except Exception as e:
                    print(f"Error in after function: {e}")

            interaction.guild.voice_client.play(source, after=after_playing)
            await interaction.followup.send(f'Now playing **{title}**')
        else:
            await interaction.followup.send("Queue is empty! Disconnecting...")
            await asyncio.sleep(5)
            if interaction.guild.voice_client:
                await interaction.guild.voice_client.disconnect()

    @discord.app_commands.command(name="skip", description="Skip the currently playing song")
    async def skip(self, interaction: discord.Interaction):
        if interaction.guild.voice_client and interaction.guild.voice_client.is_playing():
            interaction.guild.voice_client.stop()
            await interaction.response.send_message("Skipped")
        else:
            await interaction.response.send_message("Nothing is playing", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Musicbot(bot))

client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    await client.tree.sync()
    print(f'Logged in as {client.user}')

async def main():
    async with client:
        await client.add_cog(Musicbot(client))
        await client.start("MTM0MTYwMjg1MTAwODI4MjYyNA.G3B4m4.zm9JRSyz3HTaM61Y7R7gS4K-riIl-hj1d5Mo1w")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logging.info("Shutting down bot...")
    finally:
        loop.stop()
        loop.close()
