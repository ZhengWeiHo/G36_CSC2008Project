from website import create_app
from flask import render_template

app = create_app()

@app.route('/main')
def main():
     return render_template('main.html')

@app.route('/eligibility')
def appointment():
    return render_template('eligibility_check.html')




if __name__ == '__main__':
    app.run(debug=True)