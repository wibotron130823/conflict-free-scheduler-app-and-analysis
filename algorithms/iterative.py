def is_time_conflict_free_iterative(Mandatory, candidate_activity, candidate_start, candidate_end):
    for mandatory_activity in Mandatory:
        mandatory_start = int(mandatory_activity['start'].split(':')[0]) * 60 + int(mandatory_activity['start'].split(':')[1])
        mandatory_end = int(mandatory_activity['end'].split(':')[0]) * 60 + int(mandatory_activity['end'].split(':')[1])
        if candidate_activity['day'] == mandatory_activity['day']:
            if (candidate_start < mandatory_end and candidate_end > mandatory_start):
                return False
    return True

def get_conflict_free_activities_iterative(Candidate, Mandatory):
    Result = []
    for candidate_activity in Candidate:
        candidate_start = int(candidate_activity['start'].split(':')[0]) * 60 + int(candidate_activity['start'].split(':')[1])
        candidate_end = int(candidate_activity['end'].split(':')[0]) * 60 + int(candidate_activity['end'].split(':')[1])
        if is_time_conflict_free_iterative(Mandatory, candidate_activity, candidate_start, candidate_end):
            Result.append(candidate_activity)
    return Result