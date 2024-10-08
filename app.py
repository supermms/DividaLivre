import os
import logging
import json
from whatsapp import WhatsApp, Message
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from flask_session import Session
import database as db

from helpers import apology, login_required, admin_required

msg_limpanome = "O Limpa Nome é um serviço inovador especializado em suspender dívidas, oferecendo uma solução eficaz para quem está enfrentando dificuldades financeiras e precisa de uma oportunidade para recomeçar. \nNossa missão é ajudar nossos clientes a recuperar seu poder de compra e sua credibilidade no mercado, permitindo que voltem a sonhar e a planejar seu futuro sem o peso das dívidas. \nSe você está pronto para dar o primeiro passo em direção a uma vida financeira mais saudável e equilibrada, entre em contato conosco e descubra como o Limpa Nome pode ajudar você a suspender suas dívidas e a reconstruir seu futuro."
msg_como_funciona =  "Como Funciona? \n\nNosso processo é simples e transparente: \n\n*Análise Financeira Completa:* Avaliamos detalhadamente a situação financeira do cliente, identificando todas as dívidas e credores envolvidos. \n\nApós essa análise temos 2 opções de reabilitação de crédito: \n\n*Opção 1* \n\n*Negociação com Credores:* Atuamos como intermediários na negociação com os credores, buscando acordos que permitam a suspensão  das dívidas e a elaboração de um plano de pagamento viável. \n\n*Opção 2* \n\n*Liminar:* Um serviço completo em reabilitação de crédito, nos baseamos na lei 8.078 do códigos direito do consumidor, e com isso conseguimos uma Liminar obrigando os órgãos de proteção ao crédito ocultar as negativações existentes, permitindo que volte a trabalhar com seu CPF e CNPJ, sem a necessidade de pagar a dívida imediatamente, com seu crédito reabilitado novamente, pode negociar posteriormente a dívida com mais tranquilidade."

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Logging
logging.basicConfig(filename='whatsapplogs.log',
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Load .env file
load_dotenv("./.env")

# Access token for your WhatsApp business account app
whatsapp_token = os.getenv("TOKEN")

# Verify Token defined when configuring the webhook
VERIFY_TOKEN = "batmanbatman"

messenger = WhatsApp(os.getenv("TOKEN"),
                     phone_number_id=os.getenv("PHONE_NUMBER_ID"))

admin_credentials = json.loads(os.getenv("ADMIN_CREDENTIALS"))

def send_button_message_visitar_website(instance, mobile):
    instance.send_reply_button(
        recipient_id=mobile,
        button={
            "type": "button",
            "body": {
                "text": "Nosso website é: \n\n https://dividalivre.shop/ \n\n Nele você encontra diversas informações importantes."
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": "b1",
                            "title": "Como Funciona?"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "b2",
                            "title": "Falar com Consultor"
                        }
                    }
                ]
            }
      },
    )

def send_button_message_lead_contatou_primeiro(instance, mobile):
    instance.send_reply_button(
        recipient_id=mobile,
        button={
            "type": "button",
            "body": {
                "text": "Olá, obrigado por contatar o *DívidaLivre*!\n\n Somos uma empresa especializada em suspensão de dívidas, oferecendo uma solução eficaz para quem está enfrentando dificuldades financeiras e precisa de uma oportunidade para recomeçar. \n\nNossa missão é ajudar nossos clientes a recuperar seu poder de compra e sua credibilidade no mercado, permitindo que voltem a sonhar e a planejar seu futuro sem o peso das dívidas. \n\nSe você está pronto para dar o primeiro passo em direção a uma vida financeira mais saudável e equilibrada, entre em contato conosco e descubra como o Limpa Nome pode ajudar você a suspender suas dívidas e a reconstruir seu futuro."
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": "b1",
                            "title": "Como Funciona?"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "b2",
                            "title": "Visitar Website"
                        }
                    }
                    {
                        "type": "reply",
                        "reply": {
                            "id": "b3",
                            "title": "Falar com Consultor"
                        }
                    }
                ]
            }
      },
    )


def send_button_message_como_funciona(instance, mobile):
    instance.send_reply_button(
        recipient_id=mobile,
        button={
            "type": "button",
            "body": {
                "text": msg_como_funciona
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": "b1",
                            "title": "Visitar Website"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "b2",
                            "title": "Falar com Consultor"
                        }
                    }
                ]
            }
      },
    )

def send_button_message_quero_saber(instance, mobile):
    instance.send_reply_button(
        recipient_id=mobile,
        button={
            "type": "button",
            "body": {
                "text": msg_limpanome
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": "b1",
                            "title": "Como Funciona?"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "b2",
                            "title": "Falar com Consultor"
                        }
                    }
                ]
            }
      },
    )


# Required webhook verifictaion for WhatsApp
# info on verification request payload:
# https://developers.facebook.com/docs/graph-api/webhooks/getting-started#verification-requests
def verify(request):

    # Parse params from the webhook verification request
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    # Check if a token and mode were sent
    if mode and token:
        # Check the mode and token sent are correct
        if mode == "subscribe" and token == VERIFY_TOKEN:
            # Respond with 200 OK and challenge token from the request
            print("WEBHOOK_VERIFIED")
            return challenge, 200
        else:
            # Responds with '403 Forbidden' if verify tokens do not match
            print("VERIFICATION_FAILED")
            return jsonify({"status": "error", "message": "Verification failed"}), 403
    else:
        # Responds with '400 Bad Request' if verify tokens do not match
        print("MISSING_PARAMETER")
        return jsonify({"status": "error", "message": "Missing parameters"}), 400


def handle_message(request):
    # Handle Webhook Subscriptions
    data = request.get_json()
    if data is None:
        return Response(status=200)
    logging.info("Received webhook data: %s", data)
    changed_field = messenger.changed_field(data)
    if changed_field == "messages":
        new_message = messenger.is_message(data)
        if new_message:
            logging.info("%s", new_message)
            msg = Message(instance=messenger, data=data)
            mobile = msg.sender
            name = msg.name
            message_type = msg.type
            logging.info(
                f"New Message; sender:{mobile} name:{name} type:{message_type}"
            )
            if message_type == "text":
                message = msg.content
                name = msg.name
                logging.info("Message: %s", message)
                if 'sim' in message.lower():
                    m = Message(instance=messenger, to=mobile,
                            content=msg_como_funciona)
                    m.send()
                elif 'quero saber mais' in message.lower():
                    send_button_message_quero_saber(messenger, mobile)
                elif 'não' in message.lower():
                    m = Message(instance=messenger, to=mobile,
                            content="Que pena! Fique a vontade para entrar em contato quando precisar!")
                    m.send()
                elif 'como funciona' in message.lower():
                    send_button_message_como_funciona(messenger, mobile)

            elif message_type == "button":
                button_text = data['entry'][0]['changes'][0]['value']['messages'][0]['button']['text']
                if  button_text == 'Quero saber mais!':
                    send_button_message_quero_saber(messenger, mobile)
                

            elif message_type == "interactive":
                message_response = msg.interactive
                if message_response is None:
                    return Response(status=400)
                interactive_type = message_response.get("type")
                message_id = message_response[interactive_type]["id"]
                message_text = message_response[interactive_type]["title"]

                logging.info(f"Interactive Message; {message_id}: {message_text}")
                
                if message_text == 'Como Funciona?':
                    send_button_message_como_funciona(messenger, mobile)
                elif  message_text == 'Falar com Consultor':
                    m = Message(instance=messenger, to=mobile,
                            content= "Perfeito! Em breve um dos nossos consultores irá entrar em contato. \n\nAtenciosamente,\nEquipe *DívidaLivre*")
                    m.send()
                    db.update_lead_status(mobile, 'esperando')
                elif  message_text == 'Visitar Website':
                    send_button_message_visitar_website(messenger, mobile)

            elif message_type == "location":
                message_location = msg.location
                if message_location is None:
                    return Response(status=400)
                message_latitude = message_location["latitude"]
                message_longitude = message_location["longitude"]
                logging.info("Location: %s, %s",
                                message_latitude, message_longitude)

            elif message_type == "image":
                image = msg.image
                if image is None:
                    return Response(status=400)
                image_id, mime_type = image["id"], image["mime_type"]
                image_url = messenger.query_media_url(image_id)
                if image_url is None:
                    return Response(status=400)
                image_filename = messenger.download_media(image_url, mime_type)
                logging.info(f"{mobile} sent image {image_filename}")

            elif message_type == "video":
                video = msg.video
                if video is None:
                    return Response(status=400)
                video_id, mime_type = video["id"], video["mime_type"]
                video_url = messenger.query_media_url(video_id)
                if video_url is None:
                    return Response(status=400)
                video_filename = messenger.download_media(video_url, mime_type)
                logging.info(f"{mobile} sent video {video_filename}")

            elif message_type == "audio":
                audio = msg.audio
                if audio is None:
                    return Response(status=400)
                audio_id, mime_type = audio["id"], audio["mime_type"]
                audio_url = messenger.query_media_url(audio_id)
                if audio_url is None:
                    return Response(status=400)
                audio_filename = messenger.download_media(audio_url, mime_type)
                logging.info(f"{mobile} sent audio {audio_filename}")

            elif message_type == "document":
                file = msg.document
                if file is None:
                    return Response(status=400)
                file_id, mime_type = file["id"], file["mime_type"]
                file_url = messenger.query_media_url(file_id)
                if file_url is None:
                    return Response(status=400)
                file_filename = messenger.download_media(file_url, mime_type)
                logging.info(f"{mobile} sent file {file_filename}")
            else:
                logging.info(f"{mobile} sent {message_type} ")
                logging.info(data)

            
            if not db.verificar_lead_existente(mobile):
                db.adicionar_novo_lead(nome=name, telefone=mobile, lead_status='iniciou_contato')
                send_button_message_lead_contatou_primeiro(messenger, mobile)



        else:
            delivery = messenger.get_delivery(data)
            if delivery:
                logging.info(f"Message : {delivery}")
            else:
                logging.info("No new message")
    return "OK", 200




@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route("/adminlogin", methods=["GET", "POST"])
def adminlogin():
    """logs admin in"""

    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        #Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        submitted_username = request.form.get("username")
        submitted_password = request.form.get("password")
        admin_usernames = list(admin_credentials.keys())
        if submitted_username in admin_usernames and submitted_password == admin_credentials[submitted_username]:
            # Remember which user has logged in
            session["user_admin"] = True

            #Redirects success case
            return jsonify({'success':True, 'redirect_url': url_for('adminpage')})
        # User reached route via GET (as by clicking a link or via redirect)
        else:
            return jsonify({'success':False, 'error': 'Nome de Usuário ou Senha incorretos.'})

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('adminlogin.html', shownav=True)

@app.route('/adminpage', methods=["GET", "POST"])
@admin_required
def adminpage():
    if request.method == "GET":
        return render_template('adminpage.html')

# Rota para processar o formulário
@app.route('/adicionar_lead', methods=['POST'])
@admin_required
def adicionar_lead():
    nome = request.form.get('nome')
    telefone = request.form.get('telefone')
    cnpj = request.form.get('cnpj')
    erro = db.adicionar_novo_lead(nome, telefone, cnpj)
    
    if erro:
        return f"Erro ao adicionar lead: {erro}"
    return redirect('/adminpage')

# Rota para obter leads em formato JSON
@app.route('/get_leads', methods=['GET'])
def get_new_leads():
    leads = db.get_all_leads()
    return jsonify(leads)

@app.route('/get_all_leads', methods=['GET'])
def get_all_leads():
    leads = db.get_all_leads()
    return jsonify(leads)


@app.route('/send_whatsapp_messages', methods=['POST'])
def send_whatsapp_messages():
    leads = db.get_new_leads()
    phone_numbers = [lead['telefone'] for lead in leads]

    # Supondo que você tenha uma função `send_whatsapp_message` que envia uma mensagem via WhatsApp
    for number in phone_numbers:
        try:
            send_whatsapp_template_message(number, 'apresentacao_limpanome')

            if db.check_lead_status(number) == 'novo':
                db.update_lead_status(number, 'contatado')
                log.info(f"updated lead {number} status to 'contatado'")
            else:
                log.info(f"didnt update lead {number} status")
            


        except Exception as e:
            print(f"Erro ao enviar mensagem para {number}: {e}")

    return jsonify({'status': 'success'}), 200

def send_whatsapp_template_message(phone_number, template):
    messenger.send_template(
        template, phone_number, components=[], lang="pt_BR")
    pass


# Accepts POST and GET requests at /webhook endpoint
@app.route("/webhooks", methods=["POST", "GET"])
def webhook():
    if request.method == "GET":
        return verify(request)
    elif request.method == "POST":
        return handle_message(request)


if __name__ == "__main__":
 app.run()
