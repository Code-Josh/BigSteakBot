async def cmd_nick(message, cmd):
    try:
        cmd_after = ''
        for cmd_a in cmd[1:]:
            cmd_after += ' ' + cmd_a
        cmd_after = cmd_after[1:]
        if cmd_after == '':
            await message.channel.send('Du muss hinter **"!nick"** deinen neuen nickname schreiben')
        else:
            await message.author.edit(nick=cmd_after)
            await message.channel.send('Dein nickname wurde erfolgreich zu **{0}** geändert'.format(cmd_after))
    except:
        await message.channel.send('Bei diesem Befehl entstand ein Fehler bitte kontaktiere den Server-Owner/Bot-Owner')