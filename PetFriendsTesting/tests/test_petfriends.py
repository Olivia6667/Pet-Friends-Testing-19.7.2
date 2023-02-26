from api import PetFriends
from settings import valid_email, valid_password
import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

pf = PetFriends()


def test_get_api_key_for_invalid_user(email='ayanamikate@mail.ru', password=valid_password):

    status, result = pf.get_api_key(email, password)

    assert status != 200
    assert 'key' in result

def test_add_new_pet_without_photo_valid(name='Lкукеe', animal_type='cat',
                                     age='3'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


def test_update_pet_photo_valid(pet_id='fb8bb9b3-b855-4488-8c0c-e1e5efc600e6', pet_photo='images/kitty.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.update_pet_photo(auth_key, pet_id, pet_photo)

    assert status == 200

def test_add_new_pet_with_invalid_age(name='Донни', animal_type='dog',
                                     age='lala', pet_photo='images/cat1.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status != 200
    assert result['name'] == name

def test_add_new_pet_without_photo_invalid_add_photo(name='Микки', animal_type='мышь',
                                     age='5', pet_photo='images/cat1.jpg'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age, pet_photo)

    assert status != 200
    assert result['name'] == name

def test_get_all_pets_with_invalid_email(filter=''):

    _, auth_key = pf.get_api_key('ayanamikate@mail.ru', valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status != 200
    assert len(result['pets']) > 0

def test_update_pet_photo_invalid_id(pet_id='fb8bb9b3-b855-4488-8c0c-e1e5efc60077', pet_photo='images/kitty.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.update_pet_photo(auth_key, pet_id, pet_photo)

    assert status != 200

def test__delete_not_existing_pet():

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")


    pet_id = my_pets['pets'][4]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status != 200
    assert pet_id not in my_pets.values()

def test_add_new_pet_with_invalid_photo_file(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/01_-_Alphabet.mp3'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status != 200
    assert result['name'] == name

def test_update_self_pet_info_invalid_pet(name='Микки', animal_type='cat', age=7):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][5]['id'], name, animal_type, age)

        assert status != 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")