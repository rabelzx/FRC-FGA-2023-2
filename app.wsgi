#
# Conteudo do arquivo `wsgi.py`
#
import sys

sys.path.insert(0, "/var/www/html/video-chat-app")

from app import app as application