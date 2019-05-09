from flask import Flask
import requests

app = Flask(__name__)

ftp_site = 'ftp://sftp.cdc.gov/'
rest_site = 'https://test-vaccinecodeset.cdc.gov/SymedicalDistributionRESTTest/api/distributionext/'

@app.route('/')
def home():
    response = requests.get(rest_site + 'available/TEST_JDI_1')
    result = "<table><th>Package Name</th><th>Subscribed?</th><th>Approved?</th>"
    for package in response.json()['PackageItems']:
        print(package)
        result += '<tr>'
        result += '<td>' + package['PackageUID'] + '</td>'
        result += '<td>' + str(package['PackageTemplateIsSubscribed']) + '</td>'
        result += '<td>' + str(package['PackageApprovedToSubscribe']) + '</td>'
        result += '</tr>'
    result += '</table>'

    return result

@app.route('/download')
def download():
    response = requests.post(
        rest_site + 'pending/TEST_JDI_1',
        json={},
    )
    available = get_available_dict()
    result = "<table><th>Package Name</th>"
    for package in response.json()['Packages']:
        ftp_location = package['PackageName']
        name = available.get(package['DistributionPackageUID'], ftp_location)
        result += '<tr>'
        result += '<td><a href="' + ftp_site + ftp_location  + '">' + name + '</a></td>'
        result += '</tr>'
    result += '</table>'
    return result

def get_available_dict():
    response = requests.get(rest_site + 'available/TEST_JDI_1')
    ret_dict = {}
    for package in response.json()['PackageItems']:
        key = package['PackageUID']
        value = package['PackageTemplateName']
        ret_dict[key] = value
    return ret_dict
