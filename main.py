# Prepare libraries
from flask import Flask, render_template, request
import warnings
import ilakkanam as ik
import sandhi_checker as sc
import codecs

# Stop not important warnings and define the main flask application
warnings.filterwarnings("ignore")
app = Flask(__name__)

# Application home page
@app.route("/")
def home():
    return render_template("index.html", page_title="Tamil Grammar Checker")



@app.route("/", methods=['POST'])
def get_text():
    text = request.form['tamilText']
    

    if 'a' <= text[0] <= "z" or 'A' <= text[0] <='Z':
        final = "Please enter only Tamil Text"
    else:
        words = ik.get_words(text)
        result,x = sc.check_sandhi(words)
        final = u' '.join(result)
    return render_template("index.html", page_title="Tamil Grammar Checker", output=final)


# Start the application on local server
if __name__ == "__main__":
    app.run(debug=False)