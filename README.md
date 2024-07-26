# DívidaLivre - Aplicação de Gerenciamento de Leads e Mensagens no WhatsApp

## Descrição

DívidaLivre é uma aplicação web desenvolvida em Flask que gerencia leads e envia mensagens comerciais via WhatsApp. A aplicação permite que os usuários adicionem novos leads, vejam a lista de leads e enviem mensagens automaticamente para leads específicos usando a API do WhatsApp. Os dados dos leads são armazenados no DynamoDB.

A aplicação também realiza o atendimento automático do Whatsapp por meio de mensagens interativas.

## Funcionalidades

- **Adição de Leads:** Formulário para adicionar novos leads com nome e telefone.
- **Exibição de Leads:** Lista dinâmica de leads com status 'novo'.
- **Envio de Mensagens:** Envio automático de mensagens via WhatsApp para leads na lista.
- **Login de Administrador:** Página de login para acesso ao painel de administração.

## Tecnologias Utilizadas

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Banco de Dados:** Amazon DynamoDB
- **Integração:** API do WhatsApp

## Estrutura do Projeto

```bash
.
├── app.py                  # Arquivo principal da aplicação Flask
├── database.py             # Funções de acesso ao DynamoDB
├── helpers.py             # Funções auxiliares, como @admin_required
├── templates/
│   ├── layout.html         # Template base
│   ├── index.html          # Página inicial da aplicação. Uma landing page mostrando sobre a empresa
│   ├── adminlogin.html     # Página de ogin de administrador
│   └── adminpage.html      # Exibição e gerenciamento de leads
├── static/
│   └── Imagens, CSS, Scripts
├── .env                    # Arquivo de variáveis de ambiente
├── README.md               # Este arquivo
└── requirements.txt        # Dependências do projeto
