@app.route('/')
def home():
    return render_template('my_file.html')  # <-- Теперь он сразу откроет ваш новый файл!
