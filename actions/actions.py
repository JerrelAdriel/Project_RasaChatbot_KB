import sqlite3
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet



class ActionSimpanNama(Action):

    def name(self) -> Text:
        return "action_simpan_nama"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        connect = sqlite3.connect('db_rasa.db')

        prediction = tracker.latest_message
        entity = prediction['entities']
        nama = ""

        for x in entity:
            if x['entity'] == 'nama':
                nama = x['value']

        mycursor = connect.cursor()

        sql = "INSERT INTO tb_user (nama) VALUES (?)"
        mycursor.execute(sql, (nama,))
        connect.commit()

        dispatcher.utter_message(template="utter_submit")

        return []

class ActionAmbilNama(Action):

    def name(self) -> Text:
        return "action_ambil_nama"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        connect = sqlite3.connect('db_rasa.db')

        mycursor = connect.cursor()
        mycursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tb_user'")
        
        if (len(mycursor.fetchall()) == 0):
            mycursor.execute("CREATE TABLE tb_user (nama text)")
            connect.commit()

        mycursor.execute("SELECT nama FROM tb_user")
        myresult = mycursor.fetchall()
        nama = "".join(myresult[-1])

        dispatcher.utter_message(
            template="utter_user_nama",
            nama=nama
        )

        return []


