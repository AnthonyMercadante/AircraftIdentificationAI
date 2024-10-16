import bpy
import math
import os

# Set up variables
object_name = 'Empty'  # Replace with the actual object name in Blender
render_folder = r'C:\Users\Raeth\OneDrive\Documents\lancaster renders'  # Output folder path
camera_name = 'Camera'  # Name of the camera in the scene
angle_increment = 10  # Degrees between each shot

# Ensure the render folder existss
if not os.path.exists(render_folder):
    os.makedirs(render_folder)

# Print debug info
print(f"Rendering to folder: {render_folder}")

# Select the object to rotate
object_to_rotate = bpy.data.objects[object_name]

# Calculate the number of rotations needed (360 degrees / angle_increment)
num_shots_z = int(360 / angle_increment)  # Number of steps for Z-axis rotation (yaw)
num_shots_x = int(180 / angle_increment)  # Number of steps for X-axis rotation (pitch)

# Ensure the object rotation mode is set to Euler XYZ
object_to_rotate.rotation_mode = 'XYZ'

# Set the render engine to Cycles
bpy.context.scene.render.engine = 'CYCLES'

# Enable GPU rendering with CUDA
bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
bpy.context.scene.cycles.device = 'GPU'

# Update the device list
bpy.context.preferences.addons['cycles'].preferences.get_devices()
devices = bpy.context.preferences.addons['cycles'].preferences.devices

# Enable the RTX 4070 Ti device
for device in devices:
    if device.type == 'CUDA' and 'RTX 4070' in device.name:
        device.use = True
        print(f"Enabled device: {device.name}")
    else:
        device.use = False

# Optional: Save preferences
bpy.ops.wm.save_userpref()

# Loop through each X-axis (pitch) and Z-axis (yaw) angle and take a render
total_renders = (num_shots_x + 1) * num_shots_z
render_count = 0

for x in range(num_shots_x + 1):  # Rotate around X-axis from -90 to +90 degrees (pitch)
    pitch_angle = -90 + (x * angle_increment)
    object_to_rotate.rotation_euler[0] = math.radians(pitch_angle)
    
    for z in range(num_shots_z):  # Rotate around Z-axis from 0 to 360 degrees (yaw)
        yaw_angle = z * angle_increment
        object_to_rotate.rotation_euler[2] = math.radians(yaw_angle)

        # Update the scene to reflect the new rotation
        bpy.context.view_layer.update()

        # Set the file path for the rendered image
        filepath = os.path.join(render_folder, f"render_pitch_{pitch_angle}_yaw_{yaw_angle}.png")
        bpy.context.scene.render.filepath = filepath

        # Print debug info
        render_count += 1
        print(f"Rendering image {render_count}/{total_renders}: {filepath}")

        # Render the scene and write to file
        bpy.ops.render.render(write_still=True)

# Print completion message
print("Rendering completed.")
