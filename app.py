from core import TrendyolScraper
from flask import Flask, request, jsonify
import sqlite3
import requests

app = Flask(__name__, template_folder = '.')