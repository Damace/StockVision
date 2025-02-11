import os
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
import subprocess

class Command(BaseCommand):
    help = 'Create a backup of the database'

    def handle(self, *args, **kwargs):
        # Get database settings
        db_name = settings.DATABASES['default']['NAME']
        db_user = settings.DATABASES['default']['USER']
        db_password = settings.DATABASES['default']['PASSWORD']
        db_host = settings.DATABASES['default']['HOST']
        db_port = settings.DATABASES['default']['PORT']

        # Ensure db_name is a filename-friendly string
        db_filename = os.path.basename(db_name)  # Removes any directory path
        backup_filename = f"backup_{db_filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"

        # Define backup directory and ensure it exists
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)

        backup_filepath = os.path.join(backup_dir, backup_filename)

        # Database dump command
        if 'postgresql' in settings.DATABASES['default']['ENGINE']:
            dump_command = [
                'pg_dump',
                '--username=' + db_user,
                '--host=' + db_host,
                '--port=' + str(db_port),
                '--file=' + backup_filepath,
                '--no-password',
                db_name
            ]
        elif 'mysql' in settings.DATABASES['default']['ENGINE']:
            dump_command = [
                'mysqldump',
                '--user=' + db_user,
                '--password=' + db_password,
                '--host=' + db_host,
                '--port=' + str(db_port),
                db_name,
                '--result-file=' + backup_filepath
            ]
        else:
            self.stdout.write(self.style.ERROR('Unsupported database engine'))
            return

        # Run the backup command
        try:
            subprocess.run(dump_command, check=True)
            self.stdout.write(self.style.SUCCESS(f'Backup successful: {backup_filepath}'))
        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR(f'Error during backup: {e}'))
