# @author Mragank Agarwal
import os, io, csv
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def fileUploadHome():
    # Render home.html template for root URL.
    return render_template('home.html')

@app.route('/validateCSV', methods=["POST"])
def validate_view():
    # Constants as per the assignment specifications.
    EXTENSIONS = ['csv']
    expectedRowCount = 10
    expectedColumnCount = 3

    # Fetch the file from the request.
    file = request.files

    # Check if the file does not exist and return appropriate response.
    if not file:
        return "No file was selected to be uploaded! Please select a file."

    # Fetch the file uploaded with name 'csvFile'.
    file = request.files['csvFile']

    # Fetch the uploaded file's extension.
    fileExtension = file.filename.split('.')[1]

    # Check if the extension is not .csv and return appropriate response.
    if fileExtension not in EXTENSIONS:
        return "Not a valid CSV file."

    # read the csv file by using the stream from io. Decoding set to UTF8.
    # csvInputStream is a StringIO Object.
    csvInputStream = io.StringIO(file.stream.read().decode("UTF8"))

    # Get the csv Object from the StringIO object.
    csvInput = csv.reader(csvInputStream)

    # Counter variables for csv validation
    rowCounter = 0
    columnCounter = 0

    # Print the data in the csv file to the terminal.
    for row in csvInput:
        rowCounter += 1
        if rowCounter > expectedRowCount:
            return "Failure! Number of rows is greater than " + str(expectedRowCount)
        columnCounter = 0
        for cell in row:
            columnCounter += 1
            if not cell:
                return "Failure! Found a missing cell in row " + str(rowCounter) + " and column " + str(columnCounter)
        if columnCounter != expectedColumnCount:
            return "Failure! Number of columns is not equal to " + str(expectedColumnCount) + " in row number " + str(rowCounter)
    if rowCounter != expectedRowCount:
        return "Failure! Number of rows is not equal to " + str(expectedRowCount)

    # Return String 'Success'
    return "Success! Valid CSV file."

if __name__ == "__main__":
    # Whitelist the application to be hosted on any IP with port as 5001 and DEBUG mode on.
    app.run(host='0.0.0.0', port=5001, debug=True)
