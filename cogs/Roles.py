import discord
from discord.ext import commands

class ReactionRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_id = None 
        self.emoji_to_role = {
            "❄️": 1348099968057081999,
            "💧": 1348100076555341845,
            "🌹": 1348101568427458650,
            "🥀": 1348101629177757716,
            "🟪": 1348096446418911304,
            "🟨": 1348096400537288815,
            "⬛": 1348108379134103662,
            "🟫": 1348108531919753298,
        }

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == self.message_id:
            guild = self.bot.get_guild(payload.guild_id)
            if not guild:
                return

            role_id = self.emoji_to_role.get(str(payload.emoji))
            if role_id:
                role = guild.get_role(role_id)
                if role:
                    member = guild.get_member(payload.user_id)
                    if member:
                        await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == self.message_id:
            guild = self.bot.get_guild(payload.guild_id)
            if not guild:
                return

            role_id = self.emoji_to_role.get(str(payload.emoji))
            if role_id:
                role = guild.get_role(role_id)
                if role:
                    member = guild.get_member(payload.user_id)
                    if member:
                        await member.remove_roles(role)

    @commands.command()
    async def send_reaction_embed(self, ctx):
        embed = discord.Embed(
            title="︵‿︵‿୨ age ୧‿︵‿︵",
            description="‎\n❄️・18-\n💧・18+\n\nReact below to get your role!",
            color=discord.Color.blue(),
        )

        embed.set_footer(text="Choose your age group!")

        message = await ctx.send(embed=embed)
        await message.add_reaction("❄️")
        await message.add_reaction("💧")

        embed = discord.Embed(
            title="︵‿︵‿୨ Gender ୧‿︵‿︵",
            description="‎\n🌹・Male\n🥀・Female\n\nReact below to get your role!",
            color=discord.Color.blue(),
        )

        embed.set_footer(text="Gender!")

        message = await ctx.send(embed=embed)
        await message.add_reaction("🌹")
        await message.add_reaction("🥀")
        
        embed = discord.Embed(
            title="︵‿︵‿୨ Aura ୧‿︵‿︵",
            description="‎\n🟪・Rizzler\n🟨・Sigma\n\nReact below to get your role!",
            color=discord.Color.blue(),
        )

        embed.set_footer(text="Aura!")

        message = await ctx.send(embed=embed)
        await message.add_reaction("🟪")
        await message.add_reaction("🟨")
        
        embed = discord.Embed(
            title="︵‿︵‿୨ Updates ୧‿︵‿︵",
            description="‎\n🟫・Bot updates\n⬛・Server updates\n\nReact below to get your role!",
            color=discord.Color.blue(),
        )

        embed.set_footer(text="Pick the updates you want!")

        message = await ctx.send(embed=embed)
        await message.add_reaction("🟫")
        await message.add_reaction("⬛")

        self.message_id = message.id

async def setup(bot):
    await bot.add_cog(ReactionRole(bot))
