"""
Realistic 3D Heart Model Viewer
================================

INSTALLATION INSTRUCTIONS:
--------------------------
Install required libraries using pip:
    pip install pyvista numpy

Optional (for better rendering):
    pip install vtk

USAGE:
------
1. Place all your .obj files in a folder (default: "heart_obj_files")
2. Run this script: python heart_viewer.py
3. The viewer will open automatically in fullscreen

INTERACTIVE CONTROLS:
---------------------
- Left click + drag: Rotate model
- Right click + drag: Pan/move model
- Middle click + drag: Zoom (or use scroll wheel)
- Scroll wheel: Zoom in/out
- 'r': Reset camera view
- 'w': Toggle wireframe mode
- 's': Take screenshot
- 'f': Toggle fullscreen
- 'q' or ESC: Quit viewer

FEATURES:
---------
- Medically accurate coloring (pink/red tissue, light blue veins)
- Soft, realistic lighting for organic appearance
- Smooth shading with proper normals
- Dark neutral background for professional visualization
- Seamless UI integration (no visible panels)
- Transparency control slider
"""

import pyvista as pv
import numpy as np
from pathlib import Path
import sys

# ============================================================================
# CONFIGURATION - Medically Accurate Colors
# ============================================================================

# Folder containing .obj files
OBJ_FOLDER = r"C:\Users\Admin\Desktop\Anatomy tasks\Task 3\3D Data\Heart"

# Realistic heart tissue colors (medically accurate)
# These colors represent actual heart anatomy
HEART_COLORS = {
    'muscle_tissue': [
        (0.85, 0.45, 0.45),  # Deep pink-red (cardiac muscle)
        (0.90, 0.50, 0.50),  # Pink-red (myocardium)
        (0.88, 0.48, 0.48),  # Medium pink-red
        (0.82, 0.42, 0.42),  # Darker tissue
    ],
    'arterial': [
        (0.92, 0.35, 0.35),  # Bright red (oxygenated blood)
        (0.88, 0.32, 0.32),  # Deep red
        (0.85, 0.30, 0.30),  # Dark red
    ],
    'venous': [
        (0.60, 0.70, 0.85),  # Light blue (deoxygenated)
        (0.55, 0.65, 0.82),  # Medium blue
        (0.50, 0.60, 0.80),  # Deeper blue
    ],
}

# Combine all colors for cycling through parts
ALL_COLORS = (
    HEART_COLORS['muscle_tissue'] * 2 +  # More tissue colors (most common)
    HEART_COLORS['arterial'] +
    HEART_COLORS['venous']
)

# Professional dark background (neutral dark gray)
BACKGROUND_COLOR = (0.18, 0.18, 0.18)  # Dark neutral gray

# Default transparency (1.0 = fully opaque, 0.0 = fully transparent)
DEFAULT_OPACITY = 1.0

# Lighting settings for realistic tissue appearance
LIGHTING_CONFIG = {
    'ambient': 0.35,      # Ambient light (prevents pure black shadows)
    'diffuse': 0.65,      # Diffuse reflection (main light)
    'specular': 0.15,     # Specular highlights (subtle shine)
    'specular_power': 8,  # Low value = soft, organic highlights
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def load_obj_files(folder_path):
    """Load all .obj files from the specified folder."""
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"Error: Folder '{folder_path}' does not exist!")
        print(f"Please create the folder and place your .obj files inside.")
        sys.exit(1)
    
    obj_files = sorted(list(folder.glob("*.obj")))  # Sort for consistent coloring
    
    if not obj_files:
        print(f"Error: No .obj files found in '{folder_path}'!")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print(f"Found {len(obj_files)} .obj files:")
    print(f"{'='*60}")
    for idx, obj_file in enumerate(obj_files, 1):
        print(f"  {idx:2d}. {obj_file.name}")
    print(f"{'='*60}\n")
    
    return obj_files


def apply_realistic_material(actor, color):
    """Apply realistic tissue material properties to an actor."""
    prop = actor.GetProperty()
    
    # Set color
    prop.SetColor(color)
    
    # Apply lighting properties for organic tissue
    prop.SetAmbient(LIGHTING_CONFIG['ambient'])
    prop.SetDiffuse(LIGHTING_CONFIG['diffuse'])
    prop.SetSpecular(LIGHTING_CONFIG['specular'])
    prop.SetSpecularPower(LIGHTING_CONFIG['specular_power'])
    
    # Enable smooth shading
    prop.SetInterpolationToPhong()
    
    # Slight subsurface scattering effect (translucency)
    prop.SetOpacity(DEFAULT_OPACITY)


def setup_realistic_lighting(plotter):
    """Configure soft, realistic lighting for medical visualization."""
    
    # Remove default lighting
    plotter.remove_all_lights()
    
    # Key light (main light source) - soft and from above-front
    key_light = pv.Light(
        position=(10, 15, 10),
        focal_point=(0, 0, 0),
        color='white',
        intensity=0.6,
        light_type='scene light'
    )
    plotter.add_light(key_light)
    
    # Fill light (softens shadows) - from below-left
    fill_light = pv.Light(
        position=(-8, -5, 8),
        focal_point=(0, 0, 0),
        color='white',
        intensity=0.25,
        light_type='scene light'
    )
    plotter.add_light(fill_light)
    
    # Back light (rim lighting for depth) - from behind
    back_light = pv.Light(
        position=(0, 5, -12),
        focal_point=(0, 0, 0),
        color='white',
        intensity=0.20,
        light_type='scene light'
    )
    plotter.add_light(back_light)
    
    # Ambient light (very subtle, fills in dark areas)
    ambient_light = pv.Light(
        position=(0, -10, 0),
        focal_point=(0, 0, 0),
        color='white',
        intensity=0.12,
        light_type='scene light'
    )
    plotter.add_light(ambient_light)


# ============================================================================
# MAIN VIEWER
# ============================================================================

def create_realistic_heart_viewer(obj_files):
    """Create professional medical visualization of heart model."""
    
    # Create plotter with dark theme
    plotter = pv.Plotter()
    plotter.set_background(BACKGROUND_COLOR)
    
    # Configure window
    plotter.window_size = [1920, 1080]
    
    # Store actors and meshes for manipulation
    actors = []
    meshes = []
    
    print("Loading and rendering heart model...")
    print(f"{'='*60}")
    
    # Load and add each mesh to the scene
    for idx, obj_file in enumerate(obj_files):
        try:
            # Load the mesh
            mesh = pv.read(str(obj_file))
            meshes.append(mesh)
            
            # Compute normals for smooth shading (essential for realism)
            mesh = mesh.compute_normals(
                cell_normals=False,
                point_normals=True,
                split_vertices=False,
                flip_normals=False,
                consistent_normals=True,
                auto_orient_normals=True
            )
            
            # Select color from realistic palette
            color = ALL_COLORS[idx % len(ALL_COLORS)]
            
            # Add mesh with basic settings first
            actor = plotter.add_mesh(
                mesh,
                color=color,
                smooth_shading=True,
                show_edges=False,
                name=obj_file.stem
            )
            
            # Apply realistic material properties
            apply_realistic_material(actor, color)
            
            actors.append(actor)
            
            print(f"  ✓ Loaded: {obj_file.name}")
            
        except Exception as e:
            print(f"  ✗ Warning: Could not load {obj_file.name}: {e}")
    
    print(f"{'='*60}")
    
    if not actors:
        print("Error: No meshes were successfully loaded!")
        sys.exit(1)
    
    print(f"\n✓ Successfully loaded {len(actors)} heart components\n")
    
    # Setup realistic lighting
    setup_realistic_lighting(plotter)
    
    # Enable anti-aliasing for smoother edges
    plotter.enable_anti_aliasing('fxaa')
    
    # Enable subtle ambient occlusion for depth
    try:
        plotter.enable_ssao(radius=10, bias=0.01, kernel_size=32, blur=True)
    except:
        pass  # SSAO not available in all PyVista versions
    
    # Add opacity control slider with dark theme
    def update_opacity(value):
        """Update opacity of all heart parts."""
        for actor in actors:
            actor.GetProperty().SetOpacity(value)
    
    slider_widget = plotter.add_slider_widget(
        update_opacity,
        [0.1, 1.0],  # Min opacity 0.1 to keep parts visible
        value=DEFAULT_OPACITY,
        title="Opacity",
        pointa=(0.70, 0.92),
        pointb=(0.95, 0.92),
        style='modern'
    )
    
    # Customize slider appearance to blend with background
    try:
        slider_rep = slider_widget.GetRepresentation()
        slider_rep.GetTubeProperty().SetColor(0.5, 0.5, 0.5)
        slider_rep.GetSliderProperty().SetColor(0.8, 0.4, 0.4)  # Red accent
        slider_rep.GetSelectedProperty().SetColor(0.9, 0.3, 0.3)
        slider_rep.GetTitleProperty().SetColor(0.85, 0.85, 0.85)
        slider_rep.GetLabelProperty().SetColor(0.75, 0.75, 0.75)
    except:
        pass
    
    # Add minimal instructions (bottom left, subtle)
    instructions = (
        "CONTROLS\n"
        "Left drag: Rotate  |  Right drag: Pan  |  Scroll: Zoom\n"
        "'r': Reset  |  'f': Fullscreen  |  's': Screenshot  |  'q': Quit"
    )
    plotter.add_text(
        instructions,
        position='lower_left',
        font_size=9,
        color=(0.7, 0.7, 0.7),  # Subtle gray text
        font='arial'
    )
    
    # Add title (top left, subtle)
    plotter.add_text(
        "3D Heart Model Viewer",
        position='upper_left',
        font_size=11,
        color=(0.75, 0.75, 0.75),
        font='arial'
    )
    
    # Set optimal camera position for heart viewing
    plotter.camera_position = 'iso'  # Isometric view
    plotter.camera.azimuth = 30  # Rotate slightly
    plotter.camera.elevation = 15  # Tilt up slightly
    plotter.camera.zoom(1.4)  # Zoom in for better view
    
    # Configure interactor for smooth interaction
    plotter.iren.SetDesiredUpdateRate(60)  # Smooth 60 FPS interaction
    plotter.iren.SetStillUpdateRate(30)    # 30 FPS when still
    
    return plotter


def main():
    """Main function to run the heart viewer."""
    print("\n" + "="*60)
    print("  REALISTIC 3D HEART MODEL VIEWER")
    print("="*60)
    
    # Load all .obj files
    obj_files = load_obj_files(OBJ_FOLDER)
    
    # Create the viewer
    plotter = create_realistic_heart_viewer(obj_files)
    
    # Show in fullscreen mode
    print("\n" + "="*60)
    print("Opening viewer in fullscreen mode...")
    print("="*60 + "\n")
    
    # Open fullscreen
    plotter.show(
        full_screen=True,
        auto_close=False,
        interactive_update=True
    )
    
    print("\n" + "="*60)
    print("Viewer closed. Thank you for using Heart Viewer!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()