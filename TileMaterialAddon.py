import bpy
import os

def update_texture(self, context):
    material_name = "TileMaterial"

    # Приведение пути к стандартному виду
    raw_path = self.tile_a_1
    texture_path = bpy.path.abspath(raw_path)
    normalized_path = os.path.normpath(texture_path)

    material = bpy.data.materials.get(material_name)

    nodes = material.node_tree.nodes
    texture_node = nodes.get("Tile_a_0")

    # Загрузка текстуры
    try:
        texture = bpy.data.images.load(normalized_path)
        print(f"Texture loaded: {texture.name}")
        texture_node.image = texture
        print(f"Texture '{normalized_path}' assigned to node 'Tile_a_0'")
    except Exception as e:
        print(f"Failed to load texture '{normalized_path}': {e}")
        

class SimpleToolPanel(bpy.types.Panel):
    bl_label = "Tile Shader Inspector"
    bl_idname = "VIEW3D_PT_tile_shader_inspector"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Custom Tools"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        props = context.scene.texture_path_properties
        row.operator("object.apply_tile_shader", text="Apply Tile Shader")

        # Рисуем поля ввода
        for i in range(1, 5):
            layout.prop(props, f"tile_a_{i}")

# Создаем свойства для хранения путей до текстур
class TexturePathProperties(bpy.types.PropertyGroup):
    tile_a_1: bpy.props.StringProperty(
        name="Tile_a 1",
        description="Path to the first Tile_a texture",
        subtype='FILE_PATH',  # Тип 'FILE_PATH' делает поле удобным для выбора файлов
        update=update_texture  # Привязываем обновление
    )
    tile_a_2: bpy.props.StringProperty(
        name="Tile_a 2",
        description="Path to the second Tile_a texture",
        subtype='FILE_PATH'
    )
    tile_a_3: bpy.props.StringProperty(
        name="Tile_a 3",
        description="Path to the third Tile_a texture",
        subtype='FILE_PATH'
    )
    tile_a_4: bpy.props.StringProperty(
        name="Tile_a 4",
        description="Path to the fourth Tile_a texture",
        subtype='FILE_PATH'
    )

class ApplyTileShaderOperator(bpy.types.Operator):
    bl_idname = "object.apply_tile_shader"
    bl_label = "Apply Tile Shader"

    def execute(self, context):
        # Проверка, есть ли активный объект
        obj = context.active_object
        if not obj:
            self.report({'WARNING'}, "No active object selected")
            return {'CANCELLED'}
        
        # Проверяем, есть ли у объекта минимум два UV-канала
        if not hasattr(obj.data, "uv_layers") or len(obj.data.uv_layers) < 2:
            self.report({'WARNING'}, "Object must have 2 UV channels")
            return {'CANCELLED'}

        # Проверка, есть ли материал TileMaterial
        material_name = "TileMaterial"
        material = bpy.data.materials.get(material_name)
        if not material:
            self.report({'WARNING'}, f"Material '{material_name}' not found")
            return {'CANCELLED'}

        # Переименование UV-каналов объекта
        uv_layers = obj.data.uv_layers
        uv_name_1 = uv_layers[0].name
        uv_layers[0].name = "UVMap_1"
        self.report({'INFO'}, f"The first UV Map was renamed from '{uv_name_1}' to '{uv_layers[0].name}'")
        
        uv_name_2 = uv_layers[1].name
        uv_layers[1].name = "UVMap_2"
        self.report({'INFO'}, f"The second UV Map was renamed from '{uv_name_2}' to '{uv_layers[1].name}'")

        # Проверяем, есть ли у объекта слот материала, если нет - добавляем
        if len(obj.data.materials) == 0:
            obj.data.materials.append(material)
        else:
            # Применяем материал в первый слот
            obj.data.materials[0] = material

        self.report({'INFO'}, f"Material '{material_name}' applied to {obj.name}")
        return {'FINISHED'}


# Регистрация классов
def register():
    bpy.utils.register_class(SimpleToolPanel)
    bpy.utils.register_class(ApplyTileShaderOperator)
    bpy.utils.register_class(TexturePathProperties)
    
    # Добавляем свойства в контекст сцены
    bpy.types.Scene.texture_path_properties = bpy.props.PointerProperty(type=TexturePathProperties)


def unregister():
    bpy.utils.unregister_class(SimpleToolPanel)
    bpy.utils.unregister_class(ApplyTileShaderOperator)
    bpy.utils.unregister_class(TexturePathProperties)
    del bpy.types.Scene.texture_path_properties


if __name__ == "__main__":
    register()