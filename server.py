from flask import Flask, render_template, url_for, request, redirect, make_response
import csv
app = Flask(__name__)


contact_details = {
    'email': 'druhfus@gmail.com',
    'tel': '+27 83 566 4673',
    'address': 'Umhlanga Rocks, KZN, South Africa'
}


@app.route('/')
def my_home():
    return render_template('./index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


def write_to_file(data):
    with open('cfdata.kddata', mode='a') as database:
        email = data['form_data']['email']
        subject = data['form_data']['subject']
        message = data['form_data']['message']
        remote_address = data['remote_address']
        agent_data = data['agent_data']

        file = database.write(f'\n<---------- Start ---------->\n'
                              f'--> Email:\n{email}'
                              f'\n--> Subject:\n{subject}'
                              f'\n--> Message:\n{message}'
                              f'\n<---Msg End--->'
                              f'\n--> Remote Address: {remote_address}'
                              f'\n--> Agent Data:'
                              f'\n{agent_data}'
                              f'\n<----------  END  ---------->')
        return file


def write_to_csv(data):
    with open('database.csv', newline='', mode='a') as database2:
        email = data['form_data']['email']
        subject = data['form_data']['subject']
        message = data['form_data']['message']
        remote_address = data['remote_address']
        agent_data = data['agent_data']
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message, remote_address, agent_data])


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    data = {'form_data': {}, 'remote_address': "", 'agent_data': ''}
    if request.method == 'POST':
        try:
            data['form_data'] = request.form.to_dict()
            data['remote_address'] = request.remote_addr
            data['agent_data'] = request.user_agent.string
            write_to_csv(data)
            return redirect('thankyou.html')
        except:
            return error
    else:
        return "Something when wrong.. Please try again later."
