from flask import Flask, request, render_template
from website import create_app  # Assuming create_app is in website/__init__.py
from website.views import views  


app = create_app()


if 'views' not in app.blueprints:  
    app.register_blueprint(views, url_prefix="/")


@app.route('/project-dashboard', methods=['POST'])
def project_dashboard():
    
    form_data = request.form
    
    return render_template('project-dashboard.html', data=form_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
