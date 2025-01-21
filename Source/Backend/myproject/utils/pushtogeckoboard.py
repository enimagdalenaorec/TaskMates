import requests
from django.http import JsonResponse
from core.models import GroupUser,UserTask,Rating
from django.db.models import Avg

def push_to_geckoboard(group_id):
    # Your Geckoboard API credentials
    GECKOBOARD_API_KEY = "d992f0c3fb528552927eff165bd63388"  
    GECKOBOARD_WIDGET_KEY_POINTS = "ba7e291e-0bf9-4af7-840b-f9ffc14095a8"
    GECKOBOARD_WIDGET_KEY_GRADES = "36511923-df2c-4e5d-a76a-11f4d673ea90"
    GECKOBOARD_WIDGET_KEY_COMPLETED = "128ba265-7513-4607-ace7-32ddfa3d8a65"
    
    # URLs for the three Geckoboard widgets
    GECKOBOARD_PUSH_URL1 = f"https://push.geckoboard.com/v1/send/{GECKOBOARD_WIDGET_KEY_POINTS}"
    GECKOBOARD_PUSH_URL3 = f"https://push.geckoboard.com/v1/send/{GECKOBOARD_WIDGET_KEY_GRADES}"
    GECKOBOARD_PUSH_URL2 = f"https://push.geckoboard.com/v1/send/{GECKOBOARD_WIDGET_KEY_COMPLETED}"

    # Fetch the GroupUser objects based on the group_id
    group_users = GroupUser.objects.filter(group=group_id)

    # Prepare the leaderboard data (same data for all 3 widgets)
    leaderboard_data_points = [
        {"label": user.user.username, "value": user.points}
        for user in group_users
    ]

    leaderboard_data_points.sort(key=lambda x: x['value'], reverse=True)

    leaderboard_data_tasks_solved = [
        {"label": user.user.username, "value": user.tasks_solved}  # Changed to 'tasks_solved' for the second widget
        for user in group_users
    ]
    leaderboard_data_tasks_solved.sort(key=lambda x: x['value'], reverse=True)

    # Define the payload structure
    payload_points = {
        "api_key": GECKOBOARD_API_KEY,
        "data": {
            "items": leaderboard_data_points  # Use 'points' leaderboard data
        }
    }

    payload_tasks_solved = {
        "api_key": GECKOBOARD_API_KEY,
        "data": {
            "items": leaderboard_data_tasks_solved  # Use 'tasks_solved' leaderboard data
        }
    }
    #ZA AVG OCJENU
    leaderboard_data_avg = []
    for user in group_users:
        # Get the tasks the user has worked on in the group
        user_tasks = UserTask.objects.filter(user=user.user, task__group__id=group_id)

        # Get all task ids the user has worked on
        task_ids = user_tasks.values_list('task_id', flat=True)

        # Get all ratings for the tasks the user worked on
        ratings = Rating.objects.filter(task_id__in=task_ids)

        # Calculate the average rating for the user's tasks
        avg_rating = ratings.aggregate(Avg('value'))['value__avg'] if ratings.exists() else 0

        leaderboard_data_avg.append({
            "label": user.user.username,
            "value": avg_rating,
        })
    leaderboard_data_avg.sort(key=lambda x: x['value'], reverse=True)
    payload_avg = {
        "api_key": GECKOBOARD_API_KEY,
        "data": {
            "items": leaderboard_data_avg  # Use 'tasks_solved' leaderboard data
        }
    }
    # Prepare the headers
    headers = {"Content-Type": "application/json"}

    # Send data to the first leaderboard (Points)
    response1 = requests.post(GECKOBOARD_PUSH_URL1, json=payload_points, headers=headers)
    
    # Send data to the second leaderboard (Tasks Solved) - Uses 'tasks_solved'
    response2 = requests.post(GECKOBOARD_PUSH_URL2, json=payload_tasks_solved, headers=headers)
    
    # Send data to the third leaderboard (Completed)
    response3 = requests.post(GECKOBOARD_PUSH_URL3, json=payload_avg, headers=headers)  # Same data as first request

    # Check the response status for each request and return the corresponding result
    if response1.status_code == 200 and response2.status_code == 200 and response3.status_code == 200:
        return JsonResponse({"message": "Data pushed successfully to all leaderboards."})
    else:
        # Capture and print the error message returned by Geckoboard
        error_messages = {
            "response1": response1.json() if response1.status_code != 200 else None,
            "response2": response2.json() if response2.status_code != 200 else None,
            "response3": response3.json() if response3.status_code != 200 else None,
        }
        print("Error from Geckoboard:", error_messages)
        return JsonResponse({"message": "Failed to push data.", "error": error_messages}, status=400)