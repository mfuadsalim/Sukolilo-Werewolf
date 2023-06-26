import random
data = {
    '123456': {
        'num_players': '4',
        'player_list': [
            {'name': 'Isol', 'role': '', 'status': 'alive',
                'has_voted': False, 'has_acted': False},
            {'name': 'Fuad', 'role': '', 'status': 'alive',
                'has_voted': False, 'has_acted': False},
            {'name': 'Monica', 'role': '', 'status': 'alive',
                'has_voted': False, 'has_acted': False},
            {'name': 'Khariza', 'role': '', 'status': 'alive',
                'has_voted': False, 'has_acted': False},
        ]
    }
}

num_players = 4
if num_players == 4:
    avatars = ['Werewolf', 'Seeker', 'Villager', 'Villager']
elif num_players == 8:
    avatars = ['Werewolf', 'Werewolf', 'Seeker', 'Villager',
               'Villager', 'Villager', 'Villager', 'Villager']
elif num_players == 12:
    avatars = ['Werewolf', 'Werewolf', 'Werewolf', 'Seeker', 'Seeker',
               'Villager', 'Villager', 'Villager', 'Villager', 'Villager', 'Villager', 'Villager']

random.shuffle(avatars)

# Perform start game logic with avatars here
for i, player in enumerate(data['123456']['player_list']):
    avatar = avatars[i]
    data['123456']['player_list'][i]['role'] = avatar

print(data)
