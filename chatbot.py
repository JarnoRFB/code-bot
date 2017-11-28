from chatterbot import ChatBot

bot = ChatBot(
    'Norman',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    input_adapter='chatterbot.input.TerminalAdapter',
    output_adapter='chatterbot.output.TerminalAdapter',
    # logic_adapters=[
    #     # 'chatterbot.logic.MathematicalEvaluation',
    #     # 'chatterbot.logic.TimeLogicAdapter'
    # ],
    database='./database.sqlite3',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

bot.train('chatterbot.corpus.english')

print('Hello!')
while True:
    try:
        bot_input = bot.get_response(None)
    except(KeyboardInterrupt, EOFError, SystemExit):
        break
