import random, json

DATA_FILE = "/app/data/game_db.json"

class ReturnObject:
    def __init__(self, message:str = "None", chat_id: int = None):
        self.message = message
        self.chat_id = chat_id

def code_generate() -> int:
    code = [random.randint(1, 10) for _ in range(6)]
    return int("".join(map(str, code)))

def append_group(chat_id: str, code: int):
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = {}
    
    if chat_id in data.keys(): return data[chat_id]["code"]

    data[chat_id] = {
        "code": code,
        "players": []
    }

    with open(DATA_FILE, "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    return 1

def delete_group(chat_id: str):
    with open(DATA_FILE, encoding='utf-8') as file:
        data = json.load(file)
    if chat_id in data.keys():
        data.pop(chat_id)
        with open(DATA_FILE, "w", encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
def add_player(username: str, code: int) -> ReturnObject:
    with open(DATA_FILE, encoding='utf-8') as file:
        data = json.load(file)
    result: ReturnObject = ReturnObject("Игра не найдена")
    for group in data.keys():
        if username in data[group]["players"]:
                result.message = "Ты уже состоишь в игре"
                break
        if data[group]["code"] == code:
            if len(data[group]["players"]) >=8: 
                result.message = f"Максимум 8 игроков"
                break
            if username not in data[group]["players"]:
                data[group]["players"].append(username)
                result.message = f"Теперь ты состоишь в игре! Жди начала"
                result.chat_id = int(group)
                break
    with open(DATA_FILE, "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    return result

def get_players(chat_id: str):
    with open(DATA_FILE, encoding='utf-8') as file:
        data = json.load(file)
    if data[chat_id]: return data[chat_id]["players"]