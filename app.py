import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='/')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.command()
async def create_new_web_host(ctx):
    # Instructions for user
    await ctx.send('Please upload the zip file (max 50 MB).')

    # Check for file response
    def check(message):
        return message.author == ctx.author and message.attachments and message.attachments[0].size <= 52428800

    try:
        message = await bot.wait_for('message', check=check, timeout=300.0)  # Adjust timeout as needed
    except asyncio.TimeoutError:
        await ctx.send('Timeout reached. Please try the command again.')
        return

    if message.attachments[0].size > 52428800:
        await ctx.send('File size exceeds limit, please upload less than 50 MB.')
        return
    else:
        file_url = message.attachments[0].url
        await ctx.send('Please enter the site name.')

        # Check for site name response
        def check(m):
            return m.author == ctx.author

        try:
            site_name_message = await bot.wait_for('message', check=check, timeout=120.0)
            site_name = site_name_message.content
            # Here you would normally check if the subdomain is available and deploy to Netlify
            await ctx.send(f'Site name received: {site_name}. Proceeding with deployment...')
            # Implement deployment logic here...
        except asyncio.TimeoutError:
            await ctx.send('Timeout reached. Please try the command again.')

bot.run('YOUR_TOKEN')
