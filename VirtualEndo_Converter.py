bl_info = {
    "name": "VirtualEndo Converter",
    "author": "VirtualEndo", 
    "version": (2, 1, 1),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > VirtualEndo",
    "description": "Konvertiert Diagnocat STL-Dateien zu verschiedenen Formaten",
    "category": "Import-Export",
    "support": "COMMUNITY"
}

import bpy
import os
import re
from bpy.props import StringProperty, FloatProperty, BoolProperty, FloatVectorProperty, EnumProperty
from bpy.types import Operator, Panel, PropertyGroup

def ensure_stl_addon():
    """Stellt sicher, dass das STL-Addon aktiviert ist"""
    try:
        if not hasattr(bpy.ops.import_mesh, 'stl'):
            print("STL-Addon nicht aktiv, aktiviere automatisch...")
            bpy.ops.preferences.addon_enable(module="io_mesh_stl")
            print("STL-Addon erfolgreich aktiviert!")
        else:
            print("STL-Addon bereits aktiv")
        return True
    except Exception as e:
        print(f"Fehler beim Aktivieren des STL-Addons: {e}")
        return False

def force_enable_stl():
    """Erzwingt die Aktivierung des STL-Addons mit mehreren Methoden"""
    methods = ["io_mesh_stl", "stl_import_export", "mesh_stl"]
    
    for method in methods:
        try:
            bpy.ops.preferences.addon_enable(module=method)
            if hasattr(bpy.ops.import_mesh, 'stl'):
                print(f"STL-Addon aktiviert mit Methode: {method}")
                return True
        except:
            continue
    
    return False

class VirtualEndoSettings(PropertyGroup):
    alpha_teeth: FloatProperty(
        name="Teeth Transparenz", 
        min=0.0, max=1.0, 
        default=0.3,
        description="Transparenz der Zähne"
    )
    alpha_bone: FloatProperty(
        name="Bone Transparenz", 
        min=0.0, max=1.0, 
        default=0.5,
        description="Transparenz der Knochen"
    )
    
    input_folder: StringProperty(
        name="VirtualEndo Ordner", 
        subtype='DIR_PATH',
        description="Ordner mit allen VirtualEndo STL-Dateien"
    )
    
    color_pulp: FloatVectorProperty(
        name="Pulp Farbe",
        subtype='COLOR',
        default=(0.7, 0.1, 0.1),
        min=0.0, max=1.0,
        description="Farbe für Pulp-Objekte"
    )
    color_teeth: FloatVectorProperty(
        name="Teeth Farbe", 
        subtype='COLOR',
        default=(0.98, 0.98, 0.96),
        min=0.0, max=1.0,
        description="Farbe für Teeth-Objekte"
    )
    color_bone: FloatVectorProperty(
        name="Bone Farbe",
        subtype='COLOR', 
        default=(0.88, 0.82, 0.72),
        min=0.0, max=1.0,
        description="Farbe für Bone-Objekte"
    )
    
    scale_factor: FloatProperty(
        name="Skalierung",
        default=0.01,
        min=0.001,
        max=10.0,
        description="Skalierungsfaktor für alle Objekte"
    )
    
    smooth_shading: BoolProperty(
        name="Smooth Shading",
        default=True,
        description="Smooth Shading anwenden"
    )
    
    center_objects: BoolProperty(
        name="Objekte zentrieren",
        default=True,
        description="Alle Objekte im Ursprung zentrieren"
    )
    
    export_format: EnumProperty(
        name="Export Format",
        items=[
            ('USDZ', "USDZ", "AR-kompatibles USDZ Format (iOS)"),
            ('GLB', "GLB", "Standard 3D-Format (plattformübergreifend)"),
            ('FBX', "FBX", "Autodesk FBX Format"),
            ('STL', "STL", "Stereolithographie Format")
        ],
        default='GLB',
        description="Format für den Export"
    )
    
    use_custom_output: BoolProperty(
        name="Eigenen Ausgabeordner verwenden",
        default=False,
        description="Wählen Sie einen eigenen Ordner für die Ausgabedatei"
    )
    
    output_folder: StringProperty(
        name="Ausgabeordner",
        subtype='DIR_PATH',
        description="Ordner für die exportierte Datei"
    )

def get_materials(settings):
    alpha_teeth = settings.alpha_teeth
    alpha_bone = settings.alpha_bone
    
    pulp_color = (*settings.color_pulp, 1.0)
    teeth_color = (*settings.color_teeth, alpha_teeth)
    bone_color = (*settings.color_bone, alpha_bone)
    
    return {
        "Pulp": {
            "alpha": 1.0,
            "color": pulp_color,
            "metallic": 0.0,
            "roughness": 0.8
        },
        "Teeth": {
            "alpha": alpha_teeth,
            "color": teeth_color,
            "metallic": 0.1,
            "roughness": 0.3
        },
        "Bone": {
            "alpha": alpha_bone,
            "color": bone_color,
            "metallic": 0.0,
            "roughness": 0.6
        }
    }

def categorize_stl_files(folder_path):
    """Kategorisiert STL-Dateien basierend auf Dateinamen"""
    files = {"Pulp": [], "Teeth": [], "Bone": []}
    
    if not os.path.exists(folder_path):
        return files
    
    for filename in os.listdir(folder_path):
        if not filename.lower().endswith('.stl'):
            continue
            
        filepath = os.path.join(folder_path, filename)
        filename_lower = filename.lower()
        
        if re.match(r'^pulp_\d+\.stl$', filename_lower):
            files["Pulp"].append((filepath, filename))
        elif re.match(r'^tooth_\d+\.stl$', filename_lower):
            files["Teeth"].append((filepath, filename))
        elif filename_lower in ['mandible.stl', 'maxilla.stl']:
            files["Bone"].append((filepath, filename))
    
    return files

class VIRTUALENDO_OT_enable_stl(Operator):
    bl_idname = "virtualendo.enable_stl"
    bl_label = "STL Add-on aktivieren"
    bl_description = "Aktiviert das STL Import/Export Add-on"
    
    def execute(self, context):
        if ensure_stl_addon():
            self.report({'INFO'}, "STL Add-on aktiviert!")
        else:
            if force_enable_stl():
                self.report({'INFO'}, "STL Add-on mit alternativer Methode aktiviert!")
            else:
                self.report({'ERROR'}, "STL Add-on konnte nicht aktiviert werden!")
        return {'FINISHED'}

class VIRTUALENDO_OT_color_presets(Operator):
    bl_idname = "virtualendo.color_presets"
    bl_label = "Farbpresets"
    bl_description = "Lädt vordefinierte Farbkombinationen"
    
    preset_type: EnumProperty(
        items=[
            ('DEFAULT', "Standard", "Standardfarben"),
            ('EDUCATIONAL', "Lehrreich", "Kontraststarke Farben"),
            ('PRESENTATION', "Präsentation", "Professionelle Farben")
        ]
    )
    
    def execute(self, context):
        settings = context.scene.virtualendo_settings
        
        if self.preset_type == 'DEFAULT':
            settings.color_pulp = (0.7, 0.1, 0.1)
            settings.color_teeth = (0.98, 0.98, 0.96)
            settings.color_bone = (0.88, 0.82, 0.72)
        elif self.preset_type == 'EDUCATIONAL':
            settings.color_pulp = (0.95, 0.2, 0.2)
            settings.color_teeth = (1.0, 1.0, 1.0)
            settings.color_bone = (0.85, 0.75, 0.55)
        elif self.preset_type == 'PRESENTATION':
            settings.color_pulp = (0.8, 0.15, 0.25)
            settings.color_teeth = (0.96, 0.96, 0.94)
            settings.color_bone = (0.82, 0.78, 0.68)
        
        self.report({'INFO'}, f"Preset '{self.preset_type}' geladen")
        return {'FINISHED'}

class VIRTUALENDO_OT_scan_files(Operator):
    bl_idname = "virtualendo.scan_files"
    bl_label = "Dateien scannen"
    bl_description = "Scannt den Ordner nach VirtualEndo STL-Dateien"
    
    def execute(self, context):
        settings = context.scene.virtualendo_settings
        
        if not settings.input_folder:
            self.report({'ERROR'}, "Kein Ordner ausgewählt!")
            return {'CANCELLED'}
            
        if not os.path.exists(settings.input_folder):
            self.report({'ERROR'}, "Ordner existiert nicht!")
            return {'CANCELLED'}
        
        files = categorize_stl_files(settings.input_folder)
        
        pulp_count = len(files["Pulp"])
        teeth_count = len(files["Teeth"])
        bone_count = len(files["Bone"])
        total_files = pulp_count + teeth_count + bone_count
        
        if total_files == 0:
            self.report({'WARNING'}, "Keine passenden STL-Dateien gefunden!")
            self.report({'INFO'}, "Erwartet: pulp_XX.stl, tooth_XX.stl, mandible.stl, maxilla.stl")
        else:
            self.report({'INFO'}, f"Gefunden: {pulp_count} Pulp, {teeth_count} Teeth, {bone_count} Bone")
            
            if files["Pulp"]:
                self.report({'INFO'}, f"Pulp Beispiel: {files['Pulp'][0][1]}")
            if files["Teeth"]:
                self.report({'INFO'}, f"Teeth Beispiel: {files['Teeth'][0][1]}")
            if files["Bone"]:
                self.report({'INFO'}, f"Bone Beispiel: {files['Bone'][0][1]}")
        
        return {'FINISHED'}

class VIRTUALENDO_OT_convert_to_ar(Operator):
    bl_idname = "virtualendo.convert_to_ar"
    bl_label = "Konvertieren"
    bl_description = "Konvertiert alle VirtualEndo STL-Dateien zum gewählten Format"
    
    def execute(self, context):
        settings = context.scene.virtualendo_settings
        
        # STL-Addon prüfen und aktivieren
        if not hasattr(bpy.ops.import_mesh, 'stl'):
            self.report({'INFO'}, "Aktiviere STL-Addon...")
            if not ensure_stl_addon() and not force_enable_stl():
                self.report({'ERROR'}, "STL Import konnte nicht aktiviert werden!")
                return {'CANCELLED'}
        
        # Eingabe-Validierung
        if not settings.input_folder or not os.path.exists(settings.input_folder):
            self.report({'ERROR'}, "Ungültiger Eingabeordner!")
            return {'CANCELLED'}
        
        # Ausgabeordner bestimmen
        if settings.use_custom_output and settings.output_folder:
            if not os.path.exists(settings.output_folder):
                self.report({'ERROR'}, f"Ausgabeordner existiert nicht: {settings.output_folder}")
                return {'CANCELLED'}
            output_dir = settings.output_folder
        else:
            output_dir = settings.input_folder
        
        # STL-Dateien kategorisieren
        files = categorize_stl_files(settings.input_folder)
        total_files = sum(len(file_list) for file_list in files.values())
        
        if total_files == 0:
            self.report({'ERROR'}, "Keine passenden STL-Dateien gefunden!")
            return {'CANCELLED'}
        
        # Import und Verarbeitung
        materials = get_materials(settings)
        imported_objects = []
        
        # Szene aufräumen
        self.report({'INFO'}, "Räume Szene auf...")
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

        # Import aller Kategorien
        for category, file_list in files.items():
            if not file_list:
                continue
                
            material_settings = materials.get(category)
            if not material_settings:
                continue
                
            mat = self.create_material(category, material_settings)
            self.report({'INFO'}, f"Importiere {len(file_list)} {category} Dateien...")

            for filepath, filename in file_list:
                try:
                    result = bpy.ops.import_mesh.stl(filepath=filepath)
                    if result == {'FINISHED'}:
                        obj = bpy.context.active_object
                        if obj and obj.type == 'MESH':
                            obj.data.materials.clear()
                            obj.data.materials.append(mat)
                            
                            clean_name = filename[:-4] if filename.endswith('.stl') else filename
                            obj.name = f"{category}_{clean_name}"
                            
                            imported_objects.append(obj)
                            self.report({'INFO'}, f"Importiert: {filename}")
                except Exception as e:
                    self.report({'ERROR'}, f"Fehler bei {filename}: {str(e)}")

        if not imported_objects:
            self.report({'ERROR'}, "Keine STL-Dateien erfolgreich importiert!")
            return {'CANCELLED'}

        # Objektverarbeitung
        self.report({'INFO'}, f"Verarbeite {len(imported_objects)} Objekte...")
        
        bpy.ops.object.select_all(action='DESELECT')
        for obj in imported_objects:
            obj.select_set(True)
        
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        for obj in imported_objects:
            if settings.center_objects:
                obj.location = (0, 0, 0)
            else:
                obj.location = (-0.1, -0.1, 0.08)
                
            obj.scale = (settings.scale_factor, settings.scale_factor, settings.scale_factor)
            
            if settings.smooth_shading:
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.shade_smooth()

        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Export
        bpy.ops.object.select_all(action='DESELECT')
        for obj in imported_objects:
            obj.select_set(True)
        
        # Export durchführen
        if settings.export_format == 'USDZ':
            export_path = os.path.join(output_dir, "VirtualEndo_Export.usdz")
            success = self.do_usdz_export(export_path)
        elif settings.export_format == 'GLB':
            export_path = os.path.join(output_dir, "VirtualEndo_Export.glb")
            success = self.do_glb_export(export_path)
        elif settings.export_format == 'FBX':
            export_path = os.path.join(output_dir, "VirtualEndo_Export.fbx")
            success = self.do_fbx_export(export_path)
        else:  # STL
            export_path = os.path.join(output_dir, "VirtualEndo_Export.stl")
            success = self.do_stl_export(export_path)
        
        if success:
            file_size = os.path.getsize(export_path)
            filename = os.path.basename(export_path)
            self.report({'INFO'}, f"Erfolgreich erstellt: {filename} ({file_size} Bytes)")
            self.report({'INFO'}, f"Speicherort: {export_path}")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Export fehlgeschlagen!")
            return {'CANCELLED'}

    def do_usdz_export(self, filepath):
        """Exportiert als USDZ-Datei"""
        try:
            if not hasattr(bpy.ops.wm, 'usd_export'):
                self.report({'ERROR'}, "USD Export nicht verfügbar! Verwenden Sie GLB stattdessen.")
                return False
            
            bpy.ops.wm.usd_export(
                filepath=filepath,
                selected_objects_only=True,
                export_materials=True,
                export_meshes=True,
                export_lights=False,
                export_cameras=False
            )
            
            return os.path.exists(filepath) and os.path.getsize(filepath) > 0
        except Exception as e:
            self.report({'ERROR'}, f"USDZ Export fehlgeschlagen: {str(e)}")
            return False
    
    def do_glb_export(self, filepath):
        """Exportiert als GLB-Datei"""
        try:
            bpy.ops.export_scene.gltf(
                filepath=filepath,
                export_format='GLB',
                use_selection=True,
                export_materials='EXPORT'
            )
            
            return os.path.exists(filepath) and os.path.getsize(filepath) > 0
        except Exception as e:
            self.report({'ERROR'}, f"GLB Export fehlgeschlagen: {str(e)}")
            return False

    def do_fbx_export(self, filepath):
        """Exportiert als FBX-Datei - Korrigierte Version"""
        try:
            # Basis-Parameter für FBX-Export
            export_params = {
                'filepath': filepath,
                'use_selection': True,
                'use_mesh_modifiers': True,
                'object_types': {'MESH'}
            }
            
            # Blender-Version spezifische Parameter
            blender_version = bpy.app.version
            
            # Für Blender 3.0+ verwende path_mode statt use_material_texture
            if blender_version >= (3, 0, 0):
                export_params.update({
                    'path_mode': 'AUTO',  # Automatische Pfadverwaltung
                    'embed_textures': False,  # Texturen nicht einbetten
                })
            else:
                # Für ältere Blender-Versionen
                export_params['use_material_texture'] = True
            
            # Optional: Weitere Parameter für bessere Kompatibilität
            export_params.update({
                'use_custom_props': False,  # Keine Custom Properties
                'add_leaf_bones': False,    # Keine zusätzlichen Bones
                'primary_bone_axis': 'Y',   # Bone-Ausrichtung
                'secondary_bone_axis': 'X',
                'mesh_smooth_type': 'FACE', # Smooth-Typ für Meshes
                'use_metadata': True,       # Metadaten einschließen
            })
            
            # FBX Export ausführen
            bpy.ops.export_scene.fbx(**export_params)
            
            # Erfolg prüfen
            if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                return True
            else:
                self.report({'ERROR'}, "FBX-Datei wurde nicht erstellt oder ist leer")
                return False
                
        except Exception as e:
            self.report({'ERROR'}, f"FBX Export fehlgeschlagen: {str(e)}")
            return False

    def do_stl_export(self, filepath):
        """Exportiert als STL-Datei"""
        try:
            bpy.ops.export_mesh.stl(
                filepath=filepath,
                use_selection=True,
                ascii=False,
                use_mesh_modifiers=True
            )
            
            return os.path.exists(filepath) and os.path.getsize(filepath) > 0
        except Exception as e:
            self.report({'ERROR'}, f"STL Export fehlgeschlagen: {str(e)}")
            return False

    def create_material(self, name, material_settings):
        """Erstellt ein Material mit den gegebenen Einstellungen"""
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        principled = nodes.new(type="ShaderNodeBsdfPrincipled")
        output = nodes.new(type="ShaderNodeOutputMaterial")
        links.new(principled.outputs["BSDF"], output.inputs["Surface"])

        color = material_settings.get("color", (0.8, 0.8, 0.8, 1.0))
        alpha = material_settings.get("alpha", 1.0)
        metallic = material_settings.get("metallic", 0.0)
        roughness = material_settings.get("roughness", 0.5)
        
        principled.inputs["Base Color"].default_value = color
        
        try:
            if "Alpha" in principled.inputs:
                principled.inputs["Alpha"].default_value = alpha
            if "Metallic" in principled.inputs:
                principled.inputs["Metallic"].default_value = metallic
            if "Roughness" in principled.inputs:
                principled.inputs["Roughness"].default_value = roughness
        except:
            pass
        
        if alpha < 1.0:
            mat.blend_method = 'BLEND'
            mat.use_backface_culling = False
            try:
                if hasattr(mat, "shadow_method"):
                    mat.shadow_method = 'HASHED'
            except:
                pass
        
        return mat

class VirtualEndoPanel(Panel):
    bl_label = "VirtualEndo"
    bl_idname = "PT_VirtualEndo"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "VirtualEndo"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.virtualendo_settings
        
        # STL Status
        box = layout.box()
        if hasattr(bpy.ops.import_mesh, 'stl'):
            box.label(text="STL Import verfügbar", icon='CHECKMARK')
        else:
            box.label(text="STL Import nicht verfügbar!", icon='ERROR')
            box.operator("virtualendo.enable_stl", text="STL Add-on aktivieren", icon='PLUS')
        
        # Input Ordner
        box = layout.box()
        box.label(text="VirtualEndo Ordner:", icon='FOLDER_REDIRECT')
        box.prop(settings, "input_folder", text="")
        
        if settings.input_folder:
            box.operator("virtualendo.scan_files", text="Dateien scannen", icon='VIEWZOOM')
        
        # Info Box
        info_box = layout.box()
        info_box.label(text="Erwartete Dateien:", icon='INFO')
        col = info_box.column(align=True)
        col.label(text="pulp_11.stl, pulp_12.stl, ...")
        col.label(text="tooth_11.stl, tooth_12.stl, ...")
        col.label(text="mandible.stl, maxilla.stl")
        
        # Material-Einstellungen
        box = layout.box()
        box.label(text="Material-Einstellungen:", icon='MATERIAL')
        
        col = box.column(align=True)
        col.label(text="Farben:")
        row = col.row(align=True)
        row.prop(settings, "color_pulp", text="")
        row.label(text="Pulp")
        
        row = col.row(align=True)
        row.prop(settings, "color_teeth", text="")
        row.label(text="Teeth")
        
        row = col.row(align=True)
        row.prop(settings, "color_bone", text="")
        row.label(text="Bone")
        
        box.separator()
        col = box.column(align=True)
        col.label(text="Transparenz:")
        col.prop(settings, "alpha_teeth", slider=True)
        col.prop(settings, "alpha_bone", slider=True)
        
        # Farbpresets
        box.separator()
        row = box.row()
        row.label(text="Presets:")
        
        row = box.row(align=True)
        op = row.operator("virtualendo.color_presets", text="Standard")
        op.preset_type = 'DEFAULT'
        op = row.operator("virtualendo.color_presets", text="Lehrreich") 
        op.preset_type = 'EDUCATIONAL'
        op = row.operator("virtualendo.color_presets", text="Präsentation")
        op.preset_type = 'PRESENTATION'
        
        # Objekt-Einstellungen
        box = layout.box()
        box.label(text="Objekt-Einstellungen:", icon='OBJECT_DATA')
        box.prop(settings, "scale_factor", slider=True)
        box.prop(settings, "smooth_shading")
        box.prop(settings, "center_objects")
        
        # Export-Einstellungen
        box = layout.box()
        box.label(text="Export-Einstellungen:", icon='EXPORT')
        
        row = box.row()
        row.prop(settings, "export_format", expand=True)
        
        if settings.export_format == 'USDZ':
            info_box = box.box()
            info_box.label(text="USDZ: Optimal für iOS AR", icon='INFO')
        elif settings.export_format == 'GLB':
            info_box = box.box()
            info_box.label(text="GLB: Universell kompatibel", icon='INFO')
        elif settings.export_format == 'FBX':
            info_box = box.box()
            info_box.label(text="FBX: Autodesk Standard", icon='INFO')
        else:  # STL
            info_box = box.box()
            info_box.label(text="STL: 3D-Druck Format", icon='INFO')
        
        box.separator()
        box.prop(settings, "use_custom_output")
        
        if settings.use_custom_output:
            sub = box.column()
            sub.prop(settings, "output_folder", text="")
            if not settings.output_folder:
                sub.label(text="Kein Ausgabeordner gewählt!", icon='ERROR')
        else:
            box.label(text="Ausgabe im Eingabeordner", icon='INFO')
        
        # Konvertierung
        box = layout.box()
        box.label(text="Konvertierung:", icon='PLAY')
        
        row = box.row()
        row.scale_y = 1.5
        
        button_text = f"Zu VirtualEndo_Export.{settings.export_format.lower()} konvertieren"
        op = row.operator("virtualendo.convert_to_ar", text=button_text, icon='EXPORT')
        
        button_enabled = bool(settings.input_folder)
        if settings.use_custom_output:
            button_enabled = button_enabled and bool(settings.output_folder)
        row.enabled = button_enabled
        
        if not button_enabled:
            if not settings.input_folder:
                box.label(text="Eingabeordner erforderlich", icon='ERROR')
            elif settings.use_custom_output and not settings.output_folder:
                box.label(text="Ausgabeordner erforderlich", icon='ERROR')
        
        # Ausgabe-Info
        if settings.input_folder:
            if settings.use_custom_output and settings.output_folder:
                output_dir = settings.output_folder
            else:
                output_dir = settings.input_folder
            
            output_name = f"VirtualEndo_Export.{settings.export_format.lower()}"
            layout.label(text=f"Ausgabe: {output_name}", icon='INFO')
            layout.label(text=f"in: {os.path.basename(output_dir)}/", icon='FOLDER_REDIRECT')

def register():
    print("Registriere VirtualEndo Add-on v2.1.1")
    
    ensure_stl_addon()
    
    bpy.utils.register_class(VirtualEndoSettings)
    bpy.types.Scene.virtualendo_settings = bpy.props.PointerProperty(type=VirtualEndoSettings)
    bpy.utils.register_class(VIRTUALENDO_OT_color_presets)
    bpy.utils.register_class(VIRTUALENDO_OT_enable_stl)
    bpy.utils.register_class(VIRTUALENDO_OT_scan_files)
    bpy.utils.register_class(VIRTUALENDO_OT_convert_to_ar)
    bpy.utils.register_class(VirtualEndoPanel)
    print("VirtualEndo Add-on v2.1.1 erfolgreich registriert")

def unregister():
    print("Deregistriere VirtualEndo Add-on v2.1.1")
    bpy.utils.unregister_class(VirtualEndoSettings)
    del bpy.types.Scene.virtualendo_settings
    bpy.utils.unregister_class(VIRTUALENDO_OT_color_presets)
    bpy.utils.unregister_class(VIRTUALENDO_OT_enable_stl)
    bpy.utils.unregister_class(VIRTUALENDO_OT_scan_files)
    bpy.utils.unregister_class(VIRTUALENDO_OT_convert_to_ar)
    bpy.utils.unregister_class(VirtualEndoPanel)
    print("VirtualEndo Add-on v2.1.1 erfolgreich deregistriert")

if __name__ == "__main__":
    register()
