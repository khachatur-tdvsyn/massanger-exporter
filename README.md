# Messanger exporter

Get your chat information in any format you wish.

Quick setup
```bash
pip install -r requirements.txt
python manage.py runserver
```

On other side
```bash
celery -A massanger_exporter worker --loglevel=info
```