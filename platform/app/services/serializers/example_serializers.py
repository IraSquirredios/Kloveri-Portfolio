from ...schemas.example_schemas import ProfileModel, ProjectModel, ProjectRegistryObject


def serialize_registry_entry_to_project_model(data: dict) -> ProjectModel | None:
    try:
        data = ProjectRegistryObject(**data)
    except Exception as e:
        print(f"Ошибка сериализации в методе serialize_registry_entry_to_project_model, "
              f"схема ProjectRegistryObject.\n"
              f"Тип исключения: {type(e).__name__}\nСообщение: {str(e)}\n"
              f"Объект: {data}")
    output_data = {
        "project_id": data.id,
        "project_type": data.object_type,
        "project_name": data.name,
        "message": data.data.message
    }
    try:
        output_model = ProjectModel(**output_data)
        return output_model
    except Exception as e:
        print(f"Ошибка сериализации в методе serialize_registry_entry_to_project_model, "
              f"схема ProjectModel.\n"
              f"Тип исключения: {type(e).__name__}\nСообщение: {str(e)}\n"
              f"Объект: {output_data}")


def serialize_profile_entry_to_profile_model(data: dict) -> ProfileModel | None:
    try:
        profile_model = ProfileModel(**data)
        return profile_model
    except Exception as e:
        print(f"Ошибка сериализации в методе serialize_profile_entry_to_profile_model, "
              f"схема ProfileModel.\n"
              f"Тип исключения: {type(e).__name__}\nСообщение: {str(e)}\n"
              f"Объект: {data}")
