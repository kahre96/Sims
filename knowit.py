import sys
sys.path.append('./AI')
from threading import Thread
from surveillance_class import surveillance
import webview

def surveillanceTask(theLabels, theModel, theSource):
    surveillance(theLabels, theModel, theSource)

if __name__ == '__main__':
    Thread(target = surveillanceTask, args=('AI/labels.pickle', 'AI/models/knowit_vgg16_Images_noaug_0.75x0.5d_N512x256.h5', 0)).start()

    webview.create_window('SIMS2022 - Knowit', 'http://localhost/sims/frontend/app/index.html', fullscreen=True)
    webview.start(gui='cef', debug=True)
