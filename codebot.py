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


print('Hello! I am codebot. Please specify the path to the file you want me to help with.')
while True:
    try:
        bot_input = bot.get_response(None)
    except(KeyboardInterrupt, EOFError, SystemExit) as e:
        break
