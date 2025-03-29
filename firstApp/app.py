from flask import Flask, render_template , request

app = Flask(__name__,template_folder='templates')

@app.route('/')
def index():
    myValue = 10
    myList = [1,2,3,4,5]
    return render_template('index.html',myValue=myValue,myList=myList)

@app.route('/hello')
def hello():
    return '<h4>Hello, World!, From Hello Route !<h4>'

@app.route('/greet/<name>')
def user(name):
    return f'<h3>Hello, {name}!<h3>'

@app.route('/add/<int:num1>/<int:num2>')
def add(num1,num2):
    return f'<h3>Sum of {num1} and {num2} is = {num1+num2}<h3>'

"""
handle the url parameters in defferent ways
"""
@app.route('/handle_url_params')
def handle_url_params():
    if 'name' in request.args.keys() and 'age' in request.args.keys():
        name = request.args.get('name')
        age = request.args.get('age')
        return f'<h3>Hello, {name}! Your age is {age}<h3>'
    else:
        return '<h3>Ooohh! Invalid URL Parameters<h3>'
    

@app.route('/post',methods=['GET','POST'])
def post():
    if request.method == 'POST':
        return '<h3>POST Request<h3>'
    elif request.method == 'GET':
        return '<h3>GET Request<h3>'
    else:
        return '<h3>Invalid Request<h3>'   
    


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')