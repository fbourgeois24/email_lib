import os

try:
	from email_lib.email_lib import mail_sender
except ModuleNotFoundError:
	# Si module non trouvé, on installe les dépendances
	os.popen(f"pip install --no-cache-dir -r {os.path.dirname(os.path.realpath(__file__))}/requirements.txt").read()
	from email_lib.email_lib import mail_sender