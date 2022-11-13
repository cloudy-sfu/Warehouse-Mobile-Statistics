from get_data import get_data
from get_stats import statistics

import pywebio


def index():
    pywebio.output.put_markdown('# Warehouse Mobile Statistics')
    username = pywebio.input.input(
        'NZ phone number', type=pywebio.input.NUMBER,
        help_text='Do not contain any blanks, dashes, brackets or other not-numbers.'
    )
    username = '64' + str(username)
    retrieve_data = pywebio.input.select(
        'Update data?', options=[('Yes', True), ('No', False)],
        help_text='If you choose \'Yes\', this program will request data from warehouse mobile website.'
    )
    if retrieve_data:
        password = pywebio.input.input('Password', type='password')
        try:
            pywebio.output.put_text('Retrieving data from warehouse mobile website ...\n'
                                    'Please do not close this program. It may takes some minutes, and you can track '
                                    'the progress in the console.')
            get_data(username, password)
        except Exception as e:
            pywebio.output.put_error(e)
            pywebio.output.put_html(
                '<button class="btn btn-primary" onclick="window.location.href = \'/\'">Back</button>')
            return
    try:
        s = statistics(username)
    except Exception as e:
        pywebio.output.put_error(e)
        pywebio.output.put_html('<button class="btn btn-primary" onclick="window.location.href = \'/\'">Back</button>')
        return
    pywebio.output.put_grid([
        [pywebio.output.span(pywebio.output.put_markdown('## This month'), col=3)],
        [pywebio.output.put_html(
            "<div class='alert alert-light border-dark m-2 text-dark'><p>Data usage</p> "
            f"<h3 class='text-center'>{s['tmu']['d']}</h3> <p class='text-right'>(MB) $ {s['tmf']['d']}</p></div>"
        ), pywebio.output.put_html(
            "<div class='alert alert-light border-dark m-2 text-dark'><p>Text usage</p> "
            f"<h3 class='text-center'>{s['tmu']['t']}</h3> <p class='text-right'>$ {s['tmf']['t']} </p></div>"
        ), pywebio.output.put_html(
            "<div class='alert alert-light border-dark m-2 text-dark'><p>Call usage</p> "
            f"<h3 class='text-center'>{s['tmu']['c']}</h3> <p class='text-right'>(Minutes) $ {s['tmf']['c']}</p></div>"
        )]
    ])
    pywebio.output.put_markdown('## History')
    pywebio.output.put_grid([
        [pywebio.output.put_text('Usage'), pywebio.output.put_text('Extra fee (not covered by value packs)')],
        [pywebio.output.put_html(s['hu'].to_html(border=0)), pywebio.output.put_html(s['hf'].to_html(border=0))]
    ])
    pywebio.output.put_html('<button class="btn btn-primary" onclick="window.location.href = \'/\'">Back</button>')


if __name__ == '__main__':
    # Debug
    # pywebio.start_server([index], auto_open_webbrowser=False, port=5000, debug=True)
    # Deploy
    pywebio.start_server([index], auto_open_webbrowser=True)
