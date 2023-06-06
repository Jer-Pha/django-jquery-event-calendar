const HTML_START_WEEK = '<tr class="calendar-week">';
const HTML_END_WEEK = '</tr>';
const HTML_START_DAY = '<td><div class="calendar-day"><div class="calendar-content"><div class="calendar-number"><span class="mobile-header">';
const HTML_MID_DAY = '</span></div></div>';
const HTML_END_DAY = '</div></div></td>';
const HTML_NO_DAY = '<td class="calendar-no-day"></td>';
const URL = $('#page-info').attr('data-url');
const CSRF_TOKEN = $('#page-info').attr('data-session');

let prevMonth = $('#page-info').attr('data-prev-month');
let nextMonth = $('#page-info').attr('data-next-month');

function loadMonth(month){
    $.ajax({
        type: 'POST',
        url: URL,
        data: {
            'month': month,
            'csrfmiddlewaretoken': CSRF_TOKEN
        },
        datatype:'json',
        headers: { 'X-CSRFToken': CSRF_TOKEN},
        success: function (data) {
            prevMonth = data['prev_month_name'] + ' ' + data['prev_month_year'];
            nextMonth = data['next_month_name'] + ' ' + data['next_month_year'];
            $('#calendar-header').html(data['curr_month_name'] + '&nbsp;' + data['curr_month_year']);
            var html = '';

            for (var week = 0; week < data['curr_month_calendar'].length; week++) {
                html += HTML_START_WEEK;

                for (var day = 0; day < data['curr_month_calendar'][week].length; day++) {
                    if (data['curr_month_calendar'][week][day]) {
                        html += HTML_START_DAY;
                        html += data['curr_month_name'] + '</span>&nbsp;' + data['curr_month_calendar'][week][day];
                        html += '<div class="day-of-week"><span class="mobile-header">' + data['day_of_week'][day];

                        html += HTML_MID_DAY;

                        for (var event = 0; event < data['events'].length; event++) {
                            if (data['events'][event]['fields']['day'] == data['curr_month_calendar'][week][day]) {
                                html += '<div class="event-item ';

                                html += '" title="' + data['events'][event]['fields']['title'] + '"><a href="/calendar_app/view-event/' + data['events'][event]['pk'] + '">' + data['events'][event]['fields']['title'] + '</div>';
                            }
                        }

                        html += HTML_END_DAY;
                    }
                    else
                        html += HTML_NO_DAY;
                }

                html += HTML_END_WEEK;
            }

            $('#render-calendar').html(html);

            if (data['prev_limit'])
                $('#prev-month').hide();
            else
                $('#prev-month').show();

            if (data['next_limit'])
                $('#next-month').hide();
            else
                $('#next-month').show();
        }
    });
}

document.getElementById('prev-month').addEventListener('click', function () {
    loadMonth(prevMonth);
});
document.getElementById('next-month').addEventListener('click', function () {
    loadMonth(nextMonth);
});
