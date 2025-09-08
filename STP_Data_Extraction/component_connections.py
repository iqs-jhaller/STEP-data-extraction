"""
Component Connection Analysis
This module analyzes physical connections between components in a STEP assembly.
"""

import pandas as pd
from Step_GetTopology import TopologyExplorer
from Step_FileReader import StepFileReader
from OCC.Core.TopoDS import TopoDS_Solid
from OCC.Core.TopAbs import TopAbs_SOLID
import itertools

class ComponentConnectionAnalyzer:
    
    def __init__(self, step_file_path):
        """Initialize with a STEP file"""
        self.step_file = step_file_path
        self.shape = StepFileReader(step_file_path).getShape()
        self.explorer = TopologyExplorer(self.shape)
        self.solids = list(self.explorer.solids())
        
    def analyze_physical_connections(self):
        """
        Analyze which components physically connect to each other
        by finding shared edges and vertices between solids
        """
        connections = {}
        connection_matrix = pd.DataFrame(index=range(len(self.solids)), 
                                       columns=range(len(self.solids)), 
                                       data=0)
        
        # Compare each pair of solids
        for i, solid1 in enumerate(self.solids):
            for j, solid2 in enumerate(self.solids):
                if i != j:  # Don't compare solid with itself
                    connection_type = self._analyze_solid_connection(solid1, solid2)
                    if connection_type:
                        connection_matrix.iloc[i, j] = 1
                        connections[(i, j)] = connection_type
        
        return connection_matrix, connections
    
    def _analyze_solid_connection(self, solid1, solid2):
        """
        Check if two solids are connected by analyzing shared topology elements
        Returns connection type: 'face', 'edge', 'vertex', or None
        """
        explorer1 = TopologyExplorer(solid1)
        explorer2 = TopologyExplorer(solid2)
        
        # Get all faces, edges, and vertices from both solids
        faces1 = set(explorer1.faces())
        faces2 = set(explorer2.faces())
        
        edges1 = set(explorer1.edges()) 
        edges2 = set(explorer2.edges())
        
        vertices1 = set(explorer1.vertices())
        vertices2 = set(explorer2.vertices())
        
        # Check for shared faces (strongest connection)
        shared_faces = faces1.intersection(faces2)
        if shared_faces:
            return 'face'
            
        # Check for shared edges (medium connection)
        shared_edges = edges1.intersection(edges2)
        if shared_edges:
            return 'edge'
            
        # Check for shared vertices (weakest connection)
        shared_vertices = vertices1.intersection(vertices2)
        if shared_vertices:
            return 'vertex'
            
        return None
    
    def get_adjacency_report(self):
        """Generate a detailed report of component connections"""
        matrix, connections = self.analyze_physical_connections()
        
        report = []
        for (i, j), conn_type in connections.items():
            report.append({
                'Component_A': f'Component_{i+1}',
                'Component_B': f'Component_{j+1}',
                'Connection_Type': conn_type,
                'Connected': True
            })
        
        return pd.DataFrame(report)
    
    def print_connection_summary(self):
        """Print a summary of component connections"""
        matrix, connections = self.analyze_physical_connections()
        
        print(f"=== COMPONENT CONNECTION ANALYSIS ===")
        print(f"Total Components: {len(self.solids)}")
        print(f"Total Connections: {len(connections)}")
        
        if connections:
            print("\nConnection Details:")
            for (i, j), conn_type in connections.items():
                print(f"  Component_{i+1} ↔ Component_{j+1} (via {conn_type})")
        else:
            print("\nNo physical connections detected between components.")
            print("Components may be separate parts or the analysis method needs refinement.")
        
        return matrix

# Example usage function
def analyze_step_file_connections(step_file_path):
    """Analyze connections in a STEP file and return results"""
    analyzer = ComponentConnectionAnalyzer(step_file_path)
    
    # Get connection matrix and summary
    connection_matrix = analyzer.print_connection_summary()
    
    # Get detailed report
    adjacency_report = analyzer.get_adjacency_report()
    
    print(f"\nConnection Matrix:")
    print(connection_matrix)
    
    if not adjacency_report.empty:
        print(f"\nAdjacency Report:")
        print(adjacency_report)
    
    return connection_matrix, adjacency_report

if __name__ == "__main__":
    # Test with the knife.step file
    step_file = "C:/Users/Work/Desktop/CAD test/knife.step"
    analyze_step_file_connections(step_file)
