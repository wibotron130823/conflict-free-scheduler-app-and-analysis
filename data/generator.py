import random
from data.static import BAND_ACTIVITIES, DAYS_OF_WEEK
from algorithms.iterative import is_time_conflict_free_iterative

def generate_activities(size, conflict_free):
    activities = []
    attempts = 0

    if conflict_free:
        max_attempts = size * 50
    else:
        max_attempts = size * 2

    while len(activities) < size and attempts < max_attempts:
        random_day = random.choice(DAYS_OF_WEEK)
        random_activity = random.choice(BAND_ACTIVITIES)
        random_start_hour = random.randint(8, 18)
        random_start_minute = random.choice([0, 15, 30, 45])
        random_duration_minute = random.choice([30, 60, 90, 120])

        total_start_minute = random_start_hour * 60 + random_start_minute
        total_end_minute = total_start_minute + random_duration_minute

        random_end_hour = total_end_minute // 60
        random_end_minute = total_end_minute % 60

        new_random_activity = {
            "day": random_day, 
            "activity": f"{random_activity} {len(activities)+1}", 
            "start": f"{random_start_hour:02}:{random_start_minute:02}", 
            "end": f"{random_end_hour:02}:{random_end_minute:02}"
        }
        if conflict_free:
            if is_time_conflict_free_iterative(activities, new_random_activity, total_start_minute, total_end_minute):
                activities.append(new_random_activity)
        else:
            activities.append(new_random_activity)
        attempts += 1

    return activities
