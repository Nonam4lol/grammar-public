import os
import discord
from discord.ext import commands
import language_tool_python
from dotenv import load_dotenv
import re
from googletrans import Translator

load_dotenv()
tool = language_tool_python.LanguageTool('en-US')

# Regular expression pattern for laughter and common expressions
laughter_pattern = re.compile(
    r'\b(?:[A-Za-z]*[Hh][Aa]+|[Pp][Ff]{3}[Tt]|(?:[Hh][Ee]+)?[Hh]a+Hh?|lol|rofl)\b'
)

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or('eg!'),
    help_command=None,
    intents=discord.Intents.all()
)

language_codes = {
    'af': 'Afrikaans',
    'sq': 'Albanian',
    'am': 'Amharic',
    'ar': 'Arabic',
    'hy': 'Armenian',
    'az': 'Azerbaijani',
    'eu': 'Basque',
    'be': 'Belarusian',
    'bn': 'Bengali',
    'bs': 'Bosnian',
    'bg': 'Bulgarian',
    'ca': 'Catalan',
    'ceb': 'Cebuano',
    'ny': 'Chichewa',
    'zh-cn': 'Chinese (Simplified)',
    'zh-tw': 'Chinese (Traditional)',
    'co': 'Corsican',
    'hr': 'Croatian',
    'cs': 'Czech',
    'da': 'Danish',
    'nl': 'Dutch',
    'en': 'English',
    'eo': 'Esperanto',
    'et': 'Estonian',
    'tl': 'Filipino',
    'fi': 'Finnish',
    'fr': 'French',
    'fy': 'Frisian',
    'gl': 'Galician',
    'ka': 'Georgian',
    'de': 'German',
    'el': 'Greek',
    'gu': 'Gujarati',
    'ht': 'Haitian Creole',
    'ha': 'Hausa',
    'haw': 'Hawaiian',
    'iw': 'Hebrew',
    'hi': 'Hindi',
    'hmn': 'Hmong',
    'hu': 'Hungarian',
    'is': 'Icelandic',
    'ig': 'Igbo',
    'id': 'Indonesian',
    'ga': 'Irish',
    'it': 'Italian',
    'ja': 'Japanese',
    'jw': 'Javanese',
    'kn': 'Kannada',
    'kk': 'Kazakh',
    'km': 'Khmer',
    'ko': 'Korean',
    'ku': 'Kurdish (Kurmanji)',
    'ky': 'Kyrgyz',
    'lo': 'Lao',
    'la': 'Latin',
    'lv': 'Latvian',
    'lt': 'Lithuanian',
    'lb': 'Luxembourgish',
    'mk': 'Macedonian',
    'mg': 'Malagasy',
    'ms': 'Malay',
    'ml': 'Malayalam',
    'mt': 'Maltese',
    'mi': 'Maori',
    'mr': 'Marathi',
    'mn': 'Mongolian',
    'my': 'Myanmar (Burmese)',
    'ne': 'Nepali',
    'no': 'Norwegian',
    'or': 'Odia',
    'ps': 'Pashto',
    'fa': 'Persian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'pa': 'Punjabi',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sm': 'Samoan',
    'gd': 'Scots Gaelic',
    'sr': 'Serbian',
    'st': 'Sesotho',
    'sn': 'Shona',
    'sd': 'Sindhi',
    'si': 'Sinhala',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'so': 'Somali',
    'es': 'Spanish',
    'su': 'Sundanese',
    'sw': 'Swahili',
    'sv': 'Swedish',
    'tg': 'Tajik',
    'ta': 'Tamil',
    'te': 'Telugu',
    'th': 'Thai',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'ug': 'Uyghur',
    'uz': 'Uzbek',
    'vi': 'Vietnamese',
    'cy': 'Welsh',
    'xh': 'Xhosa',
    'yi': 'Yiddish',
    'yo': 'Yoruba',
    'zu': 'Zulu'
}

@bot.command(name='help')
async def bot_help(ctx):
    """Display a list of available commands."""
    try:
        embed = discord.Embed(title="Bot Commands", description="Here are the commands you can use:", color=0x007bff)
        embed.add_field(name="eg!info", value="Display information about the bot.", inline=False)
        embed.add_field(name="eg!translate <message_id> <language>", value="Translate a message to a specified language.", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        print(f"Error in bot_help: {e}")

# ... rest of your code ...

@bot.command(name='info')
async def bot_info(ctx):
    """Display information about the bot."""
    try:
        # Calculate bot latency
        latency = round(bot.latency * 1000)  # Latency in milliseconds

        # Create an embed with bot information
        embed = discord.Embed(title=f"I am {bot.user.name}", description="Your friendly Grammar Police bot!", color=0x007bff)
        embed.add_field(name="Bot Latency", value=f"{latency}ms", inline=False)

        await ctx.send(embed=embed)
    except Exception as e:
        print(f"Error in bot_info: {e}")

@bot.command(name='translate')
async def translate(ctx, message_id: int = None, language: str = None):
    """Translate a message to a specified language."""
    try:
        if message_id is None or language is None:
            await ctx.send('Usage: eg!translate <message_id> <language>')
            return

        message = await ctx.channel.fetch_message(message_id)
        translator = Translator()
        detected = translator.detect(message.content)
        translation = translator.translate(message.content, dest=language)
        detected_language = language_codes.get(detected.lang, detected.lang)
        translated_language = language_codes.get(language, language)

        embed = discord.Embed(title="Translate", color=0x007bff)
        embed.add_field(name=f"*{detected_language}*", value=message.content, inline=False)
        embed.add_field(name=f"*{translated_language}*", value=translation.text, inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        print(f"Error in translate: {e}")
        await ctx.send("An error occurred while translating. Please try again.")

@bot.event
async def on_ready():
    try:
        print(f'{bot.user.name} has connected to Discord!')
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you"))
    except Exception as e:
        print(f"Error in on_ready: {e}")

@bot.event
async def on_message(message):
    try:
        if message.author == bot.user:
            return

        # Skip checking messages with laughter patterns
        if laughter_pattern.search(message.content):
            return

        # Skip grammar checking if the message starts with the command prefix
        prefixes = bot.command_prefix(bot, message)  # Get the list of prefixes
        for prefix in prefixes:
            if message.content.startswith(prefix):
                await bot.process_commands(message)
                return

        # Perform grammar checking
        matches = tool.check(message.content)
        if matches:
            corrected_message = message.content
            for match in reversed(matches):  # Iterate in reverse to avoid index issues
                corrected_message = corrected_message[:match.offset] + match.replacements[0] + corrected_message[match.offset + match.errorLength:]

            await message.channel.send(f'Did you mean: "{corrected_message}" ? || <@!{message.author.id}>')

        await bot.process_commands(message)
    except Exception as e:
        print(f"Error in on_message: {e}")

bot.run(os.getenv("DISCORD_TOKEN"))
