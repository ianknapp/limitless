# Main webapp process
web: gunicorn --timeout 120 limitless.wsgi --chdir=server --log-file -

# Update DB schema for any changes
release: python server/manage.py migrate --noinput && python server/manage.py update_cura_printers
