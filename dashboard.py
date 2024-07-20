import os
import logging
import json
from whatsapp import WhatsApp, Message
from dotenv import load_dotenv
from flask import Flask, render_template, request

def admin_login(credentials):
