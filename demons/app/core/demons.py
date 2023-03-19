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

                    # Event creation.
                    event = CoreEvent.objects.create(
                        name=f'Lunch in {place.name}',
                        date=date,
                        start_time=sett.start_time,
                        end_time=sett.end_time,
                        place=place,
                    )

                    # Build email content.
                    str_date = date.strftime('%d/%m/%Y')
                    str_s_time = sett.start_time.strftime('%H:%M')
                    str_e_time = sett.end_time.strftime('%H:%M')

                    text_content = (
                        f'{event.name} ({place.address})\n' +
                        f'{str_date} from {str_s_time}' +
                        f' to {str_e_time} with:\n' +
                        ''.join(f' - {user.username}\n' for user in users)
                    )

                    html_content = (
                        '<html><head>' +
                        f'<title>{event.name}</title>' +
                        '</head><body>' +
                        f'<img src="{place.image}" />' +
                        f'<p>Lunch in <strong>{place.name} ({place.address})</strong>' +
                        f'<br /><strong>{str_date}</strong>' +
                        f' from <strong>{str_s_time}</strong>' +
                        f' to <strong>{str_e_time}</strong> with:</p>' +
                        '<ul>' +
                        ''.join(f'<li>{user.username}</li>' for user in users) +
                        '</ul></body></html>'
                    )

                    now = datetime.now()
                    str_date = date.strftime('%Y%m%d')
                    str_s_time = sett.start_time.strftime('%H%M%S')
                    str_e_time = sett.end_time.strftime('%H%M%S')
                    plain_content = text_content.replace('\n', '\\n')
                    caldav = (
                        'BEGIN:VCALENDAR\n' +
                        'VERSION:2.0\n' +
                        'PRODID:Django\n' +
                        'CALSCALE:GREGORIAN\n' +
                        'METHOD:REQUEST\n' +
                        'BEGIN:VEVENT\n' +
                        f'DTSTAMP:{now.strftime("%Y%m%dT%H%M%S")}\n' +
                        'STATUS:CONFIRMED\n' +
                        f'DTSTART:{str_date}T{str_s_time}\n' +
                        f'DTEND:{str_date}T{str_e_time}\n' +
                        f'SUMMARY:{event.name}\n' +
                        f'DESCRIPTION:{plain_content}\n' +
                        'ORGANIZER;CN=Lunch Roulette demon:mailto:lunch@roulette.demon\n' +
                        ''.join(f'ATTENDEE;CUTYPE=INDIVIDUAL;RSVP=TRUE;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;CN="{user.username}";X-NUM-GUESTS=0:MAILTO:{user.email}\n' for user in users) +
                        'SEQUENCE:0\n' +
                        f'GEO:{place.lat};{place.lon}\n'
                        'END:VEVENT\n' +
                        'END:VCALENDAR'
                    )

                    # Add colleagues and send email.
                    for user in users:
                        CoreEventColleagues.objects.create(
                            event=event,
                            user=user
                        )

                        to = f'{user.username}<{user.email}>'
                        msg = EmailMultiAlternatives(event.name, text_content, to=[to])
                        msg.attach_alternative(html_content, 'text/html')
                        msg.attach_alternative(caldav, 'text/calendar; method=REQUEST')
                        msg.attach('invite.ics', caldav, 'application/ics; name="invite.ics"')
                        msg.send()
                else:
                    print('No day selected.')

            else:
                print('No user available.')

        else:
            print('No place available.')
