# Main webapp process
web: gunicorn limitless.wsgi --chdir=server --log-file -

# Update DB schema for any changes
release: python server/manage.py migrate --noinput && python server/manage.py update_cura_printers
