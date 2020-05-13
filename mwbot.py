import discord
import requests
from discord.ext import commands
import json


bot = commands.Bot(command_prefix='!')

client = discord.Client()
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def usage(ctx):
    await ctx.send('Type *\"!stats <player> <br/mp>\"* for ingame stats,\nor type *\"!matches <player> <br/mp>\"* for the 5 most recent matches.' +
                    '\n**In the <player> section, you need to type in your BattleTag**, for example: Dpara#2643')

Xsrf_token_URL = 'https://profile.callofduty.com/cod/login'
Auth_URL = 'https://profile.callofduty.com/do_login?new_SiteId=cod'
s = requests.Session()

r = s.get(Xsrf_token_URL)
xsrf_token = r.cookies['XSRF-TOKEN']
payload = {'username': 'EMAIL_HERE', 'password': 'PASSWORD_HERE',
               'remember_me':'true', '_csrf': xsrf_token}

r = s.post(Auth_URL, data=payload)
print('Authenticated successfully!')

@bot.command()
async def stats(ctx,playername,mode):
    x = playername.replace("#","%23")

    Stats_URL = 'https://my.callofduty.com/api/papi-client/stats/cod/v1/title/mw/platform/battle/gamer/' + x + '/profile/type/mp'

    r = s.get(Stats_URL)
    jsonResponse = r.json()
    
    brprop = jsonResponse['data']['lifetime']['mode']['br']['properties']
    mpprop = jsonResponse['data']['lifetime']['all']['properties']
    if mode=='br':
        await ctx.send('**The stats for ' + playername + '\'s Warzone matches are:\n\nGames played: **' + str(int(brprop['gamesPlayed'])) + '\n**Games won: **' + str(int(brprop['wins']))
                            +'\n**Top 5\'s: **' + str(int(brprop['topFive'])) + '\n**Top 10\'s: **'+ str(int(brprop['topTen'])) +'\n\n**Kills: **' + str(int(brprop['kills']))
                            +'\n**Downs: **'+ str(int(brprop['downs'])) + '\n**Contracts completed: **' + str(int(brprop['contracts'])))
    elif mode =='mp':
        await ctx.send('**The stats for ' + playername + '\'s Multiplayer matches are:**\n\n**Total Games Played: **' + str(int(mpprop['totalGamesPlayed'])) +
                         '\n**Wins: **' + str(int(mpprop['wins'])) + '\n**Win/Loss Ratio: **' + str(round(mpprop['winLossRatio'],2)) + '\n\n**Kills: **' + str(int(mpprop['kills'])) +
                         '\n**KDR: **' + str(round(mpprop['kdRatio'],2)) + '\n**Most Kills: **' + str(int(mpprop['bestKills'])) + '\n**Best Killstreak: **' + str(int(mpprop['recordKillStreak']))) 
        if mpprop['kdRatio'] < 1:
            await ctx.send('\n__**You could improve on your KDR :)**__')

    else :
        await ctx.send('**Error:** Did you type in the mode correctly? It\'s **br** or **mp**')
    return

@bot.command()
async def matches(ctx,playername,mode):
    x = playername.replace("#","%23")
    conv = mode.replace('br','warzone')
    Matches_URL = 'https://my.callofduty.com/api/papi-client/crm/cod/v2/title/mw/platform/battle/gamer/' + x +'/matches/'+ conv +'/start/0/end/0/details' 

    r = s.get(Matches_URL)
    jsonResponse = r.json()

    data = jsonResponse['data']['matches']

    if mode=='br':
        await ctx.send('**5 Most recent Warzone matches: **\n\n' +
                        '**1.- Placement: **' + str(int(data[0]['playerStats']['teamPlacement'])) + '\n      **Kills: **' + str(int(data[0]['playerStats']['kills'])) +
                            '\n      **Damage done: **' + str(int(data[0]['playerStats']['damageDone'])) +
                            '\n      **Total time survived: **' + str(int(round(data[0]['playerStats']['teamSurvivalTime']/60000, 0))) + ' Minutes    ' +
                            '\n      **Moving Percent: **' + str(int(data[0]['playerStats']['percentTimeMoving'])) + '%' +
                        '**\n\n2.- Placement: **' + str(int(data[1]['playerStats']['teamPlacement'])) + '\n      **Kills: **' + str(int(data[1]['playerStats']['kills'])) +
                            '\n      **Damage done: **' + str(int(data[1]['playerStats']['damageDone'])) +
                            '\n      **Total time survived: **' + str(int(round(data[1]['playerStats']['teamSurvivalTime']/60000, 0))) + ' Minutes    ' +
                            '\n      **Moving Percent: **' + str(int(data[1]['playerStats']['percentTimeMoving'])) + '%' +
                        '**\n\n3.- Placement: **' + str(int(data[2]['playerStats']['teamPlacement'])) + '\n      **Kills: **' + str(int(data[2]['playerStats']['kills'])) +
                            '\n      **Damage done: **' + str(int(data[2]['playerStats']['damageDone'])) +
                            '\n      **Total time survived: **' + str(int(round(data[2]['playerStats']['teamSurvivalTime']/60000, 0))) + ' Minutes    ' +
                            '\n      **Moving Percent: **' + str(int(data[2]['playerStats']['percentTimeMoving'])) + '%' +
                        '**\n\n4.- Placement: **' + str(int(data[3]['playerStats']['teamPlacement'])) + '\n      **Kills: **' + str(int(data[3]['playerStats']['kills'])) +
                            '\n      **Damage done: **' + str(int(data[3]['playerStats']['damageDone'])) +
                            '\n      **Total time survived: **' + str(int(round(data[3]['playerStats']['teamSurvivalTime']/60000, 0))) + ' Minutes    ' +
                            '\n      **Moving Percent: **' + str(int(data[3]['playerStats']['percentTimeMoving'])) + '%' +
                        '**\n\n5.- Placement: **' + str(int(data[4]['playerStats']['teamPlacement'])) + '\n      **Kills: **' + str(int(data[4]['playerStats']['kills'])) +
                            '\n      **Damage done: **' + str(int(data[4]['playerStats']['damageDone'])) +
                            '\n      **Total time survived: **' + str(int(round(data[4]['playerStats']['teamSurvivalTime']/60000, 0))) + ' Minutes    ' +
                            '\n      **Moving Percent: **' + str(int(data[4]['playerStats']['percentTimeMoving'])) + '%')
        
    elif mode =='mp':
        await ctx.send('**5 Most recent Multiplayer matches:**\n' +
                        '\n**1.- **' + str(data[0]['map'].replace("mp_", "").capitalize()) + ' - ' + str(data[0]['result'].capitalize()) + ' - Kills: ' + str(data[0]['playerStats']['kills']) +
                        '\n**2.- **' + str(data[1]['map'].replace("mp_", "").capitalize()) + ' - ' + str(data[1]['result'].capitalize()) + ' - Kills: ' + str(data[1]['playerStats']['kills']) +
                        '\n**3.- **' + str(data[2]['map'].replace("mp_", "").capitalize()) + ' - ' + str(data[2]['result'].capitalize()) + ' - Kills: ' + str(data[2]['playerStats']['kills']) +
                        '\n**4.- **' + str(data[3]['map'].replace("mp_", "").capitalize()) + ' - ' + str(data[3]['result'].capitalize()) + ' - Kills: ' + str(data[3]['playerStats']['kills']) +
                        '\n**4.- **' + str(data[0]['map'].replace("mp_", "").capitalize()) + ' - ' + str(data[4]['result'].capitalize()) + ' - Kills: ' + str(data[4]['playerStats']['kills']) +
                        '\n**5.- **' + str(data[0]['map'].replace("mp_", "").capitalize()) + ' - ' + str(data[5]['result'].capitalize()) + ' - Kills: ' + str(data[5]['playerStats']['kills']))

    else :
        await ctx.send('**Error:** Did you type in the mode correctly? It\'s **br** or **mp**')
    return

bot.run('BOT TOKEN HERE')
