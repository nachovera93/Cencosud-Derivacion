import datetime
from datetime import date, timedelta
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, ActionExecuted, EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import SlotSet
from rasa_sdk.events import Restarted
from rasa_sdk.events import AllSlotsReset
import pymysql
global SiPaga
global NoPaga
global motivo
global tipo_contacto
global compromiso_p
global derivacion
global fecha_com
global entrega_info
SiPaga=None
NoPaga=None
motivo=None
tipo_contacto=0
compromiso_p=0
derivacion=None
fecha_com=None
entrega_info=None


import requests
import json
#url = "http://172.16.1.72/webservice-php-json/index.php"

url = "http://45.228.211.133:8080/webservice-php-json/index.php"


def Querys(uniqueid):
        payload={'action': 'get','id': f'{uniqueid}'}
        files=[
        ]
        headers = {}
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        my_bytes_value = response.content
        my_new_string = my_bytes_value.decode("utf-8").replace("'", '"')
        data = json.loads(my_new_string)
        s = json.dumps(data, indent=4, sort_keys=True)
        print(s)
        global nombre
        global monto
        global fechaVencimiento
        global primernombre
        global rut
        global campania
        nombre=data["data"][0]["address1"]
        monto=data["data"][0]["address2"]
        fechaVencimiento=data["data"][0]["city"]
        primernombre=data["data"][0]["first_name"]
        rut=data["data"][0]["vendor_lead_code"]
        campania=data["data"][0]["campaign_name"]

"""
            "address1": "DANIELA HERNANDEZ",
            "address2": "26799",
            "campaign_name": "CLICK RECORDATORIO",
            "city": "28-02-21",
            "email": "",
            "first_name": "DANIELA",
            "lead_id": "134",
            "list_name": "CLICK RECORDATORIO",
            "owner": "78574270",
            "vendor_lead_code": "170099999"
"""

def Updates(tipo_contacto,motivo,compromiso_p,derivacion,fecha_com,entrega_info,lead_id,rut):
          payload={'action': 'update',
          'tipo_contacto': f'{tipo_contacto}',
          'motivo': f'{motivo}',
          'compromiso_p': f'{compromiso_p}',
          'derivacion': f'{derivacion}',
          'fecha_com': f'{fecha_com}',
          'entrega_info': f'{entrega_info}',
          'lead_id': f'{lead_id}',
          'rut': f'{rut}'}
          files=[
          ]
          headers = {}
          response = requests.request("POST", url, headers=headers, data=payload, files=files)
          print(response.text)


def month_converter(i):
       month = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
       return month[i-1]


def ConverterDate():
     global mes
     global dia
     global anio
     global nombreMes 
     dia=int(fechaVencimiento[0:2])
     mes=int(fechaVencimiento[3:5])
     anio=int(fechaVencimiento[6:10])
     nombreMes=month_converter(mes)
     print("dia: ",dia)
     print("mes: ",nombreMes)
     print("a??o: ",anio)


class ActionHello(Action):
    def name(self):
        return "action_hello"

    def run(self, dispatcher, tracker, domain):
        #database = DataBase()
        global uniqueid
        uniqueid = tracker.sender_id
        Querys(uniqueid)
        Updates(7,motivo,compromiso_p,derivacion,fecha_com,"No",uniqueid,rut)
        t = datetime.datetime.now()
        if 23 >= int(t.hour) >= 12:
             dispatcher.utter_message(f'Buenas tardes, mi nombre es Gertrudis, ??Me comunico con {nombre}?')
        else:
             dispatcher.utter_message(f'Buenos d??as, mi nombre es Gertrudis, ??Me comunico con {nombre}?')
           
           
        return []
           


class ActionHello2(Action):
    def name(self):
        return "action_hello2"

    def run(self, dispatcher, tracker, domain):
        #database = DataBase()
        global uniqueid
        uniqueid = tracker.sender_id
        #print("uniqueid: ", tracker.sender_id)
        Querys(uniqueid)
        Updates(7,motivo,compromiso_p,derivacion,fecha_com,"No",uniqueid,rut)
        dispatcher.utter_message(f'Me comunico con {primernombre}?')
        return []


###########################################################
################### Pregunta Principal ####################
###########################################################

class ActionQuestion(Action):
    def name(self):
        return "action_ask_question"

    def run(self, dispatcher, tracker, domain):
        #database = DataBase()
        global uniqueid
        uniqueid = tracker.sender_id
        Querys(uniqueid)
        Updates(1,motivo,compromiso_p,derivacion,fecha_com,"No",uniqueid,rut)
        ConverterDate()
        dispatcher.utter_message(f'{nombre}, estamos llamando de SICC por encargo de cencosud para entregarle informaci??n especial para usted. ??Desea comunicarse con un ejecutivo para saber m??s?') 
        Updates(2,motivo,compromiso_p,derivacion,fecha_com,"Si",uniqueid,rut)
           
        return []
       
################################################
################### Si paga ####################
################################################

class ActionSiPaga(Action):
    def name(self):
        return "action_si_paga"

    def run(self, dispatcher, tracker, domain):
        #database = DataBase()
        global uniqueid
        uniqueid = tracker.sender_id
        Querys(uniqueid)
        dispatcher.utter_message(f"{primernombre}, para una mejor atenci??n por favor ingrese su rut. si termina en K, reempl??cela por un cero. | DER")
       
        return []


################################################
################### No paga ####################
################################################

class ActionNoPaga(Action):
    def name(self):
        return "action_no_paga"

    def run(self, dispatcher, tracker, domain):
        #database = DataBase()
        global uniqueid
        uniqueid = tracker.sender_id
        Querys(uniqueid)
        motivo = tracker.get_slot("razon")
        Updates(4,motivo,4,derivacion,fecha_com,"Si",uniqueid,rut)
        dispatcher.utter_message(f"Muchas gracias por su tiempo {primernombre}. Para m??s informaci??n puede ingresar a triple doble b punto sicc punto cl o llamando al 223658000. Que tenga un lindo d??a! | EXIT")#{primernombre}
        return []


################################################
################# Action Contactar #############
################################################

class ActionContact(Action):
    def name(self):
        return "action_contactar"

    def run(self, dispatcher, tracker, domain):
        #database = DataBase()
        global uniqueid
        uniqueid = tracker.sender_id
        dispatcher.utter_message(f'Muchas gracias, lo estar?? contactando uno de nuestros Ejecutivos | EXIT')
        Querys(uniqueid)
        #TipoContacto(uniqueid)
        #if (tipo_contact=="3"):
        Updates(3,motivo,3,"Si",fecha_com,"Si",uniqueid,rut)
        #elif(tipo_contact=="4"):
        #    progreso(4,razon,None,"Si",fecha_com,"Si",uniqueid)
        #else:
        #    print("Nada")
        return []


################################################
################# Action Despedida #############
################################################

class ActionGetGoodBye(Action):
    def name(self):
        return "action_despedida"

    def run(self, dispatcher, tracker, domain):
        #database = DataBase()
        global uniqueid
        uniqueid = tracker.sender_id
        dispatcher.utter_message(f'Muchas gracias por su tiempo, que tenga un buen d??a | EXIT')
        Querys(uniqueid)
        #if (tipo_contact=="3"):
        Updates(3,motivo,3,"No",fecha_com,"Si",uniqueid,rut)
        #elif (tipo_contact=="4"):
        #    progreso(4,razon,4,"No",fecha_com,"Si",uniqueid)
        #else:
        #    print("Nada")
        return []




#####################################
############ Action Si Conoce ##########
#####################################
 
class ActionConoce0(Action):
    def name(self):
        return "action_conoce"

    def run(self, dispatcher, tracker, domain):
        #database = DataBase()
        global uniqueid
        uniqueid = tracker.sender_id
        Querys(uniqueid)
        dispatcher.utter_message(f'Disculpe, usted conoce a {nombre}?')
        return []


class ActionSiConoce(Action):
    def name(self):
        return "action_si_conoce"

    def run(self, dispatcher, tracker, domain):
        #database = DataBase()
        global uniqueid
        uniqueid = tracker.sender_id
        Querys(uniqueid)
        Updates(5,motivo,compromiso_p,derivacion,fecha_com,entrega_info,uniqueid,rut)
        dispatcher.utter_message(f'Podr??a comentarle que tenemos informaci??n importante y que nos puede encontrar en triple doble b punto sic punto cl o llamando al 223658000. Gracias | EXIT')
        Updates(6,motivo,compromiso_p,derivacion,fecha_com,"Si",uniqueid,rut)
        return []


###############################################
################### Restart ###################
###############################################

class ActionRestart2(Action):
    """Resets the tracker to its initial state.
    Utters the restart template if available."""

    def name(self) -> Text:
        return "action_restart2"

    async def run(self, dispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [Restarted()]

class ActionSlotReset(Action):  
    def name(self):         
        return 'action_slot_reset'  
    def run(self, dispatcher, tracker, domain):
        return[AllSlotsReset()]


##########################
########## Final #########
##########################
class Final(Action):
    def name(self):   
        return "action_final"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #database.close()
        dispatcher.utter_message("Exit")
        return []


###############################
####### Preguntas Usuario #####
###############################

class ActionConoce(Action):
    def name(self):
        return "action_quien"

    def run(self, dispatcher, tracker, domain):
        
        global uniqueid
        uniqueid = tracker.sender_id
        Querys(uniqueid)
        dispatcher.utter_message(f'Me comunico con {nombre}?')
        return []

class ActionDonde(Action):
    def name(self):
        return "action_donde"

    def run(self, dispatcher, tracker, domain):
        global uniqueid
        uniqueid = tracker.sender_id
        Querys(uniqueid)
        dispatcher.utter_message(f'Nos estamos comunicando de SICC por encargo de cencosud')
        return []

class ActionDonde2(Action):
    def name(self):
        return "action_donde2"

    def run(self, dispatcher, tracker, domain):
        global uniqueid
        uniqueid = tracker.sender_id
        Querys(uniqueid)
        dispatcher.utter_message(f'Estamos llamando de SICC por encargo de cencosud')
        return []





######################################
###### Action Guardar Slots ##########
######################################

global conoce_o_no
class ActionGuardarConoce(Action):

    def name(self) -> Text:
        return "action_guardar_conoce_o_no"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        conoce_o_no = tracker.get_slot("conoce_o_no")
        if tracker.get_slot("conoce_o_no") is None:
            print("Es None ..")
        print("conoce_o_no: ", conoce_o_no)
            #dispatcher.utter_message(text=f"Raz??n: {Raz??n}")
        return []


global es_o_no
class ActionRecibirEsoNo(Action):

    def name(self) -> Text:
        return "action_recibir_es_o_no"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
       
        es_o_no = tracker.get_slot("es_o_no")
        print("es_o_no: ", es_o_no)
            #dispatcher.utter_message(text=f"Raz??n: {Raz??n}")
        return []

global pagar??_o_no
class ActionRecibirPagaoNo(Action):

    def name(self) -> Text:
        return "action_recibir_paga_o_no"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
       
        pagar??_o_no = tracker.get_slot("pagar??_o_no")
        print("pagar??_o_no: ", pagar??_o_no)
            #dispatcher.utter_message(text=f"Raz??n: {Raz??n}")
        return []

class ActionRecibirAutorizaoNo(Action):

    def name(self) -> Text:
        return "action_guardar_raz??n"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        motivo = tracker.get_slot("razon")
        print("motivo: ", motivo)
            #dispatcher.utter_message(text=f"Raz??n: {Raz??n}")
        return []


####################
##### Dar Hora #####
####################
class ActionDarHora(Action):
    def name(self):   
        return "action_dar_hora"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        t = datetime.datetime.now()
        global uniqueid
        uniqueid = tracker.sender_id
        Querys(uniqueid)
        dispatcher.utter_message(text=f"{primernombre}, son las {t.hour} {t.minute} Horas")

        return []
###########################
#### Questions 2 y 3 ######
###########################
class ActionQuestion2(Action):
    def name(self):
        return "action_ask_question2"

    def run(self, dispatcher, tracker, domain):
     
       dispatcher.utter_message(f'Disculpe le har?? la pregunta nuevamente')
       return []

class ActionQuestion3(Action):
    def name(self):
        return "action_ask_question3"

    def run(self, dispatcher, tracker, domain):
       dispatcher.utter_message(f'Disculpe comencemos desde el principio')
       return []


