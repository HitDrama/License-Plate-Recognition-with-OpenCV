import os
import random
from datetime import timedelta
from flask import url_for

class Config:
    SECRET_KEY="876ey3dtad6qwy3d6e23rrt61e176233stad"
    SQLALCHAMY_DATABASE_URI="mysql+pymysql://root@localhost/xulyanh"
    UPLOAD_FOLDER="static/uploads"
    VIDEO_FOLDER="static/video"