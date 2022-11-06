from flask import Flask
# Python sets the __name__ variable to the module name, so the value of this variable will vary depending on the Python source file in which you use it.
app=Flask(__name__)
from application import routes
