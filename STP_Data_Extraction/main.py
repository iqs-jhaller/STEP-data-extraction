print("Starting main.py script...")
from Step_GetAssemblyPNG import GetAssemblyPNG
print("Imported GetAssemblyPNG")
from Step_GetName import *
print("Imported Step_GetName")
from Step_GetTopology import *
print("Imported Step_GetTopology")
from Step_FileReader import StepFileReader
print("Imported StepFileReader")
from Step_GetGeometricFeatures import *
print("Imported Step_GetGeometricFeatures")
# from Step_GetGeometryInformation import *
# from Step_GetColor import *
from Step_GetColor_2 import get_part_colors
print("Imported get_part_colors")
from Step_GetProperties import *
print("Imported Step_GetProperties")
from utils import Utils
print("Imported Utils")
import pandas as pd
print("Imported pandas")
print("All imports successful!")


# sys.path.append(r"/home/fabian/Desktop/KoPro/Planning_Algorithm/Code/STP_DATA_EXTRACTION")
# sys.path.append(r"C:/Users/Varun Kaarthik/Documents/cad_data_extraction/STP_Data_Extraction/CAD/pick-up_heavy-duty_single-cab/") 

#filename = "/home/fabian/Desktop/KoPro/Planning_Algorithm/Code/STP_DATA_EXTRACTION/CAD/test_Uhlmann.stp"

#filename = "/home/fabian/Desktop/KoPro/Planning_Algorithm/Code/STP_DATA_EXTRACTION/CAD/Truck_komplett(stp)/pick-up_classic_king-size.stp"
# filename = "/home/fabian/Desktop/KoPro/Planning_Algorithm/Code/STP_DATA_EXTRACTION/CAD/fertiges_bauteil_asm_2.stp"
# filename = "/home/fabian/Desktop/KoPro/Planning_Algorithm/Code/STP_DATA_EXTRACTION/CAD/bt_asm.stp"
# filename = "C:/Users/Varun Kaarthik/Documents/cad_data_extraction/STP_Data_Extraction/CAD/bt_asm.stp"
# filename = "C:/Users/Varun Kaarthik/Documents/CAD/fertiges_bauteil_asm_2.stp"
filename = "C:/Users/Work/Desktop/CAD test/knife.step"

#filename = "/home/fabian/Desktop/KoPro/Planning_Algorithm/Code/STP_DATA_EXTRACTION/CAD/Wittenstein/Step-KoPro V1.stp"

if __name__ == "__main__":
    print("Entering main block...")
 
    '''############# Returns color values for every single component in the assembly. 
    ############# Returns dimension, physical properties and origins of every component in the assembly.'''

    print("Skipping color processing for now...")
    # Temporarily skip color processing to get to topology
    color_parts = []
    
    print("Creating mock data...")
    # Create empty mock data structures
    dimension_df = pd.DataFrame()
    physical_properties_df = pd.DataFrame()
    origins_df = pd.DataFrame()
    
    print("Proceeding to topology analysis...")
    print('No of color parts: ', len(color_parts))
    print('')

    print('Dimensions: \n ', dimension_df)
    print('')
    print('Physical properties: \n ', physical_properties_df)
    print('')
    print('Origin Locations: \n ', origins_df)
    print('')   

        
    '''##### PNG Images Generation ####'''
    print("Skipping PNG generation for now...")
    # Temporarily skip PNG generation to get to topology
    # #creates a new folder to save the images and returns its path. Named images_assembly_name
    # png_save_path = Utils.create_folder(filename, 'images_')
    # assembly = GetAssemblyPNG(StepFileReader(filename).getShape())
    # # Calls function to save step-by-step assembly images
    # assembly.saveAssemblySequenzToPNG(png_save_path, color_parts)
    # # Calls function to save step-by-step assembly images
    # assembly.SaveAssemblyPartsToPNG(png_save_path, color_parts)

    ''' #### Step file generation for every part in the assembly ####'''
    print("Skipping STEP file generation...")
    # Creates a folder and saves all individual parts of assembly as step files
    # step_save_path = Utils.create_folder(filename, 'step_')    
    # assembly.Export_Step_File(step_save_path, color_parts)

    print("Moving to topology analysis...")

    print("Creating generic component names based on topology...")
    # Skip the problematic getNamesComponents function for now
    # try:
    #     names = getNamesComponents(filename)
    #     print(f"Successfully got {len(names)} component names: {names}")
    # except Exception as e:
    #     print(f"Error getting component names: {e}")
    #     print("Creating generic names based on topology...")
        
    # Create generic names based on the topology levels
    shape = StepFileReader(filename).getShape()
    explorer = TopologyExplorer(shape)
    num_solids = explorer.number_of_solids()
    
    # We need names for: 1 compound (main assembly) + num_solids (components)
    names = ['MainAssembly'] + [f"Component_{i+1}" for i in range(num_solids)]
    print(f"Created {len(names)} names: {names}")
   
    print('Topology:', len(names))
    # get_Colors_to_Names(filename)

    print("Creating shape from STEP file...")
    shape = StepFileReader(filename).getShape()

    print("Creating topology explorer...")
    explorer = TopologyExplorer(shape)
    # explorer._loop_topo()
    
    print("Number of faces:", explorer.number_of_faces())
    print("Calling dump_topology_to_string...")
    print("Topology dump completed!")
    topo, shapes = dump_topology_to_string(shape)

    '''###### Prints the relationship matrix of the assembly #####'''

    print(f"Topology levels found: {len(topo)}")
    print(f"Shape objects found: {len(shapes)}")
    
    if len(names) > 0 and len(topo) > 0:
        print("Creating relationship matrix...")
        print(f"Topology levels: {topo}")
        print(f"Component names: {names}")
        
        # Check if we have a 3-level hierarchy (required by Utils.relationship_matrix)
        has_level_2 = any(level == 2 for level in topo)
        
        if has_level_2:
            matrix = Utils.relationship_matrix(names, topo)
            print('')
            print('Relationship Matrix:')
            print(matrix)
        else:
            print('')
            print('Relationship Matrix: Not applicable for flat assembly (no sub-assemblies)')
            
            # Create a simple 2-level relationship table instead
            relationships = []
            main_assembly = names[0] if topo[0] == 0 else "Unknown"
            level_1_components = [names[i] for i in range(len(topo)) if topo[i] == 1]
            
            for component in level_1_components:
                relationships.append([main_assembly, component])
            
            df = pd.DataFrame(relationships, columns=['Assembly', 'Component'])
            print('Simple Assembly-Component Relationships:')
            print(df)
        
        # Also create a simple parent-child relationship display
        print('\nSimple Assembly Structure:')
        print(f"Main Assembly: {names[0]}")
        level_1_components = [names[i] for i in range(len(topo)) if topo[i] == 1]
        for comp in level_1_components:
            print(f"  └─ {comp}")
    else:
        print("Skipping relationship matrix (no component names available)")
        print(f"Names count: {len(names)}, Topology count: {len(topo)}")
    
    print("\n=== TOPOLOGY ANALYSIS COMPLETE ===")
    # geometry = getGeometryInformation(filename)
