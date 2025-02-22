import arcpy

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (The name of the toolbox is the name of the .pyt file)."""
        self.label = "Lab_06_HN.pyt"
        self.alias = "Lab_06_HN.pyt"
        # List of tool classes associated with this toolbox
        self.tools = [GraduatedColorsRenderer]

class GraduatedColorsRenderer(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "graduatedcolor"
        self.description = "Create a graduated color map based on a specific attribute of a layer"
        self.canRunInBackground = False
        self.category = "MapTools"

    def getParameterInfo(self):
        #Original Project Name.
        param0 = arcpy.Parameter(
            displayName="Input ArcGIS Pro Project Name",
            name="aprxInputName",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )

        # which layer you want to classify to create a color map
        param1 = arcpy.Parameter(
            displayName="Layer To Classify",
            name="LayerToClassify",
            datatype="GPLayer",
            parameterType="Required",
            direction="Input"
        )

        #output folder location
        param2 = arcpy.Parameter(
            displayName="Output Location",
            name="OutputLocation",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )

        #output project name
        param3 = arcpy.Parameter(
            displayName="Output Project Name",
            name="OutputProjectName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        params = [param0, param1, param2, param3]
        return params
    
    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        #Define Progressor Variables
        readTime = 3 #the time for users to read the progress
        start = 0 #beginning position of the progressor
        max = 100 #end position
        step = 33 #the progress interval to move the progressor along

        #Setup Progressor
        arcpy.SetProgressor("step", "Validating Project File...", start, max, step)
        time.sleep(readTime) #pause the execution for 2.5 seconds

        #Add message to the results pane
        arcpy.AddMessage("Validating Project File...")

        #Project File
        project = arcpy.mp.ArcGISProject(parameters[0].valueAsText)

        #Grabs the first instance of a map from the .aprx
        campus = project.listMaps('Map')[0]

        #Increment Progressor
        arcpy.SetProgressorPosition(start + step) #now is 33% completed
        arcpy.SetProgressorLabel("Finding Your Map Layer...")
        time.sleep(readTime)
        arcpy.AddMessage("Finding Your Map Layer...")

        #Loop through the layers of the map
        for layer in campus.listLayers():
            #Check if the layer is a feature layer
            if layer.isFeatureLayer:
                #copy the layers symbology
                symbology = layer.symbology
                #make sure the layer has renderer attribute
                if hasattr(symbology, 'renderer'):
                    #check Layer name
                    if layer.name == parameters[1].valueAsText: #check if the layer name match the input layer

                        #Increment Progessor
                        arcpy.SetProgessorPosition(start + step*2) #now is 66% complete
                        arcpy.SetProgressorLabel("Calculating and classifying...")
                        time.sleep(readTime)
                        arpy.AddMessage("Calculating and classifying...")
                        #Update the copy's renderer to "Graduated Colors Renderer"
                        symbology.updateRenderer('GraduatedColorsRenderer')
                        #tell arcpy which field we want to base our chloropleth off of
                        symbology.renderer.classificationField("Shape_Area")

                        #set how many classes we'll have for the map
                        symbology.renderer.breakCount = 5

                        #Set color ramp
                        symbology.renderer.colorRamp =project.listColorRamps('Oranges (5 Classes)')[0]

                        #Set the Layer's Actual symbology level equal to the copy's
                        layer.symbology = symbology

                        arcpy.AddMessage("Finish Generating Layer...")
                    else:
                        print("NO layers found")

            #Increment Progessor
            arcpy.SetProgessorPosition(start + step*3) #now 99% completed
            arcpy.SetProgressorLabel("Saving...")
            time.sleep(readTime)
            arcpy.AddMessage("Saving...")

            project.saveACopy(parameters[2].valueAsText + ".aprx")
            #Param 2 is the folder location Param 3 is the name of the new project
            return