#!/usr/bin/env python3
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import sqlite3
import config

#variables globales
TIENDA=0
token=str(config.token)
#variables globales

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)
# Enable logging

LOCACION = range(1)
admin='ADMIN_ID'

##################################################33
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    update.message.reply_text('Bienvenido, tú ID es:')
    a= update.message.chat_id    
    update.message.reply_text(a)
    context.bot.send_message(chat_id=update.effective_chat.id,text=" Para más información de comandos disponibles usa */help* ", parse_mode='Markdown')
    context.bot.send_message(chat_id=update.effective_chat.id,text=" Para más información de comandos de administrador usa */helpadmin* ", parse_mode='Markdown')
def helpp(update, context):
    #"""Send a message when the command /help is issued."""
    update.message.reply_text('Comandos disponibles:')
    context.bot.send_message(chat_id=update.effective_chat.id,text=" */tienda [núm tienda]* Este comando es para consultar información básica de la tienda. ", parse_mode='Markdown')
    context.bot.send_message(chat_id=update.effective_chat.id,text=" */ubicaciontienda [núm tienda]* Este comando es para consultar link en GOOGLE MAPS de la tienda. ", parse_mode='Markdown')
def helpadmin(update, context):
    update.message.reply_text('Comandos disponibles:')
    context.bot.send_message(chat_id=update.effective_chat.id,text=" */editarmaps [núm tienda]* Este comando es para modificar Link de GOOGLE MAPS de la tienda. ", parse_mode='Markdown')
    context.bot.send_message(chat_id=update.effective_chat.id,text=" */cancel* Este comando es para cancelar comando", parse_mode='Markdown')
    
def error(update, context):
    #"""Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    
def comandobuscar(update, context):
    user_says = " ".join(context.args)
    val=0
    val2='x'
    try:
        val=int(user_says)
        val2=str(val)
        vector=consultar(val2)
        
        context.bot.send_message(chat_id=update.effective_chat.id,text=" *_Número Tienda:_* ", parse_mode='Markdown')
        update.message.reply_text(vector[1])#[1])# tienda
            #update.message.reply_text("Sucursal:")
        context.bot.send_message(chat_id=update.effective_chat.id,text=" *_Sucursal:_* ", parse_mode='Markdown')
        update.message.reply_text(vector[2])# sucursal
            #update.message.reply_text("Formato:")
        context.bot.send_message(chat_id=update.effective_chat.id,text=" *_Formato:_* ", parse_mode='Markdown')
        update.message.reply_text(vector[3])# Formato
            #update.message.reply_text("Estado:")
        context.bot.send_message(chat_id=update.effective_chat.id,text=" *_Estado:_* ", parse_mode='Markdown')
        update.message.reply_text(vector[4])# Estado
            #update.message.reply_text("Ciudad:")
        context.bot.send_message(chat_id=update.effective_chat.id,text=" *_Ciudad:_*", parse_mode='Markdown')
        update.message.reply_text(vector[5])# Ciudad
            #update.message.reply_text("Regional MTTO:")
        context.bot.send_message(chat_id=update.effective_chat.id,text=" *_Regional de MTTO:_* ", parse_mode='Markdown')
        update.message.reply_text(vector[6])# Regional
            #update.message.reply_text("DIRECCIÓN:")
        context.bot.send_message(chat_id=update.effective_chat.id,text=" *_Dirección:_* ", parse_mode='Markdown')
        update.message.reply_text(vector[7])# direccion
        
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id,text=" *Error en comando, vuelve a ingrearlo por favor. ", parse_mode='Markdown')
        context.bot.send_message(chat_id=update.effective_chat.id,text=" */tienda [núm tienda]* Este comando es para consultar información básica de la tienda. ", parse_mode='Markdown')
    return ()

def start_callback(update, context):
    user_says = " ".join(context.args)
    update.message.reply_text("You said: " + user_says)
    c=user_says
    print(user_says)    
    return()

def agregar(vector):
        dbrute= './SQLite_Python.db'
        try:
            sqliteConnection = sqlite3.connect(dbrute)
            cursor = sqliteConnection.cursor()
            print("Successfully Connected to SQLite")
            sqlite_insert_with_param = """INSERT INTO 'SqliteDb_developers'
                              ('id', 'tienda',
                              'sucursal', 'formato', 'estado',
                              'ciudad','regional_mtto','direccion','maps') 
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"""
            data_tuple = vector
            cursor.execute(sqlite_insert_with_param, data_tuple)
            sqliteConnection.commit()
            print("Python Variables inserted successfully into SqliteDb_developers table")
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to insert Python variable into sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")
        return()

def modificar(determinante,maps):
    
    dbrute= './SQLite_Python.db'
    try:
        sqliteConnection=sqlite3.connect(dbrute)
        cursor = sqliteConnection.cursor()
        update="""Update Tiendas set maps = ? where tienda = ?  """
        data=(maps,determinante)
        cursor.execute(update,data)
        sqliteConnection.commit()
        print("<<<<<<<<<<<<<<Record Updated successfully>>>>>>>>>>>")
        cursor.close
        
    except sqlite3.Error as error:
        print("Error, -----> ", error)
    finally:
        if(sqliteConnection):
            sqliteConnection.close()
            print("Cerrando conexión de Base de Datos")
    return()

def editartienda(update, context):
    user_says = " ".join(context.args)
    val=0
    administrador= int(update.message.chat_id)
    
    if administrador == admin:
    
        try:
            val=int(user_says)
            globals()['TIENDA']=user_says
            update.message.reply_text("INGRESAR LINK DE MAPS")# direccion
        except ValueError:
            update.message.reply_text("FAVOR DE INGRESAR NÚMERO VÁLIDO, ingrese comando nuevamente")
            context.bot.send_message(chat_id=update.effective_chat.id,text=" */editarmaps [núm tienda]* Este comando es para modificar Link de GOOGLE MAPS de la tienda. ", parse_mode='Markdown')
            return ConversationHandler.END
    else:
        update.message.reply_text("NO ERES ADMINISTRADOR")
        return()
        
    return "buscar"

def buscartienda (update, context):    
        print("buscandotienda")
        val = int(globals()['TIENDA'])
        text = update.message.text
        det=globals()['TIENDA']
        
        modificar(det,text)
        update.message.reply_text("A QUEDADO GUARDADA LA NUEVA LOCALIZACIÓN")# direccion
        print("listo")
        return ConversationHandler.END
    
def consultar(determinante):
    record='x'
    dbrute= './SQLite_Python.db'
    try:
        sqliteConnection=sqlite3.connect(dbrute)
        cursor = sqliteConnection.cursor()        
        SELECT="""SELECT * from Tiendas where tienda = ?  """
        cursor.execute(SELECT,(determinante,))        
        record=cursor.fetchone()
        print("Consulta  successfully")
        
        cursor.close
        
    except sqlite3.Error as error:
        
        print("Error, ALV -----> ", error)
    finally:
        if(sqliteConnection):
            sqliteConnection.close()
            print("Cerrando conexión de Base de Datos")
    return(record)

def comandoconsultar(update, context):
    user_says = " ".join(context.args)
    val=0
    try:
        val=int(user_says)
        buscarmaps(user_says,context,update)
    except ValueError:
        update.message.reply_text("FAVOR DE INGRESAR NÚMERO VÁLIDO, ingrese comando nuevamente")
        return ()
    
def buscarmaps (determinante,context,update):
    
    consulta=consultar(determinante)
    #print(consulta)
    context.bot.send_message(chat_id=update.effective_chat.id,text=" *_UNIDAD:_* ", parse_mode='Markdown')
    update.message.reply_text(consulta[1])
    context.bot.send_message(chat_id=update.effective_chat.id,text=" *_SUCURSAL:_* ", parse_mode='Markdown')
    update.message.reply_text(consulta[2])
    context.bot.send_message(chat_id=update.effective_chat.id,text=" *_LINK EN GOOGLE MAPS:_* ", parse_mode='Markdown')
    update.message.reply_text(consulta[8])
    return()


#Salir de la conversación con el BOT
def cancel (update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,text=" *_COMANDO CANCELADO:_* ", parse_mode='Markdown')
    return ConversationHandler.END

def main():
    #"""Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    
    ################
    #token para bot validado
    updater = Updater(token, use_context=True)
    #TOKENS DE BOTS
    #################
    
    #Get the dispatcher to register handlers
    dp = updater.dispatcher

    #on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helpp))
    dp.add_handler(CommandHandler("helpadmin", helpadmin))
    
    dp.add_handler(CommandHandler("tienda", comandobuscar))        
    dp.add_handler(CommandHandler("ubicaciontienda",comandoconsultar ))
    #on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text, echo)) 
  
    
##############
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('editarmaps', editartienda)],

            states={
                "buscar": [MessageHandler(Filters.text, buscartienda,pass_user_data=True)]
                
            },

            fallbacks=[CommandHandler('cancel', cancel)]
        )
    dp.add_handler(conv_handler)
##############

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
     # start_polling() is non-blocking and will stop the bot gracefully.
    updater.start_polling()


   
    updater.idle()


if __name__ == '__main__':
    print("Corriendo Script")
    main()
