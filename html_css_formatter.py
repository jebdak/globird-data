def HEADER(date):
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Globird Data Summary</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f6f8;
            padding: 30px;
        }

        h1 {
            color: #333;
        }

        table {
            border-collapse: collapse;
            width: 60%;
            background-color: white;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        th {
            background-color: #2c7be5;
            color: white;
            padding: 12px;
            text-align: left;
        }

        td {
            padding: 12px;
            border: 1px solid #ddd;
        }

        tr:nth-child(even) {
            background-color: #f8f9fa;
        }

        tr:hover {
            background-color: #eaf2ff;
        }
    </style>
</head>

<body>
    <h1>""" + f"Globird Data Summary - {date}" + """</h1>

    <table>
        <tr>
            <th>Hour</th>
            <th>Usage (kWh)</th>
            <th>Cost (cents)</th>
        </tr>
"""


def FOOTER(utotal,ctotal):
    return f"""
    <tr>
        <th>TOTALS</th>
        <th>{utotal} kWh</th>
        <th>$ {ctotal}</th>
    <tr>
    </table>
</body>
</html>
"""