import discord
from discord.ext import commands
from discord.ui import Button, View

VERIFICATION_ROLE = "Viewer"

class VerifyButton(View):
    def __init__(self):
        super().__init__()
        self.add_item(Button(label="Verify", style=discord.ButtonStyle.green, custom_id="verify_button"))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        guild = interaction.guild
        role = discord.utils.get(guild.roles, name=VERIFICATION_ROLE)

        if role is None:
            await interaction.response.send_message("Verification role not found. Please create a role named 'Viewer'.", ephemeral=True)
            return False
        
        if role in interaction.user.roles:
            await interaction.response.send_message("You are already verified!", ephemeral=True)
            return False
        
        if not interaction.guild.me.guild_permissions.manage_roles:
            await interaction.response.send_message("I don't have permission to manage roles.", ephemeral=True)
            return False
        
        if interaction.guild.me.top_role <= role:
            await interaction.response.send_message("I cannot assign the 'Viewer' role as it is above my role in the role hierarchy.", ephemeral=True)
            return False
        
        try:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"{interaction.user.mention}, you have been verified!", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to add roles.", ephemeral=True)
            return False

        return True

class VerificationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def verify(self, ctx):
        """Command to send a verification button."""
        view = VerifyButton()
        await ctx.send("Click the button below to verify yourself:", view=view)

async def setup(bot):
    await bot.add_cog(VerificationCog(bot))
