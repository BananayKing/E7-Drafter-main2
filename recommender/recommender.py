import ast
import json
import pandas as pd
import math
class DraftRecommender:
    def __init__(self, csv_path, json_path):
        # Load and parse data
        self.df = pd.read_csv(csv_path)
        self.df['slot_winrates'] = self.df['slot_winrates'].apply(ast.literal_eval)
        self.df['synergy'] = self.df['synergy'].apply(ast.literal_eval)
        self.df['counters'] = self.df['counters'].apply(ast.literal_eval)

        # Load hero metadata
        with open(json_path, 'r') as f:
            self.hero_data = json.load(f)
        self.code_to_name = {v['code']: k for k, v in self.hero_data.items()}



    def _get_slot_winrate(self, hero_row, next_pick, first_pick):
        PICK_NUMBER_TO_DATASET_PICK = {

                1: "1",
                4: "2/3",
                5: "2/3",
                8: "4/5",
                9: "4/5",
                2: "1/2",
                3: "1/2",
                6: "3/4",
                7: "3/4",
                10: "5",
            }
    


        # Ensure next_pick is an integer and first_pick is a valid string ('First' or 'Second')
        if not isinstance(next_pick, int):
            raise ValueError("next_pick should be an integer")
        if first_pick not in ['First', 'Second']:
            print(first_pick)
            raise ValueError("first_pick should be either 'First' or 'Second'")

        # Determine the pick type based on first_pick
        pick_type = first_pick
        # Find the correct pick number info
        pick_info = PICK_NUMBER_TO_DATASET_PICK.get(next_pick)
        if not pick_info:
            return 0  # No matching pick number found

        # Ensure hero_row has 'slot_winrates' as a list

        # Now match with slot_winrates entry
        for entry in hero_row['slot_winrates']:
            if entry.get('pick_number') == pick_info:
                win_rate = entry.get('final_winrate', 0) / 100.0 *10
                pick_rate = entry.get('pickrate', 0) / 100.0
                games_played = entry.get('games_played', 1)

                # Return the weighted winrate
                    # Early picks: stronger influence (but no ^7 absurdity)
                weight = games_played * pick_rate 
                return (win_rate**7) * weight /100

        return 1  # No matching entry found



    def _get_synergy_score(self, hero_row, my_picks):
        if not my_picks:
            return 0.0
        scores = []
        for entry in hero_row['synergy']:
            if entry['name'] in my_picks:
                win_rate = entry['winrate'] / 100.0 *10
                pick_rate = entry['pickrate'] / 100.0
                games_played = entry.get('games_played', 1)
                weight = pick_rate * math.log(games_played)
                scores.append(win_rate * weight * 100)
        return sum(scores) / len(scores) if scores else 0

    def _get_counter_score(self, hero_row, enemy_picks):
        if not enemy_picks:
            return 0.0
        scores = []
        for entry in hero_row['counters']:
            if entry['name'] in enemy_picks:
                win_rate = entry['winrate'] / 100.0 *10
                pick_rate = entry['pickrate'] / 100.0
                games_played = entry.get('games_played', 1)
                weight = pick_rate * math.log(games_played)
                scores.append(win_rate * weight * 100)
        return sum(scores) / len(scores) if scores else 0

    def recommend(self, picks, selected_characters=None, my_team_name='My Team'):
        if not picks:
            results = []
            for _, row in self.df.iterrows():
                if selected_characters and row['heroid'] not in selected_characters:
                    continue
                slot_score = self._get_slot_winrate(row, next_pick=1, first_pick="First")
                score = slot_score
                results.append({
                    'heroid': row['heroid'],
                    'hero_name': self.code_to_name.get(row['heroid'], 'Unknown'),
                    'score': round(score),
                    'slot_score': round(slot_score),
                    'syn_score': 0,
                    'cnt_score': 0
                })
            top_5 = sorted(results, key=lambda x: x['score'], reverse=True)[:5]
            return top_5

        picked_orders = {p['pick_order'] for p in picks}
        next_pick = min(o for o in range(1, max(picked_orders) + 6) if o not in picked_orders)

        first_pick = "First" if any(p['first_pick'] == 1 and p['Team'] == my_team_name for p in picks) else "Second"
        my_picks = [p['Hero'] for p in picks if p['Team'] == my_team_name]
        enemy_picks = [p['Hero'] for p in picks if p['Team'] != my_team_name]

        taken = set(my_picks + enemy_picks)
        candidates = self.df[~self.df['heroid'].isin(taken)]
        if selected_characters:
            candidates = candidates[candidates['heroid'].isin(selected_characters)]

        results = []
        for _, row in candidates.iterrows():
            slot_score = self._get_slot_winrate(row, next_pick, first_pick)
            syn_score = self._get_synergy_score(row, my_picks)
            cnt_score = self._get_counter_score(row, enemy_picks)
            score = 0.33 * (syn_score * slot_score) + 0.66 * (cnt_score * slot_score)
            results.append({
                'heroid': row['heroid'],
                'hero_name': self.code_to_name.get(row['heroid'], 'Unknown'),
                'score': round(score),
                'slot_score': round(slot_score),
                'syn_score': round(syn_score),
                'cnt_score': round(cnt_score)
            })
        top_5 = sorted(results, key=lambda x: x['score'], reverse=True)[:5]
        return top_5
if __name__ == '__main__':
    recommender = DraftRecommender(
        '/winrate_data.csv',
        '/herodata.json'
    )
    picks ={
  "picks": [
 {"pick_order": 2, "Team": "My Team", "Hero": "c2124", "first_pick": 0},
    {"pick_order": 1, "Team": "Enemy Team", "Hero": "c2066", "first_pick": 1}]
}
    top_5, info = recommender.recommend(picks)
    print(f"Next pick order: {info['pick_order']}, Team: {'My Team' if info['first_pick'] else 'Enemy'}")
    print("Top 5 recommended heroes:")
    for hero in top_5:
        print(hero['hero_name'], hero)