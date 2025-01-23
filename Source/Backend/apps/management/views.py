# management/views.py
from django.core.management import call_command
from django.http import JsonResponse

def run_check_deadlines(request):
    try:
        # Run the custom management command 'check_deadlines'
        call_command('checkdeadlines')
        return JsonResponse({"status": "success", "message": "Deadline check completed."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

