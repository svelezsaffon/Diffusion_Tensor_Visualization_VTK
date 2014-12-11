__author__ = 'santiago'



import Tkinter as tk
import vtk
import sys

class ImageModification(object):

    def __init__(self,dti,vol_geo):


        self.print_counter=0
        ren = vtk.vtkRenderer()

        self.dti_reader = vtk.vtkStructuredPointsReader()
        self.dti_reader.SetFileName(dti)



        self.vol_reader = vtk.vtkStructuredPointsReader()
        self.vol_reader.SetFileName(vol_geo)


        self.geo_Mapper=vtk.vtkPolyDataMapper()
        self.geo_Mapper.SetInputConnection(self.dti_reader.GetOutputPort())



        self.arrowColor = vtk.vtkColorTransferFunction()

        self.update_look_up_table()




        #------------NEW CODE BEGINS HERE----------


        for i in range(0,1000):
            ren.AddActor(self.create_hyper_stream_line(i,i,i))

        ren.AddVolume(self.create_volume_rendering())



        #------------NEW CODE ENDS HERE------------



        #Add renderer to renderwindow and render
        self.renWin = vtk.vtkRenderWindow()
        self.renWin.AddRenderer(ren)
        self.renWin.SetSize(1920, 1080)

        iren = vtk.vtkRenderWindowInteractor()
        iren.SetRenderWindow(self.renWin)

        iren.AddObserver('RightButtonPressEvent', self.capture_image, 1.0)


        # Scalar Bar actor
        scalar_bar = vtk.vtkScalarBarActor()
        scalar_bar.SetOrientationToHorizontal()
        scalar_bar.SetLookupTable(self.arrowColor)
        scalar_bar.SetTitle("Color map")
        scalar_bar.SetLabelFormat("%5.2f")
        scalar_bar.SetMaximumHeightInPixels(300)
        scalar_bar.SetMaximumWidthInPixels(100)

        # Scalar Bar Widget
        scalar_bar_widget = vtk.vtkScalarBarWidget()
        scalar_bar_widget.SetInteractor(iren)
        scalar_bar_widget.SetScalarBarActor(scalar_bar)
        scalar_bar_widget.On()




        ren.SetBackground(0,0,0)
        self.renWin.Render()
        iren.Start()

    def create_volume_rendering(self):

        opacityfunction=vtk.vtkPiecewiseFunction()

        opacityfunction.AddPoint(0,0.0)
        opacityfunction.AddPoint(0.4,0.1)
        opacityfunction.AddPoint(1,0.02)
        opacityfunction.AddPoint(1.5,0.03)




        volproperty=vtk.vtkVolumeProperty()
        volproperty.SetColor(self.arrowColor)
        volproperty.SetScalarOpacity(opacityfunction)
        volproperty.ShadeOn()
        volproperty.SetInterpolationTypeToLinear()


        volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
        volumeMapper.SetInputConnection(self.vol_reader.GetOutputPort())
        volumeMapper.SetSampleDistance(0.01)

        volume = vtk.vtkVolume()
        volume.SetMapper(volumeMapper)
        volume.SetProperty(volproperty)

        return volume


    def update_look_up_table(self):

        self.arrowColor.AddRGBPoint(0, 1.0, 0.0, 0.0)

        self.arrowColor.AddRGBPoint(0.6, 0.0, 1.0, 0.0)

        self.arrowColor.AddRGBPoint(1.5, 0.0, 0.0, 1.0)

    def create_hyper_stream_line(self,x,y,z):



        streamline = vtk.vtkHyperStreamline()
        streamline.SetInputConnection(self.dti_reader.GetOutputPort())
        streamline.SetStartPosition(x,y,z)
        streamline.SetIntegrationStepLength(0.05)
        #streamline.SetMaximumPropagationDistance(1000)
        #streamline.SetIntegrationEigenvectorToMajor()
        #streamline.SetRadius(0.1)
        streamline.LogScalingOn()
        streamline.SetIntegrationDirectionToIntegrateBothDirections()
        #streamline.TubeWrappingOff()


        streamlineMapper = vtk.vtkPolyDataMapper()
        streamlineMapper.SetInputConnection(streamline.GetOutputPort())
        streamlineMapper.SetLookupTable(self.arrowColor)

        streamline_actor = vtk.vtkActor()
        streamline_actor.SetMapper(streamlineMapper)
        streamline_actor.VisibilityOn()

        return streamline_actor


    def capture_image(self,obj,eve):
        self.renWin.Render()
        self.w2i = vtk.vtkWindowToImageFilter()
        self.w2i.SetInput(self.renWin)
        self.writer = vtk.vtkJPEGWriter()
        self.writer.SetInputConnection(self.w2i.GetOutputPort())
        self.writer.SetFileName(`self.print_counter` + "vectorscreen.jpg");
        self.print_counter =1 + self.print_counter
        self.writer.Write()



if __name__ == '__main__':
    dti =sys.argv[0:][1]
    vol_geo =sys.argv[0:][2]

    ImageModification(dti,vol_geo)