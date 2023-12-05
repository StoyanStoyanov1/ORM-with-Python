import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

# Create queries within functions
from django.db.models import QuerySet, F
from main_app.models import Pet
from main_app.models import Artifact
from main_app.models import Location
from main_app.models import Car
from main_app.models import Task
from main_app.models import HotelRoom
from main_app.models import Character


def create_pet(name: str, species: str) -> str:
    pet = Pet.objects.create(
        name=name,
        species=species
    )

    return f"{pet.name} is a very cute {pet.species}!"


# print(create_pet('Buddy', 'Dog'))
# print(create_pet('Whiskers', 'Cat'))
# print(create_pet('Rocky', 'Hamster'))


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool) -> str:
    artifact = Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical,
    )

    return f"The artifact {artifact.name} is {artifact.age} years old!"


def delete_all_artifacts() -> None:
    Artifact.objects.all().delete()


# print(create_artifact('Ancient Sword', 'Lost Kingdom', 500, 'A legendary sword with a rich history', True))
# print(create_artifact('Crystal Amulet', 'Mystic Forest', 300, 'A magical amulet believed to bring good fortune',True))

# delete_all_artifacts()

def show_all_locations() -> str:
    all_locations = Location.objects.all().order_by('-id')

    return '\n'.join(str(l) for l in all_locations)


def new_capital() -> None:
    location = Location.objects.first()
    location.is_capital = True
    location.save()


def get_capitals() -> QuerySet:
    return Location.objects.filter(is_capital=True).values('name')


def delete_first_location() -> None:
    Location.objects.first().delete()


# print(show_all_locations())
# print(new_capital())
# print(get_capitals())


def apply_discount() -> None:
    for car in Car.objects.all():
        percent = sum(int(d) for d in str(car.year)) / 100
        discount = float(car.price) * percent
        car.price_with_discount = float(car.price) - discount
        car.save()


# apply_discount()


def get_recent_cars() -> QuerySet:
    return Car.objects.filter(year__gte=2020).values('model', 'price_with_discount', )


# print(get_recent_cars())


def delete_last_car() -> None:
    Car.objects.last().delete()


# delete_last_car()


def show_unfinished_tasks() -> str:
    all_unfinished_tasks = Task.objects.filter(is_finished=False)

    return '\n'.join(str(task) for task in all_unfinished_tasks)


# print(show_unfinished_tasks())


def complete_odd_tasks() -> None:
    for task in Task.objects.all():
        if task.id % 2 != 0:
            task.is_finished = True
            task.save()


complete_odd_tasks()


def encode_and_replace(text: str, task_title: str) -> None:
    tasks_with_matching_title = Task.objects.filter(title=task_title)
    decoded_text = ''.join(chr(ord(x) - 3) for x in text)

    for task in tasks_with_matching_title:
        task.description = decoded_text
        task.save()


# encode_and_replace("Zdvk#wkh#glvkhv$", "Simple Task")
# print(Task.objects.get(title ='Simple Task') .description)


def get_deluxe_rooms() -> str:
    deluxe_rooms = HotelRoom.objects.filter(room_type='Deluxe')
    even_id_deluxe_rooms = [str(room) for room in deluxe_rooms if room.id % 2 == 0]

    return '\n'.join(even_id_deluxe_rooms)


# print(get_deluxe_rooms())


def increase_room_capacity() -> None:
    rooms = HotelRoom.objects.all().order_by('id')

    previous_room_capacity = None

    for room in rooms:
        if not room.is_reserved:
            continue

        if previous_room_capacity:
            room.capacity += previous_room_capacity
        else:
            room.capacity += room.id

        previous_room_capacity = room.capacity

        room.save()


# increase_room_capacity()


def reserve_first_room() -> None:
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()


# reserve_first_room()


def delete_last_room() -> None:
    last_room = HotelRoom.objects.last()

    if last_room.is_reserved:
        last_room.delete()


# delete_last_room()

# character1 = Character.objects.create(
#     name="Gandalf",
#     class_name="Mage",
#     level=10,
#     strength=15,
#     dexterity=20,
#     intelligence=25,
#     hit_points=100,
#     inventory="Staff of Magic, Spellbook",
# )
#
# character2 = Character.objects.create(
#     name="Hector",
#     class_name="Warrior",
#     level=12,
#     strength=30,
#     dexterity=15,
#     intelligence=10,
#     hit_points=150,
#     inventory="Sword of Troy, Shield of Protection",
# )

def update_characters() -> None:
    Character.objects.filter(class_name='Mage').update(
        level=F('level') + 3,
        intelligence=F('intelligence') - 7,
    )

    Character.objects.filter(class_name='Warrior').update(
        hit_points=F('hit_points') / 2,
        dexterity=F('dexterity') + 4,
    )

    Character.objects.filter(class_name__in=["Assassin", "Scout"]).update(
        inventory="The inventory is empty",
    )


# update_characters()


def fuse_characters(first_character: Character, second_character: Character) -> None:
    fusion_name = first_character.name + ' ' + second_character.name
    fusion_level = (first_character.level + second_character.level) // 2
    fusion_class = 'Fusion'
    fusion_strength = (first_character.strength + second_character.strength) * 1.2
    fusion_dexterity = (first_character.dexterity + second_character.dexterity) * 1.4
    fusion_intelligence = (first_character.intelligence + second_character.intelligence) * 1.5
    fusion_hit_points = (first_character.hit_points + second_character.hit_points)

    fusion_inventory = "Bow of the Elven Lords, Amulet of Eternal Wisdom" \
        if first_character.class_name in ['Mage', 'Scout'] \
        else "Dragon Scale Armor, Excalibur"

    Character.objects.create(
        name=fusion_name,
        class_name=fusion_class,
        level=fusion_level,
        strength=fusion_strength,
        dexterity=fusion_dexterity,
        intelligence=fusion_intelligence,
        hit_points=fusion_hit_points,
        inventory=fusion_inventory
    )

    first_character.delete()
    second_character.delete()


def grand_dexterity() -> None:
    Character.objects.update(dexterity=30)


def grand_intelligence() -> None:
    Character.objects.update(intelligence=40)


def grand_strength() -> None:
    Character.objects.update(strength=50)


def delete_characters() -> None:
    Character.objects.filter(inventory="The inventory is empty").delete()
