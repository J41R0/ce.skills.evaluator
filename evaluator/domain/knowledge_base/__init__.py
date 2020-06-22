from Py_FCM import from_json, FuzzyCognitiveMap


def load_project_fcm():
    with open('kb_stored/project_kb.json', 'r') as file:
        project_kb_json = file.read()
        knowledge_base = from_json(project_kb_json)
        knowledge_base.set_map_decision_function("exited")
        return knowledge_base
