from django.core.management import call_command

def timing_backup():
  try:
    call_command('dbbackup')
  except:
    pass