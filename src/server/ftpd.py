import os
import pathlib

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler, TLS_FTPHandler
from pyftpdlib.servers import FTPServer

from models import UserModel
from auth import app

os.chdir(pathlib.Path(__file__).parent.resolve())

BASE_DIR = os.path.join(os.getcwd(), 'data')
ANONYMOUS_DIR = os.path.join(os.getcwd(), 'data/anonymous')
ADDRESS = ('127.0.0.1', 2121)

def main():
  users = UserModel.getAll()
  authorizer = DummyAuthorizer()
  for user in users:
    USER_DIR = os.path.join(BASE_DIR, user['username'])
    if not os.path.exists(USER_DIR):
      os.makedirs(USER_DIR)

    authorizer.add_user(
      user['username'],
      user['password'],
      USER_DIR, 
      perm='elradfmw'
    )

  authorizer.add_anonymous(ANONYMOUS_DIR, perm='elradfmwMT')

  handler = FTPHandler
  handler.authorizer = authorizer



  server = FTPServer(ADDRESS, handler)

  server.serve_forever()

print(UserModel.getAll())

main()


