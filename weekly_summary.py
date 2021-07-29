from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz

day_input = 25
month_input = 7
year_input = 2021

def main():
    start_month = datetime(year_input, month_input, day_input, 0, 0, 0,tzinfo=pytz.timezone("Asia/Jerusalem"))
    deep_work_file = open('../deep work.ics','rb')
    cal_deep_work = Calendar.from_ical(deep_work_file.read())
    total_deep_work = timedelta(0)
    for day in range(0, 7):
        start_day_of_month = start_month + day * timedelta(days=1)
        print(start_day_of_month.day, '-', start_day_of_month.month, '-', start_day_of_month.year)
        for component in cal_deep_work.walk():
            event_time = get_timedelta(component, start_day_of_month)
            total_deep_work += event_time
    deep_work_file.close()
    print('total_deep_work: ', total_deep_work.seconds//3600, ' hours')


def get_timedelta(component, start_day_of_month):
    if component.name == "VEVENT":
        start_event = component.get('dtstart').dt
        end_event =  component.get('dtend').dt
        if isinstance(start_event, datetime) and isinstance(end_event, datetime):
            end_day_of_month = start_day_of_month + timedelta(hours=23, minutes=59)
            if start_event >= start_day_of_month and end_event <= end_day_of_month:
                # print(component.get('summary'), ' : ', component.get('dtstart').dt)
                delta_event = component.get('dtend').dt - component.get('dtstart').dt
                return delta_event
    return timedelta(0)

if __name__ == '__main__':
    main()