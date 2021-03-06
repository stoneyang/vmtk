#!/usr/bin/env python

## Program:   VMTK
## Module:    $RCSfile: vmtkimagemorphology.py,v $
## Language:  Python
## Date:      $Date: 2006/07/17 09:53:14 $
## Version:   $Revision: 1.8 $

##   Copyright (c) Luca Antiga, David Steinman. All rights reserved.
##   See LICENCE file for details.

##      This software is distributed WITHOUT ANY WARRANTY; without even 
##      the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
##      PURPOSE.  See the above copyright notices for more information.


import vtk
from vmtk import vtkvmtk
import sys

import pypes

vmtkimagemorphology = 'vmtkImageMorphology'

class vmtkImageMorphology(pypes.pypeScript):

    def __init__(self):

        pypes.pypeScript.__init__(self)
        
        self.Image = None

        self.Grayscale = 1
        self.BallRadius = [1,1,1]
        self.Operation = 'closing'

        self.SetScriptName('vmtkimagemorphology')
        self.SetScriptDoc('apply binary or grayscale morphology filter to the input image')
        self.SetInputMembers([
            ['Image','i','vtkImageData',1,'','the input image','vmtkimagereader'],
            ['BallRadius','radius','int',3,'(0,)','the radius of the structuring element'],
            ['Operation','operation','str',1,'["dilate","erode","open","close"]','the morphological operation to perform'],
            ['Grayscale','grayscale','bool',1,'','perform binary or grayscale morphology']
            ])
        self.SetOutputMembers([
            ['Image','o','vtkImageData',1,'','the output image','vmtkimagewriter']
            ])

    def Execute(self):

        if self.Image == None:
            self.PrintError('Error: No input image.')

        if self.Grayscale:
            morphologyFilter = vtkvmtk.vtkvmtkGrayscaleMorphologyImageFilter()
            if self.Operation == 'close':
                morphologyFilter.SetOperationToClose()
            elif self.Operation == 'open':
                morphologyFilter.SetOperationToOpen()
            elif self.Operation == 'dilate':
                morphologyFilter.SetOperationToDilate()
            elif self.Operation == 'erode':
                morphologyFilter.SetOperationToErode()

            cast = vtk.vtkImageCast()
            cast.SetInput(self.Image)
            cast.SetOutputScalarTypeToFloat()
            cast.Update()

            morphologyFilter.SetInput(cast.GetOutput())

        morphologyFilter.SetBallRadius(self.BallRadius)
        morphologyFilter.Update()

        self.Image = morphologyFilter.GetOutput()


if __name__=='__main__':

    main = pypes.pypeMain()
    main.Arguments = sys.argv
    main.Execute()
