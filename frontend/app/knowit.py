import webview
# import surveillance_class

# To pass custom settings to CEF, import and update settings dict
# See the complete set of options for CEF, here: https://github.com/cztomczak/cefpython/blob/master/api/ApplicationSettings.md
# from webview.platforms.cef import settings, browser_settings

surveillance(labels='labels.pickle', model='models/knowit_vgg16_Images_noaug_0.75x0.5d_N512x256.h5', video_source=0)

if __name__ == '__main__':
    webview.create_window('SIMS2022 - Knowit', 'http://localhost/sims/frontend/app/index.html', fullscreen=True)
    webview.start(gui='cef', debug=True)
