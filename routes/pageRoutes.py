from flask import Flask, render_template, request, redirect, url_for, Response, session, Blueprint
from flask_cors import CORS
import json
import random
import uuid
import os
import qrcode
from datetime import datetime

from sharedFuncs import bs

app = Blueprint('pageRoutes', __name__)



