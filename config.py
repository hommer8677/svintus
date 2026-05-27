import random, json

DATA_FILE = "/app/data/game_db.json"

def code_generate() -> int:
    code = [random.randint(1, 10) for _ in range(6)].join()
    return int("".join(map(str, code)))

def append_group(chat_id: str, code: int):
    with open(DATA_FILE, encoding='utf-8') as file:
        data = json.load(file)
    if chat_id in data.keys(): return "Игра уже началась"
    
    data[chat_id] = code
    with open(DATA_FILE, "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    return f"Комната создана! Код комнаты: {code}"
def delete_group(chat_id: str):
    with open(DATA_FILE, encoding='utf-8') as file:
        data = json.load(file)
    if chat_id in data.keys():
        data.pop(chat_id)
        with open(DATA_FILE, "w", encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)