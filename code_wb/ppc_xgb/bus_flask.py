import pathlib
from flask import Flask, Response

from bus_info import get_bus_info
from bus_test import discover_reports


app = Flask(__name__)


# http://127.0.0.1:5001/bus/gaoxinnan
@app.route('/bus/<station>')
def bus_info(station):
    info = get_bus_info(station)
    return {
        "msg": "success",
        "data": info
    }


# http://localhost:5001/report/测试报告2022-06-13-19-05-25.html
@app.route('/report/<file_name>')
def get_report(file_name):
    file_path = pathlib.Path(__file__).parent / 'output' / file_name
    f = open(file_path, encoding='utf-8')
    report = f.read()
    f.close()
    return Response(report)


# http://127.0.0.1:5001/reports
@app.route('/reports')
def get_reports():
    report_names = discover_reports()
    return {
        "msg": "success",
        "data": [f"http://localhost:5001/report/{name}" for name in report_names]
    }


app.run(port=5001)
