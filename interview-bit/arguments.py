#!/Library/Frameworks/Python.framework/Versions/3.13/bin/python3

from argparse import ArgumentParser
from os import getenv
import sys
import subprocess
import logging

print(sys.argv)

parser = ArgumentParser()
parser.add_argument("-a")
parser.add_argument("--pqr")
args = parser.parse_args()
print(type(args))
print(args)
print(args.a, args.pqr)

my_env = getenv("TEST_ENV", "Something")
db = getenv("DB_NAME", "default_db")
print(my_env, db)


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s")
logging.info("Info Message")
logging.debug("Debug Message")
logging.error("Error Message")
logging.warning("Warning")
logging.critical("Critical")

result = subprocess.run(["ls", "-al"], capture_output=True, text=True)
print(result.stdout)
print(exit_code:= result.returncode)

sys.exit(1 if not exit_code else 0)