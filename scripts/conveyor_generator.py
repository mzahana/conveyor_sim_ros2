#!/usr/bin/env python3

import os
import sys
import argparse
import math
import shutil
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET

def create_model_config(model_name, directory):
    """
    Create model.config file for the conveyor belt model.
    """
    root = ET.Element("model")
    name = ET.SubElement(root, "name")
    name.text = model_name
    
    version = ET.SubElement(root, "version")
    version.text = "1.0"
    
    sdf = ET.SubElement(root, "sdf", version="1.7")
    sdf.text = "model.sdf"
    
    author = ET.SubElement(root, "author")
    author_name = ET.SubElement(author, "name")
    author_name.text = "Auto Generated"
    email = ET.SubElement(author, "email")
    email.text = "info@example.com"
    
    description = ET.SubElement(root, "description")
    description.text = f"A conveyor belt model with length {args.length}m, width {args.width}m, thickness {args.thickness}m, and height {args.height}m."
    
    # Convert to pretty XML
    rough_string = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")
    
    # Write to file
    config_path = os.path.join(directory, "model.config")
    with open(config_path, "w") as f:
        f.write(pretty_xml)
    
    print(f"Created {config_path}")

def create_model_sdf(args, directory, material_names):
    """
    Create model.sdf file for the conveyor belt model with the given parameters.
    """
    # Create the root elements
    sdf = ET.Element("sdf", version="1.7")
    model = ET.SubElement(sdf, "model", name=args.model_name)
    
    # Set model as static
    static = ET.SubElement(model, "static")
    static.text = "1"
    
    # Create base link
    base_link = ET.SubElement(model, "link", name="base_link")
    pose = ET.SubElement(base_link, "pose", relative_to="__model__")
    pose.text = "0 0 0 0 0 0"
    
    # Inertial properties - approximate values
    inertial = ET.SubElement(base_link, "inertial")
    mass = ET.SubElement(inertial, "mass")
    mass.text = str(args.length * args.width * args.thickness * 2000)  # Approximate mass based on dimensions
    
    # Rough inertia calculation based on box dimensions
    ixx = (1/12) * float(mass.text) * (args.width**2 + args.thickness**2)
    iyy = (1/12) * float(mass.text) * (args.length**2 + args.thickness**2)
    izz = (1/12) * float(mass.text) * (args.length**2 + args.width**2)
    
    inertia = ET.SubElement(inertial, "inertia")
    ixx_elem = ET.SubElement(inertia, "ixx")
    ixx_elem.text = str(ixx)
    ixy_elem = ET.SubElement(inertia, "ixy")
    ixy_elem.text = "0"
    ixz_elem = ET.SubElement(inertia, "ixz")
    ixz_elem.text = "0"
    iyy_elem = ET.SubElement(inertia, "iyy")
    iyy_elem.text = str(iyy)
    iyz_elem = ET.SubElement(inertia, "iyz")
    iyz_elem.text = "1.5e-05"  # Small coupling term
    izz_elem = ET.SubElement(inertia, "izz")
    izz_elem.text = str(izz)
    
    # Main belt collision
    main_collision = ET.SubElement(base_link, "collision", name="main_collision")
    main_pose = ET.SubElement(main_collision, "pose", relative_to="base_link")
    main_pose.text = f"0 0 {args.height + args.thickness/2} 0 0 0"
    
    main_geometry = ET.SubElement(main_collision, "geometry")
    main_box = ET.SubElement(main_geometry, "box")
    main_size = ET.SubElement(main_box, "size")
    main_size.text = f"{args.length} {args.width} {args.thickness}"
    
    main_surface = ET.SubElement(main_collision, "surface")
    main_friction = ET.SubElement(main_surface, "friction")
    main_ode = ET.SubElement(main_friction, "ode")
    main_mu = ET.SubElement(main_ode, "mu")
    main_mu.text = "0.7"
    main_mu2 = ET.SubElement(main_ode, "mu2")
    main_mu2.text = "150"
    main_fdir1 = ET.SubElement(main_ode, "fdir1")
    main_fdir1.text = "0 1 0"
    
    # Main belt visual
    main_visual = ET.SubElement(base_link, "visual", name="main_visual")
    main_vis_pose = ET.SubElement(main_visual, "pose", relative_to="base_link")
    main_vis_pose.text = f"0 0 {args.height + args.thickness/2} 0 0 0"
    
    main_vis_geometry = ET.SubElement(main_visual, "geometry")
    main_vis_box = ET.SubElement(main_vis_geometry, "box")
    main_vis_size = ET.SubElement(main_vis_box, "size")
    main_vis_size.text = f"{args.length} {args.width} {args.thickness}"
    
    # Create material section for main belt
    main_material = ET.SubElement(main_visual, "material")
    
    if material_names and args.use_custom_materials:
        # Use custom materials if requested
        if args.use_pbr_materials:
            # PBR material setup
            main_diffuse = ET.SubElement(main_material, "diffuse")
            main_diffuse.text = "1.0 1.0 1.0"
            main_specular = ET.SubElement(main_material, "specular")
            main_specular.text = "1.0 1.0 1.0"
            
            pbr = ET.SubElement(main_material, "pbr")
            metal = ET.SubElement(pbr, "metal")
            
            # Belt albedo texture
            model_path = f"model://{args.model_name}"
            if material_names.get("belt_texture_filename"):
                albedo_map = ET.SubElement(metal, "albedo_map")
                albedo_map.text = f"{model_path}/materials/textures/{material_names.get('belt_texture_filename')}"
            
            # Optional normal map
            if material_names.get("belt_normal_filename"):
                normal_map = ET.SubElement(metal, "normal_map")
                normal_map.text = f"{model_path}/materials/textures/{material_names.get('belt_normal_filename')}"
            
            # Optional metalness map
            if material_names.get("belt_metalness_filename"):
                metalness_map = ET.SubElement(metal, "metalness_map")
                metalness_map.text = f"{model_path}/materials/textures/{material_names.get('belt_metalness_filename')}"
            else:
                metalness = ET.SubElement(metal, "metalness")
                metalness.text = "0.5"  # Default metalness value
            
            # Optional roughness map
            if material_names.get("belt_roughness_filename"):
                roughness_map = ET.SubElement(metal, "roughness_map")
                roughness_map.text = f"{model_path}/materials/textures/{material_names.get('belt_roughness_filename')}"
            else:
                roughness = ET.SubElement(metal, "roughness")
                roughness.text = "0.5"  # Default roughness value
        
        # Fallback script material
        script = ET.SubElement(main_material, "script")
        uri1 = ET.SubElement(script, "uri")
        uri1.text = f"model://{args.model_name}/materials/scripts/"
        uri2 = ET.SubElement(script, "uri")
        uri2.text = f"model://{args.model_name}/materials/textures/"
        name = ET.SubElement(script, "name")
        name.text = material_names["belt_material"]
    else:
        # Default material setup without custom textures
        main_ambient = ET.SubElement(main_material, "ambient")
        main_ambient.text = "0.05 0.05 0.70 1"
        main_diffuse = ET.SubElement(main_material, "diffuse")
        main_diffuse.text = "0.05 0.05 0.70 1"
        main_specular = ET.SubElement(main_material, "specular")
        main_specular.text = "0.8 0.8 0.8 1"
    
    # Add roller cylinders at the ends
    roller_radius = args.thickness / 2  # Roller radius based on belt thickness
    
    # First roller (positive X end)
    collision1 = ET.SubElement(base_link, "collision", name="collision_1")
    pose1 = ET.SubElement(collision1, "pose", relative_to="base_link")
    pose1.text = f"{args.length/2} 0 {args.height + args.thickness/2} -1.570796327 0 0"
    
    geometry1 = ET.SubElement(collision1, "geometry")
    cylinder1 = ET.SubElement(geometry1, "cylinder")
    length1 = ET.SubElement(cylinder1, "length")
    length1.text = str(args.width)
    radius1 = ET.SubElement(cylinder1, "radius")
    radius1.text = str(roller_radius)
    
    surface1 = ET.SubElement(collision1, "surface")
    friction1 = ET.SubElement(surface1, "friction")
    ode1 = ET.SubElement(friction1, "ode")
    mu1 = ET.SubElement(ode1, "mu")
    mu1.text = "0.7"
    mu21 = ET.SubElement(ode1, "mu2")
    mu21.text = "150"
    fdir11 = ET.SubElement(ode1, "fdir1")
    fdir11.text = "0 1 0"
    
    visual1 = ET.SubElement(base_link, "visual", name="visual_1")
    vis_pose1 = ET.SubElement(visual1, "pose", relative_to="base_link")
    vis_pose1.text = f"{args.length/2} 0 {args.height + args.thickness/2} -1.570796327 0 0"
    
    vis_geom1 = ET.SubElement(visual1, "geometry")
    vis_cyl1 = ET.SubElement(vis_geom1, "cylinder")
    vis_len1 = ET.SubElement(vis_cyl1, "length")
    vis_len1.text = str(args.width)
    vis_rad1 = ET.SubElement(vis_cyl1, "radius")
    vis_rad1.text = str(roller_radius)
    
    # Material for roller 1
    vis_mat1 = ET.SubElement(visual1, "material")
    
    if material_names and args.use_custom_materials:
        if args.use_pbr_materials:
            # PBR material setup for rollers
            roller_diffuse = ET.SubElement(vis_mat1, "diffuse")
            roller_diffuse.text = "1.0 1.0 1.0"
            roller_specular = ET.SubElement(vis_mat1, "specular")
            roller_specular.text = "1.0 1.0 1.0"
            
            roller_pbr = ET.SubElement(vis_mat1, "pbr")
            roller_metal = ET.SubElement(roller_pbr, "metal")
            
            # Roller albedo texture using the material_names dictionary
            model_path = f"model://{args.model_name}"
            if material_names.get("roller_texture_filename"):
                roller_albedo_map = ET.SubElement(roller_metal, "albedo_map")
                roller_albedo_map.text = f"{model_path}/materials/textures/{material_names.get('roller_texture_filename')}"
            
            # Set roller metalness using texture if provided; otherwise, use default
            if material_names.get("roller_metalness_filename"):
                roller_metalness_map = ET.SubElement(roller_metal, "metalness_map")
                roller_metalness_map.text = f"{model_path}/materials/textures/{material_names.get('roller_metalness_filename')}"
            else:
                roller_metalness = ET.SubElement(roller_metal, "metalness")
                roller_metalness.text = "0.9"  # Default high metalness
            
            # Set roller roughness using texture if provided; otherwise, use default
            if material_names.get("roller_roughness_filename"):
                roller_roughness_map = ET.SubElement(roller_metal, "roughness_map")
                roller_roughness_map.text = f"{model_path}/materials/textures/{material_names.get('roller_roughness_filename')}"
            else:
                roller_roughness = ET.SubElement(roller_metal, "roughness")
                roller_roughness.text = "0.1"  # Default low roughness
        
        # Fallback script material for roller 1
        script1 = ET.SubElement(vis_mat1, "script")
        uri1_1 = ET.SubElement(script1, "uri")
        uri1_1.text = f"model://{args.model_name}/materials/scripts/"
        uri1_2 = ET.SubElement(script1, "uri")
        uri1_2.text = f"model://{args.model_name}/materials/textures/"
        name1 = ET.SubElement(script1, "name")
        name1.text = material_names["roller_material"]
    else:
        # Default material setup without custom textures for roller 1
        vis_amb1 = ET.SubElement(vis_mat1, "ambient")
        vis_amb1.text = "0.7 0.7 0.7 1"
        vis_dif1 = ET.SubElement(vis_mat1, "diffuse")
        vis_dif1.text = "0.7 0.7 0.7 1" 
        vis_spec1 = ET.SubElement(vis_mat1, "specular")
        vis_spec1.text = "1.0 1.0 1.0 1"
    
    # Second roller (negative X end)
    collision2 = ET.SubElement(base_link, "collision", name="collision_2")
    pose2 = ET.SubElement(collision2, "pose", relative_to="base_link")
    pose2.text = f"{-args.length/2} 0 {args.height + args.thickness/2} -1.570796327 0 0"
    
    geometry2 = ET.SubElement(collision2, "geometry")
    cylinder2 = ET.SubElement(geometry2, "cylinder")
    length2 = ET.SubElement(cylinder2, "length")
    length2.text = str(args.width)
    radius2 = ET.SubElement(cylinder2, "radius")
    radius2.text = str(roller_radius)
    
    surface2 = ET.SubElement(collision2, "surface")
    friction2 = ET.SubElement(surface2, "friction")
    ode2 = ET.SubElement(friction2, "ode")
    mu2 = ET.SubElement(ode2, "mu")
    mu2.text = "0.7"
    mu22 = ET.SubElement(ode2, "mu2")
    mu22.text = "150"
    fdir12 = ET.SubElement(ode2, "fdir1")
    fdir12.text = "0 1 0"
    
    visual2 = ET.SubElement(base_link, "visual", name="visual_2")
    vis_pose2 = ET.SubElement(visual2, "pose", relative_to="base_link")
    vis_pose2.text = f"{-args.length/2} 0 {args.height + args.thickness/2} -1.570796327 0 0"
    
    vis_geom2 = ET.SubElement(visual2, "geometry")
    vis_cyl2 = ET.SubElement(vis_geom2, "cylinder")
    vis_len2 = ET.SubElement(vis_cyl2, "length")
    vis_len2.text = str(args.width)
    vis_rad2 = ET.SubElement(vis_cyl2, "radius")
    vis_rad2.text = str(roller_radius)
    
    # Material for roller 2
    vis_mat2 = ET.SubElement(visual2, "material")
    
    if material_names and args.use_custom_materials:
        if args.use_pbr_materials:
            # PBR material setup for roller 2
            roller2_diffuse = ET.SubElement(vis_mat2, "diffuse")
            roller2_diffuse.text = "1.0 1.0 1.0"
            roller2_specular = ET.SubElement(vis_mat2, "specular")
            roller2_specular.text = "1.0 1.0 1.0"
            
            roller2_pbr = ET.SubElement(vis_mat2, "pbr")
            roller2_metal = ET.SubElement(roller2_pbr, "metal")
            
            # Roller albedo texture for roller 2
            model_path = f"model://{args.model_name}"
            if material_names.get("roller_texture_filename"):
                roller2_albedo_map = ET.SubElement(roller2_metal, "albedo_map")
                roller2_albedo_map.text = f"{model_path}/materials/textures/{material_names.get('roller_texture_filename')}"
            
            # Roller metalness for roller 2
            if material_names.get("roller_metalness_filename"):
                roller2_metalness_map = ET.SubElement(roller2_metal, "metalness_map")
                roller2_metalness_map.text = f"{model_path}/materials/textures/{material_names.get('roller_metalness_filename')}"
            else:
                roller2_metalness = ET.SubElement(roller2_metal, "metalness")
                roller2_metalness.text = "0.9"
            
            # Roller roughness for roller 2
            if material_names.get("roller_roughness_filename"):
                roller2_roughness_map = ET.SubElement(roller2_metal, "roughness_map")
                roller2_roughness_map.text = f"{model_path}/materials/textures/{material_names.get('roller_roughness_filename')}"
            else:
                roller2_roughness = ET.SubElement(roller2_metal, "roughness")
                roller2_roughness.text = "0.1"
        
        # Fallback script material for roller 2
        script2 = ET.SubElement(vis_mat2, "script")
        uri2_1 = ET.SubElement(script2, "uri")
        uri2_1.text = f"model://{args.model_name}/materials/scripts/"
        uri2_2 = ET.SubElement(script2, "uri")
        uri2_2.text = f"model://{args.model_name}/materials/textures/"
        name2 = ET.SubElement(script2, "name")
        name2.text = material_names["roller_material"]
    else:
        # Default material setup without custom textures for roller 2
        vis_amb2 = ET.SubElement(vis_mat2, "ambient")
        vis_amb2.text = "0.7 0.7 0.7 1"
        vis_dif2 = ET.SubElement(vis_mat2, "diffuse")
        vis_dif2.text = "0.7 0.7 0.7 1"
        vis_spec2 = ET.SubElement(vis_mat2, "specular")
        vis_spec2.text = "1.0 1.0 1.0 1"
    
    # Add supporting legs at the corners
    leg_width = 0.05  # Width of the leg
    leg_length = 0.05  # Length of the leg
    leg_height = args.height
    
    leg_positions = [
        (args.length/2 - leg_length/2, args.width/2 - leg_width/2, leg_height/2),  # Front right
        (args.length/2 - leg_length/2, -args.width/2 + leg_width/2, leg_height/2),  # Front left
        (-args.length/2 + leg_length/2, args.width/2 - leg_width/2, leg_height/2),  # Back right
        (-args.length/2 + leg_length/2, -args.width/2 + leg_width/2, leg_height/2)  # Back left
    ]
    
    for i, (x, y, z) in enumerate(leg_positions):
        # Leg collision
        leg_collision = ET.SubElement(base_link, "collision", name=f"leg_collision_{i}")
        leg_coll_pose = ET.SubElement(leg_collision, "pose", relative_to="base_link")
        leg_coll_pose.text = f"{x} {y} {z} 0 0 0"
        
        leg_coll_geom = ET.SubElement(leg_collision, "geometry")
        leg_coll_box = ET.SubElement(leg_coll_geom, "box")
        leg_coll_size = ET.SubElement(leg_coll_box, "size")
        leg_coll_size.text = f"{leg_length} {leg_width} {leg_height}"
        
        # Leg visual
        leg_visual = ET.SubElement(base_link, "visual", name=f"leg_visual_{i}")
        leg_vis_pose = ET.SubElement(leg_visual, "pose", relative_to="base_link")
        leg_vis_pose.text = f"{x} {y} {z} 0 0 0"
        
        leg_vis_geom = ET.SubElement(leg_visual, "geometry")
        leg_vis_box = ET.SubElement(leg_vis_geom, "box")
        leg_vis_size = ET.SubElement(leg_vis_box, "size")
        leg_vis_size.text = f"{leg_length} {leg_width} {leg_height}"
        
        # Material for leg
        leg_material = ET.SubElement(leg_visual, "material")
        
        if material_names and args.use_custom_materials:
            if args.use_pbr_materials:
                # PBR material setup for legs
                leg_diffuse = ET.SubElement(leg_material, "diffuse")
                leg_diffuse.text = "1.0 1.0 1.0"
                leg_specular = ET.SubElement(leg_material, "specular")
                leg_specular.text = "1.0 1.0 1.0"
                
                leg_pbr = ET.SubElement(leg_material, "pbr")
                leg_metal = ET.SubElement(leg_pbr, "metal")
                
                # Leg albedo texture
                model_path = f"model://{args.model_name}"
                if args.leg_texture:
                    leg_albedo_map = ET.SubElement(leg_metal, "albedo_map")
                    leg_albedo_map.text = f"{model_path}/materials/textures/{os.path.basename(args.leg_texture)}"
                
                # Set leg metalness using texture if provided; else default
                if material_names.get("leg_metalness_filename"):
                    leg_metalness_map = ET.SubElement(leg_metal, "metalness_map")
                    leg_metalness_map.text = f"{model_path}/materials/textures/{material_names.get('leg_metalness_filename')}"
                else:
                    leg_metalness = ET.SubElement(leg_metal, "metalness")
                    leg_metalness.text = "0.9"  # Default high metalness
                
                # Set leg roughness using texture if provided; else default
                if material_names.get("leg_roughness_filename"):
                    leg_roughness_map = ET.SubElement(leg_metal, "roughness_map")
                    leg_roughness_map.text = f"{model_path}/materials/textures/{material_names.get('leg_roughness_filename')}"
                else:
                    leg_roughness = ET.SubElement(leg_metal, "roughness")
                    leg_roughness.text = "0.2"  # Default slightly higher roughness for legs
            
            # Fallback script material for leg
            leg_script = ET.SubElement(leg_material, "script")
            leg_uri1 = ET.SubElement(leg_script, "uri")
            leg_uri1.text = f"model://{args.model_name}/materials/scripts/"
            leg_uri2 = ET.SubElement(leg_script, "uri")
            leg_uri2.text = f"model://{args.model_name}/materials/textures/"
            leg_name = ET.SubElement(leg_script, "name")
            leg_name.text = material_names["leg_material"]
        else:
            # Default material setup without custom textures for leg
            leg_ambient = ET.SubElement(leg_material, "ambient")
            leg_ambient.text = "0.4 0.4 0.4 1"
            leg_diffuse = ET.SubElement(leg_material, "diffuse")
            leg_diffuse.text = "0.4 0.4 0.4 1"
            leg_specular = ET.SubElement(leg_material, "specular")
            leg_specular.text = "0.8 0.8 0.8 1"
    
    # Add gravity and kinematic properties
    gravity = ET.SubElement(base_link, "gravity")
    gravity.text = "1"
    kinematic = ET.SubElement(base_link, "kinematic")
    kinematic.text = "0"
    
    # Add plugins for conveyor belt functionality
    plugin1 = ET.SubElement(model, "plugin", 
                           filename="gz-sim-track-controller-system",
                           name="gz::sim::systems::TrackController")
    plugin1_link = ET.SubElement(plugin1, "link")
    plugin1_link.text = "base_link"
    plugin1_freq = ET.SubElement(plugin1, "odometry_publish_frequency")
    plugin1_freq.text = "1"
    plugin1_vel_topic = ET.SubElement(plugin1, "velocity_topic")
    plugin1_vel_topic.text = "/conveyor/cmd_vel"
    
    # W key (forward)
    plugin2 = ET.SubElement(model, "plugin", 
                           filename="gz-sim-triggered-publisher-system",
                           name="gz::sim::systems::TriggeredPublisher")
    plugin2_input = ET.SubElement(plugin2, "input", type="gz.msgs.Int32", topic="/keyboard/keypress")
    plugin2_match = ET.SubElement(plugin2_input, "match", field="data")
    plugin2_match.text = "87"
    plugin2_output = ET.SubElement(plugin2, "output", 
                                  type="gz.msgs.Double", 
                                #   topic=f"/model/{args.model_name}/link/base_link/track_cmd_vel"
                                topic=f"/conveyor/cmd_vel"
                                  )
    plugin2_output.text = "\n        data: 1.0\n      "
    
    # X key (backward)
    plugin3 = ET.SubElement(model, "plugin", 
                           filename="gz-sim-triggered-publisher-system",
                           name="gz::sim::systems::TriggeredPublisher")
    plugin3_input = ET.SubElement(plugin3, "input", type="gz.msgs.Int32", topic="/keyboard/keypress")
    plugin3_match = ET.SubElement(plugin3_input, "match", field="data")
    plugin3_match.text = "88"
    plugin3_output = ET.SubElement(plugin3, "output", 
                                  type="gz.msgs.Double", 
                                #   topic=f"/model/{args.model_name}/link/base_link/track_cmd_vel"
                                topic=f"/conveyor/cmd_vel"
                                  )
    plugin3_output.text = "\n        data: -1.0\n      "
    
    # S key (stop)
    plugin4 = ET.SubElement(model, "plugin", 
                           filename="gz-sim-triggered-publisher-system",
                           name="gz::sim::systems::TriggeredPublisher")
    plugin4_input = ET.SubElement(plugin4, "input", type="gz.msgs.Int32", topic="/keyboard/keypress")
    plugin4_match = ET.SubElement(plugin4_input, "match", field="data")
    plugin4_match.text = "83"
    plugin4_output = ET.SubElement(plugin4, "output", 
                                  type="gz.msgs.Double", 
                                #   topic=f"/model/{args.model_name}/link/base_link/track_cmd_vel"
                                topic=f"/conveyor/cmd_vel"
                                  )
    plugin4_output.text = "\n        data: 0.0\n      "
    
    # Convert to pretty XML with proper formatting
    rough_string = ET.tostring(sdf, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")
    
    # Fix issue with XML declaration appearing twice
    if pretty_xml.count('<?xml') > 1:
        pretty_xml = pretty_xml[pretty_xml.find('<?xml', 1):]
    
    # Write to file
    sdf_path = os.path.join(directory, "model.sdf")
    with open(sdf_path, "w") as f:
        f.write('<?xml version="1.0" ?>\n' + pretty_xml)
    
    print(f"Created {sdf_path}")

def copy_texture_file(source_path, textures_dir, default_name):
    """
    Copy a texture file from the source path to the textures directory.
    Returns the filename (without path) that was used.
    """
    if not source_path:
        return None
        
    if not os.path.exists(source_path):
        print(f"Warning: Texture file {source_path} not found. This texture will be skipped.")
        return None
    
    # Get the filename from the path
    filename = os.path.basename(source_path)
    destination_path = os.path.join(textures_dir, filename)
    
    # Copy the file
    try:
        shutil.copy2(source_path, destination_path)
        print(f"Copied texture: {source_path} → {destination_path}")
        return filename
    except Exception as e:
        print(f"Error copying {source_path}: {e}")
        print("This texture will be skipped.")
        return None

def create_material_files(args, directory):
    """
    Create the materials directory structure and files for the conveyor belt model.
    Only creates if custom materials are requested.
    """
    # Skip if not using custom materials
    if not args.use_custom_materials:
        return None
        
    # Create materials directory structure
    materials_dir = os.path.join(directory, "materials")
    textures_dir = os.path.join(materials_dir, "textures")
    scripts_dir = os.path.join(materials_dir, "scripts")
    
    os.makedirs(textures_dir, exist_ok=True)
    os.makedirs(scripts_dir, exist_ok=True)
    
    print(f"Created materials directories: {materials_dir}")
    
    # Copy texture files if provided and track which ones were successfully copied
    belt_texture_filename = copy_texture_file(args.belt_texture, textures_dir, "conveyor_belt_albedo.png")
    belt_normal_filename = copy_texture_file(args.belt_normal, textures_dir, "conveyor_belt_normal.png")
    belt_metalness_filename = copy_texture_file(args.belt_metalness, textures_dir, "conveyor_belt_metalness.png")
    belt_roughness_filename = copy_texture_file(args.belt_roughness, textures_dir, "conveyor_belt_roughness.png")
    roller_texture_filename = copy_texture_file(args.roller_texture, textures_dir, "conveyor_roller_albedo.png")
    leg_texture_filename = copy_texture_file(args.leg_texture, textures_dir, "conveyor_leg_albedo.png")
    
    # New texture copies for roller and leg metalness/roughness maps
    roller_metalness_filename = copy_texture_file(args.roller_metalness, textures_dir, "conveyor_roller_metalness.png")
    roller_roughness_filename = copy_texture_file(args.roller_roughness, textures_dir, "conveyor_roller_roughness.png")
    leg_metalness_filename = copy_texture_file(args.leg_metalness, textures_dir, "conveyor_leg_metalness.png")
    leg_roughness_filename = copy_texture_file(args.leg_roughness, textures_dir, "conveyor_leg_roughness.png")
    
    # Check for missing textures
    missing_textures = []
    if args.use_pbr_materials:
        if not belt_texture_filename and args.belt_texture:
            missing_textures.append("belt albedo")
        if not belt_normal_filename and args.belt_normal:
            missing_textures.append("belt normal map")
        if not belt_metalness_filename and args.belt_metalness:
            missing_textures.append("belt metalness map")
        if not belt_roughness_filename and args.belt_roughness:
            missing_textures.append("belt roughness map")
    if not roller_texture_filename and args.roller_texture:
        missing_textures.append("roller texture")
    if not leg_texture_filename and args.leg_texture:
        missing_textures.append("leg texture")
    # Check new textures; these are optional and will have default if missing.
    
    if missing_textures:
        print("\nWARNING: Some texture files could not be copied:")
        for texture in missing_textures:
            print(f"  - {texture}")
        print("These textures will be omitted from the model.")
    
    # Required textures warnings
    if not belt_texture_filename:
        print("\nWARNING: No belt texture provided. The belt may appear with default colors.")
    if not roller_texture_filename:
        print("WARNING: No roller texture provided. The rollers may appear with default colors.")
    if not leg_texture_filename:
        print("WARNING: No leg texture provided. The legs may appear with default colors.")
    
    # Create the material script file
    material_script_path = os.path.join(scripts_dir, "model.material")
    
    material_name = f"{args.model_name}_material"
    belt_material_name = f"UrbanTile/{args.model_name}_Belt"
    roller_material_name = f"UrbanTile/{args.model_name}_Roller"
    leg_material_name = f"UrbanTile/{args.model_name}_Leg"
    
    with open(material_script_path, "w") as f:
        # Belt material
        f.write(f"""material {belt_material_name}
{{
  technique
  {{
    pass
    {{
      ambient 1.0 1.0 1.0 1.0
      diffuse 1.0 1.0 1.0 1.0
      specular 1.0 1.0 1.0 1.0 12.5
      """)
        
        if belt_texture_filename:
            f.write(f"""
      texture_unit
      {{
        texture {belt_texture_filename}
      }}
      """)
            
        f.write("""
    }
  }
}
""")

        # Roller material
        f.write(f"""
material {roller_material_name}
{{
  technique
  {{
    pass
    {{
      ambient 1.0 1.0 1.0 1.0
      diffuse 1.0 1.0 1.0 1.0
      specular 1.0 1.0 1.0 1.0 12.5
      """)
        
        if roller_texture_filename:
            f.write(f"""
      texture_unit
      {{
        texture {roller_texture_filename}
      }}
      """)
            
        f.write("""
    }
  }
}
""")

        # Leg material
        f.write(f"""
material {leg_material_name}
{{
  technique
  {{
    pass
    {{
      ambient 1.0 1.0 1.0 1.0
      diffuse 1.0 1.0 1.0 1.0
      specular 1.0 1.0 1.0 1.0 12.5
      """)
        
        if leg_texture_filename:
            f.write(f"""
      texture_unit
      {{
        texture {leg_texture_filename}
      }}
      """)
            
        f.write("""
    }
  }
}
""")
    
    print(f"Created material script: {material_script_path}")
    
    return {
        "belt_material": belt_material_name,
        "roller_material": roller_material_name,
        "leg_material": leg_material_name,
        "belt_texture_filename": belt_texture_filename,
        "belt_normal_filename": belt_normal_filename,
        "belt_metalness_filename": belt_metalness_filename,
        "belt_roughness_filename": belt_roughness_filename,
        "roller_texture_filename": roller_texture_filename,
        "roller_metalness_filename": roller_metalness_filename,
        "roller_roughness_filename": roller_roughness_filename,
        "leg_texture_filename": leg_texture_filename,
        "leg_metalness_filename": leg_metalness_filename,
        "leg_roughness_filename": leg_roughness_filename
    }

def main():
    parser = argparse.ArgumentParser(description='Generate Gazebo conveyor belt model')
    parser.add_argument('--length', type=float, default=5.0, help='Length of the conveyor belt in meters')
    parser.add_argument('--width', type=float, default=1.0, help='Width of the conveyor belt in meters')
    parser.add_argument('--thickness', type=float, default=0.1, help='Thickness of the conveyor belt in meters')
    parser.add_argument('--height', type=float, default=0.5, help='Height of the conveyor belt legs in meters')
    parser.add_argument('--model-name', type=str, default='conveyor', help='Name of the model')
    ## The directory name should be the same as the model name for consistency 
    # parser.add_argument('--directory', type=str, default='conveyor_model', help='Directory to create the model in')
    
    # Material options
    parser.add_argument('--use-custom-materials', action='store_true', help='Use custom texture materials for the model')
    parser.add_argument('--use-pbr-materials', action='store_true', help='Use PBR materials for the model (only if use-custom-materials is set)')
    
    # Texture file paths for belt
    parser.add_argument('--belt-texture', type=str, help='Path to belt albedo texture file (will be copied)')
    parser.add_argument('--belt-normal', type=str, help='Path to belt normal map file (will be copied)')
    parser.add_argument('--belt-metalness', type=str, help='Path to belt metalness map file (will be copied)')
    parser.add_argument('--belt-roughness', type=str, help='Path to belt roughness map file (will be copied)')
    
    # Texture file paths for roller and legs
    parser.add_argument('--roller-texture', type=str, help='Path to roller albedo texture file (will be copied)')
    parser.add_argument('--roller-metalness', type=str, help='Path to roller metalness map file (will be copied)')
    parser.add_argument('--roller-roughness', type=str, help='Path to roller roughness map file (will be copied)')
    parser.add_argument('--leg-texture', type=str, help='Path to leg albedo texture file (will be copied)')
    parser.add_argument('--leg-metalness', type=str, help='Path to leg metalness map file (will be copied)')
    parser.add_argument('--leg-roughness', type=str, help='Path to leg roughness map file (will be copied)')
    
    global args
    args = parser.parse_args()
    directory = args.model_name
    
    # Create directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    
    # Create materials directory and files if custom materials are requested
    material_names = None
    if args.use_custom_materials:
        material_names = create_material_files(args, directory)
    
    # Create model config and SDF files
    create_model_config(args.model_name, directory)
    create_model_sdf(args, directory, material_names)
    
    print(f"\nConveyor belt model generated successfully in {directory}/")
    print(f"Parameters: length={args.length}m, width={args.width}m, thickness={args.thickness}m, height={args.height}m")
    if args.use_custom_materials:
        print("Using custom materials with texture files")
    else:
        print("Using default material colors")

if __name__ == "__main__":
    main()
