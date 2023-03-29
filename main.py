from  pyrogram import Client, filters, enums 
from pyrogram.errors import UserNotParticipant , FloodWait,InputUserDeactivated , UserIsBlocked , PeerIdInvalid
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle 
from  pymongo import MongoClient
import asyncio 
from time import sleep 
import datetime 

Token = '6177218989:AAGYrK5j38uIQJERMjgCW10h-OWe9naJu0c'


api_id =18802415 ; api_hash = "a8993f96404fd9a67de867586b3ddc92" ; bot_token = Token 

mongodb = "mongodb+srv://yeceta5252:8TfvIab7FZv4B2xQ@cluster0.nzk72k3.mongodb.net/?retryWrites=true&w=majority"

"buttons"
channel = InlineKeyboardButton("Channel🌴",url='https://t.me/neuralp')
group = InlineKeyboardButton("Group🪺",url='https://t.me/neuralg')
pro= InlineKeyboardButton("One of the Students from HRU",url="https://t.me/hrufn15")
feedback = InlineKeyboardButton("Subscribe Premium🍿",url='https://t.me/e_phador')
help = InlineKeyboardButton("Help📃",callback_data='help')
mark = InlineKeyboardMarkup([[InlineKeyboardButton("🥬Team Freshman 🌽",url = "https://t.me/hrufn15")]])   

app = Client ("gr",api_id=api_id,api_hash=api_hash, bot_token=bot_token)
cli = MongoClient(mongodb); db = cli.database; cuser = db.cuser ; cadmin = db.cadmin

frce = {"status":"off"}
admins = [] ; admi = cadmin.find({}) 
for guy in admi :
    admins.append(guy['admins'])
    

@app.on_message(filters.private & filters.command("set") )
def set(bot, msg):
    id = msg.text.replace("/set","")
    prp = msg.from_user.first_name 
    vals = {"admins":int(id),"promoted":prp}
    cadmin.insert_one(vals)
    cut = cadmin.find_one({"admins":int(id)})
    bot.send_message(int(id),f"you have promoted to admin by {prp}")
    msg.reply("Promoting New Admin Done🦊")
        
@app.on_message( filters.private & filters.command("users")) 
def users(bot, msg):
    usr = cuser.find()
    c = len(list(usr))
    msg.reply(f"**we have {c} users at this moment🦝**")
    

@app.on_message(filters.private & filters.command("cast") & filters.user(admins))
async def cast(bot,msg):
    txt = msg.text
    block = " ."
    idinvalid  = " ."
    dec = " ."
    mesg = txt.replace('/cast',"")
    for user in cuser.find():
        try :
            await bot.send_message(user['userid'],mesg , reply_markup=mark)
        except UserIsBlocked:
            block+=f"{user['userid']} : {user['name']} :  @{user['username']}\n"
        except InputUserDeactivated:
            dec+=f"{user['userid']} : {user['name']} : {user['username']}"
        except PeerIdInvalid:
            idinvalid+=f" {user['userid']} : {user['name']} : {user['username']}"
        except FloodWait:
            await asyncio.sleep(e.x)     
   
        except Exception as error:
          await msg.reply(error)
    await msg.reply(f"cast logs\n\nBlocked User \n{block} \n Invalid Ids \n {idinvalid} Deactivated\n {dec}")  
        
   
@app.on_message( filters.command("msg") & filters.user(admins))    
async def  messe(bot,msg):
    try :
        text = msg.copy(msg.text)
        ruid = text.split(" ")[1]
        mesgt = text.replace('/msg',"").replace(ruid,'')
        await bot.send_message(int(ruid), f"{mesgt}\n\n\n **cartx CEO**",reply_markup=mark) 
        await msg.reply("your message sent successfully")
        
    except Exception as error:
        await msg.reply(f"not sent\n{error} ")   
        

@app.on_message(filters.command("force") & filters.user(admins))       
def force(bot , msg):
    st = frce['status']
    cr = msg.reply(f"**Current Force Join Status {st}🦊**")
    tos = msg.text.split(" ")[1]
    frce["status"] = tos
    sleep(10)
    cr.edit(f"**Current Force Join Set to {st}🦊**")
@app.on_callback_query() 
async def call(bot,msg):
    await msg.message.reply("**Just send your full name and you should have to be from Hru Section 15 **")
    
    
@app.on_message(filters.private & filters.command("start"))
async def start(bot, msg):
  
    name = msg.from_user.first_name 
    userid = msg.from_user.id
    username = msg.from_user.username  
    exs = cuser.find_one({'userid':userid})
    user = {"name":name,"userid":userid,"username":username, "date":datetime.datetime.now()}
    if not exs :
      cuser.insert_one(user)
    else:
      pass
    markup = InlineKeyboardMarkup([[channel, group], [help],[pro]])
    await msg.reply(f"**Hello {username} this is F+ Channel__(the kanged version of the A+ Tutorial Paid private Channel )__ registration Bot\n\nalso Check out our [AI Question Answering Bot](t.me/chatgtp_probot)**",
    reply_markup= markup ,disable_web_page_preview = True)    
    
    
@app.on_message(filters.private & filters.text)
async def incom (bot, msg):
    if frce['status'] == 'on' :
        try :
            await bot.get_chat_member(-1001776406696 ,msg.from_user.id)
        except UserNotParticipant:
            await msg.reply("**Sorry i can't help you a lot on this ,Join the channel before our meeting**",
            reply_markup = InlineKeyboardMarkup([[channel]]))
            return
    else :
        pass 
    await bot.send_message(-1001835962707,msg.text)
    w = msg.text.split(" ")
    if  len(w) < 3 :
      await msg.reply("**Please Provide your Full name, including your grandpa😌**")
    else:
      link = await app.create_chat_invite_link(-1001634591367,name="free",member_limit=1)
      await msg.reply(link.invite_link,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Aquire Premium ", url="t.me/e_phador")]]),protect_content=True)


app.run()


