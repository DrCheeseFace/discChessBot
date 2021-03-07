import discord
from discord.ext import commands
import asyncio
import chess
import requests 
import sys 
import io


bot = commands.Bot(command_prefix="+")
@bot.event
async def on_ready():
    print('Logged on as {0}!'.format(bot.user))

@bot.event
async def on_message(message):
    print('Message from {0.author}: {0.content}'.format(message))
    await bot.process_commands(message)    
    




@bot.command()
async def test(ctx,word):
    await ctx.send(word)
@bot.command()
async def play(ctx, member: discord.Member):
    msg = await ctx.send(f"React to this message {member.mention}!")
    await msg.add_reaction("👍")
    try:
        reaction, user = await bot.wait_for("reaction_add",timeout = 60.0 ,check = lambda reaction ,user: user.id == member.id and reaction.message.id == msg.id and str(reaction.emoji) == "👍")   
    except asyncio.TimeoutError:
        await ctx.send("too slow")
    else:
        await ctx.send("lets goooo")
        global white
        white = ctx.message.author.id
        global black
        black = member.id
        print(white,black)
        global board
        board = chess.Board()
        global moveList


        url = "http://www.fen-to-image.com/image/"+board.fen()
        url = url.split(" ",1)
        url = url[0]
        response = requests.get(url,verify=False)
        file=open("board.jpg","wb")
        file.write(response.content)
        file.close()
        with open("board.jpg","rb") as f:
            picture = discord.File(f)
            await ctx.send(file=picture)
        moveList = [] 
        legalMoves = ""
        for move in board.legal_moves:
            legalMoves+=str(move)+" "
            moveList.append(str(move))
        await ctx.send("possible moves: "+legalMoves)


@bot.command()
async def move(ctx,move):
    print(board.turn,"HIIII")
    moveList =[] 
    for possibleMove in board.legal_moves:
        moveList.append(str(possibleMove))
    
    if (board.turn == True and ctx.message.author.id == white)or (board.turn==False and ctx.message.author.id == black)  and move in moveList:
        
        pieceMove = chess.Move.from_uci(move)
        board.push(pieceMove)

        url = "http://www.fen-to-image.com/image/"+board.fen()
        url = url.split(" ",1)
        url = url[0]
        response = requests.get(url,verify=False)
        file=open("board.jpg","wb")
        file.write(response.content)
        file.close()
        with open("board.jpg","rb") as f:
            picture = discord.File(f)
            await ctx.send(file=picture)
        moveList = [] 
        legalMoves = ""
        for move in board.legal_moves:
            legalMoves+=str(move)+" "
            moveList.append(str(move))
        await ctx.send("possible moves: "+legalMoves)

        






bot.run('ODE3OTk0ODgxMjA1MDEwNDUz.YERnGQ.doHew8UupuIN9uvsyB5eFT9wnRc')

