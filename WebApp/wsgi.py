# wsgi v1.0:

# Bridging Python web application to Apache server using Web Server Gateway Interface
import sys
sys.path.insert(0,"/var/www/fil-rouge/")
from fil_rouge_app import server as application
