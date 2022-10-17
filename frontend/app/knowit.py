import webview

# To pass custom settings to CEF, import and update settings dict
# See the complete set of options for CEF, here: https://github.com/cztomczak/cefpython/blob/master/api/ApplicationSettings.md
# from webview.platforms.cef import settings, browser_settings

if __name__ == '__main__':
    webview.create_window('SIMS2022 - Knowit', 'http://localhost/sims/frontend/app/index.html', fullscreen=True)
    webview.start(gui='cef', debug=True)
