from collections import Counter

def get_winner(votes):
    vote_counts = Counter(votes)
    most_common = vote_counts.most_common(2)
    if len(most_common) == 1 or most_common[0][1] > most_common[1][1]:
        return most_common[0][0]
    else:
        return None

voting_results = ['w', 'e', 'r', 'q']
winner = get_winner(voting_results)

if winner:
    print(f"The player with the most votes is: {winner}")
else:
    print("There is no clear winner.")
