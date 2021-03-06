# -*- coding:utf-8 -*-
#
# Copyright © 2020 cGIfl300
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the “Software”),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import gettext
import os
import time
from tkinter import *

import pygame
import pygame.camera
import pyperclip
import pyzbar.pyzbar as pyzbar
from PIL import Image

from configuration import *
from image_set import image_set

# import pytesseract

pygame.init()

fr = gettext.translation('base', localedir=repertoire_script + 'locales', languages=[langue_appli], fallback=False)
fr.install()
_ = fr.gettext
ngettext = fr.ngettext


class baReader(Tk):
    ''' Interface graphique ...
    '''

    def __init__(self, debug=False):
        Tk.__init__(self)
        self.debug = debug
        try:
            pygame.camera.init()
        except:
            print('You must have a camera!')
            exit(0)
        self.camlist = pygame.camera.list_cameras()
        self.videosize = (640, 480)
        self.camera = self.camlist[0]
        self.videodevice = pygame.camera.Camera(self.camera, self.videosize)
        self.videofilename = 'capture.jpg'

    def interface(self):
        ''' Interface de la fenêtre
        '''
        self.title(_('baReader'))
        self.label001 = Canvas(self,
                               bg=couleur_fond)

        ''' Implantation des composants
        '''
        self.label001.pack(expand=True,
                           fill=BOTH)
        self.logo = image_set(self.label001, 'images{}logo'.format(os.sep))

        ''' Binding
        '''
        self.after(500, self.do_scan)

    def do_scan(self):
        display = pygame.display.set_mode(self.videosize, 0)
        pygame.display.iconify()
        camera = pygame.camera.Camera(self.camera, self.videosize)
        camera.start()
        screen = pygame.surface.Surface(self.videosize, 0, display)
        Locked = True

        while Locked:
            img = camera.get_image(screen)
            pygame.image.save(img, repertoire_script + 'data{}image.jpg'.format(os.sep))
            img = Image.open(repertoire_script + 'data{}image.jpg'.format(os.sep))
            codes = pyzbar.decode(img)
            if len(codes) > 0:
                Locked = False
            # text = pytesseract.image_to_string(Image.open(repertoire_script + 'data{}image.jpg'.format(os.sep)))
            # if len(text) > 0:
            #    Locked = False
            time.sleep(0.5)
        os.remove(repertoire_script + 'data{}image.jpg'.format(os.sep))
        camera.stop()

        for l in codes:
            donnees = l.data.decode('utf-8')
            print(_('Données du code: {}'.format(donnees)))
        # donnees = '{}\n{}'.format(donnees, text)
        try:
            pyperclip.copy(donnees)
        except:
            if self.debug:
                print(_('Impossible de copier le texte.'))

        self.destroy()

    def run(self):
        self.interface()
        self.mainloop()


if __name__ == '__main__':
    App = baReader()
    App.run()
