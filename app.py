from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# Flag stored in environment
os.environ['FLAG'] = 'UbigCTF{3sTe1err_Es8u4H_T3mpe_!nd0m13}'

BASE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Template Renderer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 2px solid #ddd;
            border-radius: 5px;
        }
        button {
            background: #007bff;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background: #0056b3;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            background: #e9ecef;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 Template Renderer</h1>
        <p>Masukkan nama Anda untuk render template!</p>
        <form method="POST">
            <input type="text" name="name" placeholder="Nama Anda" value="%s">
            <button type="submit">Render!</button>
        </form>
        %s
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    name = ''
    result_html = ''
    
    if request.method == 'POST':
        name = request.form.get('name', '')
        
        if name:
            # VULNERABILITY: User input is directly embedded in template string
            # This creates SSTI because the template is rendered with user input
            result_template = '''
            <div class="result">
                <h3>Hasil:</h3>
                <p>Halo, ''' + name + '''! Selamat datang di Template Renderer.</p>
            </div>
            '''
            result_html = render_template_string(result_template)
    
    # Safe rendering of base template
    final_html = BASE_TEMPLATE % (name, result_html)
    return final_html

if __name__ == '__main__':
    app.run(debug=False)