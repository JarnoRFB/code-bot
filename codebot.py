from chatterbot import ChatBot

bot = ChatBot(
    'CodeBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    input_adapter='chatterbot.input.TerminalAdapter',
    output_adapter='chatterbot.output.TerminalAdapter',
    logic_adapters=[
        'adapters.PylintAdapter'
    ],
    database='./database.sqlite3',
)


print('Hello!')
while True:
    try:
        bot_input = bot.get_response(None)
    except(KeyboardInterrupt, EOFError, SystemExit) as e:
        print(e)
        break
