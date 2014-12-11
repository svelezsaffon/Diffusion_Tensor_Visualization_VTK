__author__ = 'santiago'



import Tkinter as tk
import vtk
import sys

class ImageModification(object):

    def __init__(self,dti):


        self.print_counter=0
        ren = vtk.vtkRenderer()

        self.dti_reader = vtk.vtkStructuredPointsReader()
        self.dti_reader.SetFileName(dti)


        self.geo_Mapper=vtk.vtkPolyDataMapper()
        self.geo_Mapper.SetInputConnection(self.dti_reader.GetOutputPort())

        #glyph actor
        #geo_actor = vtk.vtkActor()
        #geo_actor.SetMapper(geo_Mapper)

        #ren.AddActor(geo_actor)

        self.arrowColor = vtk.vtkColorTransferFunction()

        self.update_look_up_table()


        self.plane1=None
        for i in range(0,3):
            if i==0:
                x=130.0
                y=0.0
                z=0.0
            if i==1:
                x=130.0
                y=130.0
                z=0.0
            if i==2:
                x=0.0
                y=0.0
                z=65.0

            plane_mapper=self.create_cut_acto_plane(x,y,z,i)
            ren.AddActor(self.create_glyph(plane_mapper))




        #Add renderer to renderwindow and render
        self.renWin = vtk.vtkRenderWindow()
        self.renWin.AddRenderer(ren)
        self.renWin.SetSize(1920, 1080)

        iren = vtk.vtkRenderWindowInteractor()
        iren.SetRenderWindow(self.renWin)

        iren.AddObserver('RightButtonPressEvent', self.capture_image, 1.0)

        """
        #Slider 1
        sliderRep1=vtk.vtkSliderWidget()
        sliderRep1.SetInteractor(iren)
        sliderRep1.SetRepresentation(self.create_color_slider("X-Position",0.02,0.15,0,220))
        sliderRep1.SetEnabled(True)
        sliderRep1.AddObserver("InteractionEvent", self.change_iso)
        """


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

    def change_iso(self,obj,event):

      self.plane1.SetOrigin(obj.GetSliderRepresentation().GetValue(),0,0)


    def create_color_slider(self,name,left,right,down,up,default_value=0.02):

        slider=vtk.vtkSliderRepresentation2D()
        slider.SetMinimumValue(down)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        slider.SetMaximumValue(up)
        slider.SetValue(default_value)
        slider.SetTitleText(name)
        slider.SetLabelFormat("%5.2f")

        slider.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
        slider.GetPoint1Coordinate().SetValue(left, 0.1)

        slider.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
        slider.GetPoint2Coordinate().SetValue(right, 0.1)

        return slider

    def update_look_up_table(self):

        self.arrowColor.AddRGBPoint(0, 1.0, 0.0, 0.0)

        self.arrowColor.AddRGBPoint(60, 0.0, 1.0, 0.0)

        self.arrowColor.AddRGBPoint(120, 0.0, 0.0, 1.0)

    def create_glyph(self,plane_mapper):


        ptMask = vtk.vtkMaskPoints()
        ptMask.SetInputConnection(plane_mapper.GetOutputPort())
        ptMask.SetOnRatio(10)
        ptMask.RandomModeOn()


        arrows = vtk.vtkSphereSource()
        arrows.SetRadius(150)
        arrows.SetThetaResolution(35)
        arrows.SetPhiResolution(35)


        #in here we do the glyohs

        glyph = vtk.vtkTensorGlyph()
        glyph.SetSourceConnection(arrows.GetOutputPort())
        glyph.SetInputConnection(ptMask.GetOutputPort())
        glyph.SetScaleFactor(10)
        glyph.ColorGlyphsOn()
        glyph.SetColorModeToEigenvector()


        normals = vtk.vtkPolyDataNormals()
        normals.SetInputConnection(glyph.GetOutputPort())


        #Glyph mapper
        gly_mapper = vtk.vtkPolyDataMapper()
        gly_mapper.SetInputConnection(normals.GetOutputPort())
        gly_mapper.SetLookupTable(self.arrowColor)

        #glyph actor
        gly_actor = vtk.vtkActor()
        gly_actor.SetMapper(gly_mapper)

        return gly_actor

    def create_cut_acto_plane(self,xpos,ypos,zpos,plane_id):
        #vtk plane
        plane=vtk.vtkPlane()
        plane.SetOrigin(xpos,ypos,zpos)

        if plane_id==0:
            plane.SetNormal(1,0,0)
        if plane_id==1:
            plane.SetNormal(0,1,0)
        if plane_id==2:
            plane.SetNormal(0.0,0.0,1)

        #create cutter
        cutter=vtk.vtkCutter()
        cutter.SetCutFunction(plane)
        cutter.SetInputConnection(self.dti_reader.GetOutputPort())
        cutter.Update()


        #probe filter for the cutting plane
        probe_filter=vtk.vtkProbeFilter()
        probe_filter.SetInputConnection(cutter.GetOutputPort())
        probe_filter.SetSourceConnection(self.dti_reader.GetOutputPort())


        return probe_filter

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

    ImageModification(dti)