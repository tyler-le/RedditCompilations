import datetime
import pytz

def get_next_weekday(weekday_name: str, time="12:00:00"):
    """
    Given a weekday name (e.g., "Monday", "Tuesday"), this function
    returns the next occurrence of that day at 12 PM PST, in ISO 8601 format.
    
    :param weekday_name: Name of the weekday (e.g., "Monday", "Tuesday", etc.)
    :param time: Time of the day in 24-hour format (default is 12:00:00 for 12 PM)
    :return: ISO 8601 formatted timestamp for the next occurrence of the specified weekday at 12 PM PST
    """
    # Mapping the weekday name to a number (Monday=0, Sunday=6)
    weekday_map = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6
    }
    
    # Ensure the provided weekday is valid
    if weekday_name not in weekday_map:
        raise ValueError("Invalid weekday name. Please use one of: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday.")
    
    # Get the current date and calculate days ahead
    today = datetime.date.today()
    weekday = weekday_map[weekday_name]
    days_ahead = weekday - today.weekday()
    
    # If the specified weekday has already passed this week, move to next week
    if days_ahead <= 0:
        days_ahead += 7
    
    # Calculate the date of the next occurrence of the weekday
    next_day = today + datetime.timedelta(days=days_ahead)
    
    # Combine the next date with the desired time (12:00 PM PST)
    next_datetime_str = f"{next_day} {time}"
    
    # Define PST timezone
    pst = pytz.timezone("US/Pacific")
    
    # Combine the date and time and localize it to PST
    next_datetime = datetime.datetime.strptime(next_datetime_str, "%Y-%m-%d %H:%M:%S")
    localized_datetime = pst.localize(next_datetime)
    
    # Convert the localized datetime to UTC and return in ISO 8601 format
    utc_datetime = localized_datetime.astimezone(pytz.utc)
    return utc_datetime.isoformat()

# Example usage (This can be run directly or imported as a module)
if __name__ == "__main__":
    day = "Monday"  # Change this to test other weekdays
    print(f"The next {day} at 12 PM PST in ISO 8601 format is: {get_next_weekday(day)}")
