from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz

month = 7


def main():
    start_month = datetime(2021, month, 1,0,0,0,tzinfo=pytz.timezone("Asia/Jerusalem"))
    deep_work_file = open('../deep work.ics','rb')
    work_file = open('../Work.ics','rb')
    meeting_file = open('../meeting.ics','rb')
    cal_deep_work = Calendar.from_ical(deep_work_file.read())
    cal_work = Calendar.from_ical(work_file.read())
    cal_meeting = Calendar.from_ical(meeting_file.read())
    total_deep_work = timedelta(0)
    total_work = timedelta(0)
    total_meeting = timedelta(0)

    for day in range(0, 32):
        day_hours = timedelta(0)
        day_hours_deep_work = timedelta(0)
        day_hours_work = timedelta(0)
        day_hours_meeting = timedelta(0)
        start_day_of_month = start_month + day * timedelta(days=1)
        for component in cal_deep_work.walk():
            event_time = get_timedelta(component, start_day_of_month)
            day_hours_deep_work += event_time
            total_deep_work += event_time
        for component in cal_work.walk():
            event_time = get_timedelta(component, start_day_of_month)
            day_hours_work += event_time
            total_work += event_time
        for component in cal_meeting.walk():
            event_time = get_timedelta(component, start_day_of_month)
            day_hours_meeting += event_time
            total_meeting += event_time
        day_hours = day_hours_deep_work + day_hours_work + day_hours_meeting
        print('day ', day + 1, ': ', day_hours)


    deep_work_file.close()
    work_file.close()
    meeting_file.close()
    print('total_deep_work: ', total_deep_work.seconds//3600, ' hours')
    print('total_work: ', total_work.seconds//3600, ' hours')
    print('total_meeting: ', total_meeting.seconds//3600, ' hours')


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