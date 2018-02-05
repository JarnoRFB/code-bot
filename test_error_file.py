"""dfsdfds
"""
from chatterbot import ChatBot

while True:
    BOT  =ChatBot


BOT = ChatBot (
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

BOT.train('chatterbot.corpus.english')

print('Hello!')
while True:
    try:
        bot_input = BOT.get_response(None)
    except(KeyboardInterrupt, EOFError, SystemExit):
        break
