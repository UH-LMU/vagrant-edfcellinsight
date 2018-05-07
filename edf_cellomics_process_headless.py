import glob
import os.path
import sys

from ij import IJ, ImagePlus, ImageStack, WindowManager

from edf import EdfComplexWavelets, PostProcessing, Tools
from edfgui import ExtendedDepthOfField, Parameters
from imageware import Builder, ImageWare
from optparse import OptionParser


# 
REAL_WAVELETS = 2
COMPLEX_WAVELETS = 3

# EDF parameters
params = Parameters()
params.setQualitySettings(params.QUALITY_HIGH)
params.nScales = 10


#
# this is a reproduction of method "process" in edfgui.ExtendedDepthOfField.
#
def process(imp):
    isExtended = False
    waveletMethod = params.edfMethod == REAL_WAVELETS \
        or params.edfMethod == COMPLEX_WAVELETS

    stackConverted = None
    impConverted = None
    impBW = imp

    if params.color:
        print "Color support not ready yet"
        sys.exit(1)

    imageStack = Builder.wrap(impBW)

    scaleAndSizes = []
    nx = imageStack.getWidth()
    ny = imageStack.getHeight()

    nScalesAndSize = Tools.computeScaleAndPowerTwoSize(nx,ny);
    nScales = nScalesAndSize[0];
    params.maxScales = nScales;
    params.setQualitySettings(params.QUALITY_HIGH)

    if waveletMethod:
        if not Tools.isPowerOf2(nx) or not Tools.isPowerOf2(ny):
            scaleAndSizes = Tools.computeScaleAndPowerTwoSize(nx,ny)
            print "Extend images to "+ scaleAndSizes[1]+ "x" + scaleAndSizes[2] + " pixels..."
            imageStack = Tools.extend(imageStack, scaleAndSizes[1], scaleAndSizes[2])
            isExtended = True

    ima = []
    
    if params.edfMethod == COMPLEX_WAVELETS:
        edf = EdfComplexWavelets(params.daubechielength,params.nScales,params.subBandCC,params.majCC)
        ima = edf.process(imageStack)
    else:
        print "Method not supported yet, sorry!"
        sys.exit(1)

    # crop to original images    
    if waveletMethod and isExtended:
        imageStack = Tools.crop(imageStack, nx, ny)
        ima[0] = Tools.crop(ima[0],nx,ny)
        ima[1] = Tools.crop(ima[0],nx,ny)

    if params.reassignment:
        ima[1] = PostProcessing.reassignment(ima[0],imageStack)

    if params.doDenoising and not waveletMethod:
        print "option not supported: doDenoising"
        sys.exit(1)

    impComposite = ImagePlus("Output", ima[0].buildImageStack())    
    return impComposite


parser = OptionParser()
parser.add_option('-o','--output', help='edf.tiff')
options,args = parser.parse_args()

print options.output
print args

# check input image size
tmp = ImagePlus(args[0])

# put input images in a stack
stack = ImageStack(tmp.getWidth(), tmp.getHeight())
for a in args:
    imp = ImagePlus(a)
    stack.addSlice(imp.getProcessor())
imp = ImagePlus("focus stack", stack)
IJ.saveAsTiff(imp,options.output.replace("_edf_","_edf_stack_"))

#sys.exit()
# process input
output = process(imp)

# save output
IJ.saveAsTiff(output,options.output)

# close images
output.close()
imp.close()
