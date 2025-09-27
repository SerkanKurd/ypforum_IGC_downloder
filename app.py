from flask import (Flask,
                   render_template,
                   request,
                   send_from_directory)
import get_igc_files


app = Flask(__name__)
# app.config['TEMPLATES_AUTO_RELOAD'] = True
# app.jinja_env.cache = {}


@app.route("/", methods=["GET", "POST"])
def get_files():
    igc_url = ""
    downloaded_files = []
    if request.method == "POST":
        igc_url = request.form.get("igc_url")
        if igc_url:
            downloaded_files = get_igc_files.main(igc_url)
    return render_template("get_igc_files.html", igc_url=igc_url, files=downloaded_files)


@app.route("/downloads/<path:filename>")
def download_file(filename):
    return send_from_directory("downloads", filename, as_attachment=True)


if __name__ == "__main__":
    # app.run(debug=True, use_reloader=True, host="127.0.0.1", port=8000)
    app.run(debug=False, use_reloader=False, host="0.0.0.0", port=8000)
