import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import VirtualPainter
import time
import os
import AiMouse as mouse
from fpdf import FPDF
import glob





VirtualPainter.virtual_painter_function(True)


pdf = FPDF()



for image in glob.glob('K:/ASU/Second Term/New folder/Air-Drawing-Project-main/*.jpg'):
    pdf.add_page()
    pdf.image(image,x=20,y=50,w=180,h=190)
pdf.output("Doc1.pdf", "F")







