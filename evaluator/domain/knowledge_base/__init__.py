from Py_FCM import FuzzyCognitiveMap


def load_project_fcm():
    with open('kb_stored/project_kb.json', 'r') as file:
        project_kb_json = file.read()
        return FuzzyCognitiveMap.from_json(project_kb_json)
