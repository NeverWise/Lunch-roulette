from core.models.auth_user import AuthUser
from core.models.core_setting import CoreSetting
from core.models.core_place import CorePlace
from core.models.core_event import CoreEvent, CoreEventColleagues

from django.core.mail import EmailMultiAlternatives

import random
from datetime import datetime, timedelta


def random_event():
    """Generate a random event."""

    for sett in CoreSetting.objects.filter(name='default'):

        # Get the Place, if None skip all.
        place = CorePlace.objects.order_by('?').first()
        if place is not None:

            # Get the colleagues, if None skip all.
            users = AuthUser.objects.order_by('?')[:sett.colleagues_number]
            if users is not None:

                selected_days = []
                for d, e in sett.week_days:
                    if e:
                        id_day = (
                            1 if d == 'monday' else
                            2 if d == 'tuesday' else
                            3 if d == 'wednesday' else
                            4 if d == 'thursday' else
                            5 if d == 'friday' else 0
                        )
                        if (id_day != 0):
                            selected_days.append(id_day)

                if (len(selected_days) > 0):
                    today = datetime.now()
                    days_to_date = (
                        6 - today.weekday() + random.choice(selected_days)
                    )
                    date = today + timedelta(days=days_to_date)

                    subject = 'Subject email'
                    text_content = 'This is an important message'
                    html_content = '<p>This is an <strong>important</strong> message.</p>'
                    to = 'Supremo<test@example.com>'
                    caldav = '''BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//hacksw/handcal//NONSGML v1.0//EN
BEGIN:VEVENT
UID:uid1@example.com
DTSTAMP:19970714T170000Z
ORGANIZER;CN=John Doe:MAILTO:john.doe@example.com
DTSTART:19970714T170000Z
DTEND:19970715T040000Z
SUMMARY:Bastille Day Party
GEO:48.85299;2.36885
END:VEVENT
END:VCALENDAR'''

                    msg = EmailMultiAlternatives(subject, text_content, to=[to])
                    msg.attach_alternative(html_content, 'text/html')
                    msg.attach_alternative(caldav, 'text/calendar; method=REQUEST')
                    msg.attach('invite.ics', caldav, 'application/ics; name="invite.ics"')
                    msg.send()
                    #event = CoreEvent.objects.create(
                    #    name=f'Lunch in {place.name}',
                    #    date=date,
                    #    start_time=sett.start_time,
                    #    end_time=sett.end_time,
                    #    place=place,
                    #)
                    #for user in users:
                    #    CoreEventColleagues.objects.create(
                    #        event=event,
                    #        user=user
                    #    )
                        # TODO: sending email
                else:
                    print('No day selected.')

            else:
                print('No user available.')

        else:
            print('No place available.')
