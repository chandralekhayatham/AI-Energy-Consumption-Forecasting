from flask import Flask, render_template
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/"src"))
from predict import predict_next_hour
app=Flask(__name__)
@app.route("/",methods=["GET","POST"])
def home():
    result=error=None
    from flask import request
    if request.method=="POST":
        try: result=predict_next_hour()
        except Exception as e: error=str(e)
    return render_template("index.html",result=result,error=error)
if __name__=="__main__": app.run(debug=False)
