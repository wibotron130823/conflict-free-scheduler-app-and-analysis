def is_time_conflict_free_recursive(Mandatory, candidate_activity, candidate_start, candidate_end, i):
    if i >= len(Mandatory):
        return True
    mandatory_activity = Mandatory[i]
    mandatory_start = int(mandatory_activity['start'].split(':')[0]) * 60 + int(mandatory_activity['start'].split(':')[1])
    mandatory_end = int(mandatory_activity['end'].split(':')[0]) * 60 + int(mandatory_activity['end'].split(':')[1])
    if candidate_activity['day'] == mandatory_activity['day']:
        if (candidate_start < mandatory_end and candidate_end > mandatory_start):
                return False
    return is_time_conflict_free_recursive(Mandatory, candidate_activity, candidate_start, candidate_end, i + 1)

def get_conflict_free_activities_recursive(Candidate, Mandatory, i, Result=None):
    if i == 0:
        Result = []
    if i >= len(Candidate):
        return Result
    candidate_activity = Candidate[i]
    candidate_start = int(candidate_activity['start'].split(':')[0]) * 60 + int(candidate_activity['start'].split(':')[1])
    candidate_end = int(candidate_activity['end'].split(':')[0]) * 60 + int(candidate_activity['end'].split(':')[1])
    if is_time_conflict_free_recursive(Mandatory, candidate_activity, candidate_start, candidate_end, 0):
        Result.append(candidate_activity)
    return get_conflict_free_activities_recursive(Candidate, Mandatory, i + 1, Result)