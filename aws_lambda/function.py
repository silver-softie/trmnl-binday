import json
from datetime import date, timedelta

def get_next_collection(today):
    """
    A function to calculate bin collection for the next upcoming Tuesday
    from the current date.

    The collection schedule is as follows, starting from July 8, 2025:
    - Week 1: Paper and Cardboard (Grey Bin)
    - Week 2: Food and Garden Waste (Brown Bin), Landfill (Blue Bin)
    - Week 3: Cans and Plastics (Green Bin)
    - Week 4: Food and Garden Waste (Brown Bin), Landfill (Blue Bin)
    This pattern repeats every four weeks.
    All collections are on Tuesdays.
    """        

    # Calculate days until the next Tuesday (Tuesday is weekday() == 1)
    # (1 - today.weekday() + 7) % 7 ensures we get 0 if today is Tuesday,
    # 1 if today is Monday, etc., wrapping around for the next week.
    days_until_next_tuesday = (1 - today.weekday() + 7) % 7
    
    # Determine the date of the next upcoming Tuesday
    next_tuesday = today + timedelta(days=days_until_next_tuesday)

    # Define the reference date (July 8, 2025 - a Tuesday with Grey Bin)
    reference_date = date(2025, 7, 8)

    # Calculate the difference in days from the reference date to the next_tuesday
    delta_days = (next_tuesday - reference_date).days

    # Calculate the number of weeks past the reference date
    week_number_from_reference = delta_days // 7

    # Determine the cycle week (0, 1, 2, or 3)
    cycle_week = week_number_from_reference % 4

    bins_due = {}
    if cycle_week == 0:
        bins_due = {"blue": False, "brown": False, "green": False, "grey": True}
    elif cycle_week == 1:
        bins_due = {"blue": True, "brown": True, "green": False, "grey": False}
    elif cycle_week == 2:
        bins_due = {"blue": False, "brown": False, "green": True, "grey": False}
    elif cycle_week == 3:
        bins_due = {"blue": True, "brown": True, "green": False, "grey": False}
    else:
        bins_due = {} # Fallback, though highly unlikely

    return next_tuesday, bins_due
    

def lambda_handler(event, context):
    """
    AWS Lambda function to calculate bin collection for the next upcoming Tuesday
    from the current date.
    """

    next_tuesday, bins_due = get_next_collection(date.today())

    try:
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'data': {
                    'date': next_tuesday.isoformat(),
                    'bins_due': bins_due
                }
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({"error": f"An unexpected error occurred: {str(e)}"})
        }

if __name__ == "__main__":
    today = date.today()
    #today = date(2025, 8, 20)
    next_collection = get_next_collection(today)
    print(next_collection)
