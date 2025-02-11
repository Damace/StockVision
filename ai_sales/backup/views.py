from django.shortcuts import redirect
from django.core.management import call_command
from django.http import HttpResponse
from django.conf import settings
import os

def backup_data(request):
    if request.method == 'POST':
        try:
            # Call the management command to backup the data
            call_command('backup_data')

            # Prepare the backup file path (ensure it's in the backups directory)
            backup_dir = os.path.join(settings.BASE_DIR, 'backups')
            backup_filename = os.listdir(backup_dir)[-1]  # Get the most recent backup file

            # Serve the backup file for download
            with open(os.path.join(backup_dir, backup_filename), 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/sql')
                response['Content-Disposition'] = f'attachment; filename={backup_filename}'
                return response
        except Exception as e:
            return HttpResponse(f'Error: {e}')
    return redirect('some_page')  # Redirect to another page after backup
