# Full-quality 1080p guide frame settings (EEVEE, 48 samples).
import bpy
s=bpy.context.scene
s.render.resolution_percentage=100; s.eevee.taa_render_samples=48
s.render.image_settings.file_format='PNG'
