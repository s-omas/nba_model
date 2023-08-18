from prob_model.models import Team, Game, Schedule, Result, Sim, Prediction
import random


def elo_win_probability(rating_a, rating_b):
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))


def simulate_elo_with_sampling(mean_a, std_a, mean_b, std_b, num_iterations=1000):
    total_probability = 0

    for i in range(num_iterations):
        # Randomly sample ratings from the normal distributions
        rating_player_a = random.gauss(mean_a, std_a)
        rating_player_b = random.gauss(mean_b, std_b)

        # Calculate Elo win probability using the sampled ratings
        probability = elo_win_probability(rating_player_a, rating_player_b)
        total_probability += probability

    average_probability = total_probability / num_iterations
    return average_probability


#calculate winner probabilites given ratings
def make_prediction(game):
    print("making prediction for game " + str(game.game_id))
    away_rtg = game.away_team.team_sim.first().rating
    away_var = game.away_team.team_sim.first().variance
    home_rtg = game.home_team.team_sim.first().rating
    home_var = game.home_team.team_sim.first().variance
    prob_home_win = simulate_elo_with_sampling(home_rtg, home_var, away_rtg, away_var, num_iterations=1000)
    if prob_home_win >= 0.5:
        win = game.home_team
        los = game.away_team
        pct = prob_home_win
    else:
        win = game.away_team
        los = game.home_team
        pct = 1 - prob_home_win
    new_pred = Prediction(
        expected_winner = win,
        expected_loser = los,
        winner_pct = 100 * pct,
        loser_pct = 100 * (1 - pct),
        home_team_rating = home_rtg,
        home_team_variance = home_var,
        away_team_rating = away_rtg,
        away_team_variance = away_var
    )
    print("... done")
    return new_pred

#set predictions for every team's next game
def update_predictions(games_list):
    for g in games_list:
        if not g.prediction:
            new = make_prediction(g)
            new.save()
            g.prediction = new
            g.save()

def update_sim(game):
    k = 20 #rating change factor
    m = 5 #var change factor

    prediction = game.prediction
    result = game.result
    winner_sim = result.winner.team_sim.first()
    loser_sim = result.loser.team_sim.first()

    if result.winner == prediction.expected_winner:
        p = prediction.winner_pct / 100
    else:
        p = prediction.loser_pct / 100
    
    print(k * (1 - p))

    winner_sim.rating = winner_sim.rating + k * (1 - p)
    loser_sim.rating = loser_sim.rating + k * (- p)

    winner_sim.variance = winner_sim.variance - m * (p - 0.5)
    loser_sim.variance = loser_sim.variance - m * (p - 0.5)

    winner_sim.save()
    loser_sim.save()
    print("here")

