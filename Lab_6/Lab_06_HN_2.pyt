import time
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
        # Original Project Name.
        param0 = arcpy.Parameter(
            displayName="Input ArcGIS Pro Project Name",
            name="aprxInputName",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )

        # Layer to classify
        param1 = arcpy.Parameter(
            displayName="Layer To Classify",
            name="LayerToClassify",
            datatype="GPLayer",
            parameterType="Required",
            direction="Input"
        )

        # Output folder location
        param2 = arcpy.Parameter(
            displayName="Output Location",
            name="OutputLocation",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )

        # Output project name
        param3 = arcpy.Parameter(
            displayName="Output Project Name",
            name="OutputProjectName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )

        return [param0, param1, param2, param3]

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal validation."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool parameter."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # Define Progressor Variables
        readTime = 3  # the time for users to read the progress
        start = 0  # beginning position of the progressor
        max = 99  # end position (ensures smooth increments)
        step = 33  # the progress interval

        # Setup Progressor
        arcpy.SetProgressor("step", "Validating Project File...", start, max, step)
        time.sleep(readTime)

        # Add message to results pane
        arcpy.AddMessage("Validating Project File...")

        # Load the project file
        project = arcpy.mp.ArcGISProject(parameters[0].valueAsText)

        # Get the first map in the project
        campus = project.listMaps('Map')[0]

        # Increment Progressor
        arcpy.SetProgressorPosition(start + step)
        arcpy.SetProgressorLabel("Finding Your Map Layer...")
        time.sleep(readTime)
        arcpy.AddMessage("Finding Your Map Layer...")

        # Loop through the layers
        for layer in campus.listLayers():
            if layer.isFeatureLayer:
                symbology = layer.symbology
                if hasattr(symbology, 'renderer') and layer.name == parameters[1].valueAsText:
                    # Increment Progressor
                    arcpy.SetProgressorPosition(start + step * 2)
                    arcpy.SetProgressorLabel("Calculating and classifying...")
                    time.sleep(readTime)
                    arcpy.AddMessage("Calculating and classifying...")

                    # Apply Graduated Colors Renderer
                    symbology.updateRenderer('GraduatedColorsRenderer')
                    symbology.renderer.classificationField = "Shape_Area"
                    symbology.renderer.breakCount = 5
                    symbology.renderer.colorRamp = project.listColorRamps('Oranges (5 Classes)')[0]

                    # Apply the symbology
                    layer.symbology = symbology

                    arcpy.AddMessage("Finished Generating Layer...")
                    break
        else:
            arcpy.AddWarning("No matching layer found!")

        # Increment Progressor
        arcpy.SetProgressorPosition(start + step * 3)
        arcpy.SetProgressorLabel("Saving...")
        time.sleep(readTime)
        arcpy.AddMessage("Saving...")

        # Save the project copy
        output_path = parameters[2].valueAsText + "\\" + parameters[3].valueAsText + ".aprx"
        project.saveACopy(output_path)
        
        arcpy.AddMessage(f"Project saved to {output_path}")
        return