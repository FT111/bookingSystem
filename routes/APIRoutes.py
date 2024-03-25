from flask import Flask, render_template, request, redirect, url_for, Response, session
from flask_cors import CORS
import json
import random
import uuid
import os
import qrcode
from datetime import datetime

import sharedFuncs