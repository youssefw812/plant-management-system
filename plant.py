from datetime import datetime
import json
plants = []

def save_plants():
    with open("plants.json", "w", encoding="utf-8") as file:
        json.dump(
            plants,
            file,
            indent=4,
            ensure_ascii=False
        )

def load_plants():
    global plants
    try:
        with open("plants.json", "r", encoding="utf-8") as file:
            plants = json.load(file)

    except FileNotFoundError:
        plants = []
def add_plant(name, watering_interval):
    plants.append({
        'name': name,
        'last_watered': datetime.now().strftime("%Y-%m-%d"),
        'fertilized': datetime.now().strftime("%Y-%m-%d"),
        'watering_interval': watering_interval
    })

    save_plants()

def show_plants():
    if not plants:
        print("لا يوجد نباتات في القائمة.🌱")
        return
    for plant in plants:
        print(f"{plant['name']} اخر مرة اتسقى {plant['last_watered']} و يحتاج الى سقاية كل {plant['watering_interval']} يوم")

def check_watering():
    today = datetime.now().date()
    for plant in plants:
        last_watered_date = datetime.strptime(plant['last_watered'], "%Y-%m-%d").date()
        days_since_watered = (today - last_watered_date).days
        if days_since_watered >= plant['watering_interval']:
            print(f"{plant['name']} يحتاج الى سقاية🛑")
        else:
            print(f"{plant['name']} لا يحتاج الى سقاية✅")

def update_watering(name):
    for plant in plants:
        if plant['name'] == name:
            plant['last_watered'] = datetime.now().strftime("%Y-%m-%d")
            save_plants()
            print(f"{plant['name']} تم تحديث تاريخ السقاية الى {plant['last_watered']}✅")
            return
    print(f"لم يتم العثور على نبات باسم❌ {name}")

def remove_plant(name):
    for plant in plants:
        if plant['name'] == name:
            plants.remove(plant)
            save_plants()
            print(f"{plant['name']} تم ازالته من القائمة✅")
            return
    print(f"لم يتم العثور على نبات باسم❌ {name}")

def check_fertilizer():
    for plant in plants:
        last_fertilized_date = datetime.strptime(plant['fertilized'], "%Y-%m-%d").date()
        days_since_fertilized = (datetime.now().date() - last_fertilized_date).days
        if days_since_fertilized >= 30:
            print(f"{plant['name']} يحتاج الى تسميد🛑")
        else:
            print(f"{plant['name']} لا يحتاج الى تسميد✅")

def update_fertilizer(name):
    for plant in plants:
        if plant['name'] == name:
            plant['fertilized'] = datetime.now().strftime("%Y-%m-%d")
            save_plants()
            print(f"{plant['name']} تم تحديث تاريخ التسميد الى {plant['fertilized']}✅")
            return
    print(f"لم يتم العثور على نبات باسم❌ {name}")
def edit_plant(old_name, new_name, watering_interval,
               last_watered, fertilized):

    for plant in plants:

        if plant["name"] == old_name:

            plant["name"] = new_name
            plant["watering_interval"] = watering_interval
            plant["last_watered"] = last_watered
            plant["fertilized"] = fertilized

            save_plants()
            return

def update_fertilizer(name):

    for plant in plants:

        if plant["name"] == name:

            plant["fertilized"] = datetime.now().strftime(
                "%Y-%m-%d"
            )

            save_plants()
            return
        