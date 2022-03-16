from telegram.ext import Updater, CommandHandler, MessageHandler, Filters



def setup_and_run_bot(commands, token, port, app_url, logger, ip="0.0.0.0"):
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    
    # Add the commands
    for key, cmd in commands.items():
        dp.add_handler(CommandHandler(key, lambda update, context, c=cmd: update.message.reply_text(c())))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(
        Filters.text,
        lambda update, context: update.message.reply_text('Gib ein Kommando ein, um mit dem Bot zu interagieren')
    ))

    # log all errors
    dp.add_error_handler(
        lambda update, context: logger.warning('Update "%s" caused error "%s"', update, context.error)
    )

    # Start the Bot
    #updater.start_polling() # Use if local
    updater.start_webhook(listen=ip,
                          port=int(port),
                          url_path=token)
    updater.bot.setWebhook(app_url + token)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


def test(commands):
    """ This does check if the commands run without exception be thrown """
    errors = 0
    
    for key, handler in commands.items():
        try:
            handler()
            print("SUCCESS with command '{}':".format(key))
        except:
            print("ERROR with command '{}'".format(key))
            errors += 1
        
    print("Finishing with {} errors".format(errors))
    
