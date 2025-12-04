from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# Flag stored in environment
os.environ['FLAG'] = 'UbigCTF{3sTe1err_Es8u4H_T3mpe_!nd0m13}'

@app.route('/', methods=['GET', 'POST'])
def index():
    name = request.form.get('name', '') if request.method == 'POST' else ''
    
    # VULNERABILITY: User input is directly concatenated into template string
    # This allows SSTI exploitation
    template = '''
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
            <input type="text" name="name" placeholder="Nama Anda">
            <button type="submit">Render!</button>
        </form>
        ''' + (f'''
        <div class="result">
            <h3>Hasil:</h3>
            <p>Halo, {name}! Selamat datang di Template Renderer.</p>
        </div>
        ''' if name else '') + '''
    </div>
</body>
</html>
    '''
    
    # The vulnerability is here: rendering template with user input embedded
    return render_template_string(template)

if __name__ == '__main__':
    app.run(debug=False)