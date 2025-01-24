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

from django.http import HttpResponse
from django.middleware.csrf import get_token

def test_csrf(request):
    csrf_token = get_token(request)
    print(f"CSRF token: {csrf_token}")  # Print the generated CSRF token

    response = HttpResponse("CSRF test")
    response["Access-Control-Allow-Origin"] = "https://taskmates-gjhi.onrender.com"  # Important for testing
    response["Access-Control-Allow-Credentials"] = "true"  # Important for testing
    return response