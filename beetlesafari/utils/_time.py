def hours_to_seconds(hours : float):
    return hours * 60 * 60

def minutes_to_seconds(minutes : float):
    return minutes * 60

def seconds_to_hours(seconds : float):
    return seconds / 60 / 60

def seconds_to_minutes(seconds: float):
    return seconds / 60

def days_to_seconds(days : float):
    return hours_to_seconds(24 * days)