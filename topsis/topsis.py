import math
import scipy.stats as ss


def build_denominators_for_normalization(number_of_criteria, decision_matrix):
    sum_matrix_columns = []

    for _ in range(number_of_criteria):
        sum_matrix_columns.append(0)

    for alternative_scores in decision_matrix:
        for index, score in enumerate(alternative_scores):
            sum_matrix_columns[index] = sum_matrix_columns[index] + pow(score, 2)

    denominators = []

    for sum_score in sum_matrix_columns:
        denominators.append(math.sqrt(sum_score))

    return denominators


def build_weighted_normalized_matrix(number_of_criteria, decision_matrix, weight):
    denominators = build_denominators_for_normalization(number_of_criteria, decision_matrix)
    # print(denominators)
    # print("\n")

    weighted_normalized_matrix = []

    for alternative_scores in decision_matrix:
        weighted_normalized_alternative_scores = []

        for column_number in range(number_of_criteria):
            weighted_normalized_score = weight[column_number] * alternative_scores[column_number] / denominators[column_number]
            weighted_normalized_alternative_scores.append(weighted_normalized_score)
        
        weighted_normalized_matrix.append(weighted_normalized_alternative_scores)

    # print(weighted_normalized_matrix)
    # print("\n")

    return weighted_normalized_matrix


def build_matrix_for_ideal_solution(number_of_criteria, weighted_normalized_matrix):
    # positive_ideal_solution_matrix = []
    matrix_for_ideal_solution = []

    for _ in range(number_of_criteria):
        # positive_ideal_solution_matrix.append(0)
        matrix_for_ideal_solution.append([])
    
    for weighted_scores in weighted_normalized_matrix:
        for index, score in enumerate(weighted_scores):
            matrix_for_ideal_solution[index].append(score)

    return matrix_for_ideal_solution


def get_ideal_solution(number_of_criteria, matrix_for_ideal_solution, criteria_type, solution_type):
    ideal_solution_matrix = []

    for _ in range(number_of_criteria):
        ideal_solution_matrix.append(0)

    criterion_type = "benefit" if solution_type == "positive" else "cost"
    
    for index, ideal_solution_scores in enumerate(matrix_for_ideal_solution):
        if criteria_type[index] == criterion_type:
            ideal_solution_matrix[index] = max(ideal_solution_scores)
        else:
            ideal_solution_matrix[index] = min(ideal_solution_scores)
    
    return ideal_solution_matrix


def get_distance_from_positive_ideal(weighted_normalized_matrix, positive_ideal_solutions):
    distance_from_positive = []

    for weighted_scores in weighted_normalized_matrix:
        sum_distance = 0

        for index, weighted_score in enumerate(weighted_scores):
            sum_distance = sum_distance + pow(positive_ideal_solutions[index] - weighted_score, 2)

        distance = math.sqrt(sum_distance)
        
        distance_from_positive.append(distance)

    return distance_from_positive


def get_distance_from_negative_ideal(weighted_normalized_matrix, negative_ideal_solutions):
    distance_from_negative = []

    for weighted_scores in weighted_normalized_matrix:
        sum_distance = 0

        for index, weighted_score in enumerate(weighted_scores):
            sum_distance = sum_distance + pow(weighted_score - negative_ideal_solutions[index], 2)

        distance = math.sqrt(sum_distance)
        
        distance_from_negative.append(distance)

    return distance_from_negative


def get_relative_closeness_to_ideal_solution(distance_from_positive, distance_from_negative):
    relative_closeness = []

    for index, positive_distance in enumerate(distance_from_positive):
        relative_closeness.append(distance_from_negative[index] / (positive_distance + distance_from_negative[index]))
    
    return relative_closeness


def topsis(weight, decision_matrix, criteria_type):
    # print(decision_matrix)
    # print("\n")
    
    number_of_criteria = len(weight)

    weighted_normalized_matrix = build_weighted_normalized_matrix(number_of_criteria, decision_matrix, weight)

    # print(weighted_normalized_matrix)
    # print("\n")

    matrix_for_ideal_solution = build_matrix_for_ideal_solution(number_of_criteria, weighted_normalized_matrix)
    positive_ideal_solutions = get_ideal_solution(number_of_criteria, matrix_for_ideal_solution, criteria_type, "positive")
    negative_ideal_solutions = get_ideal_solution(number_of_criteria, matrix_for_ideal_solution, criteria_type, "negative")

    # print(positive_ideal_solutions)
    # print("\n")
    # print(negative_ideal_solutions)
    # print("\n")

    distance_from_positive = get_distance_from_positive_ideal(weighted_normalized_matrix, positive_ideal_solutions)

    # print(distance_from_positive)
    # print("\n")

    distance_from_negative = get_distance_from_negative_ideal(weighted_normalized_matrix, negative_ideal_solutions)

    # print(distance_from_negative)
    # print("\n")

    relative_closeness = get_relative_closeness_to_ideal_solution(distance_from_positive, distance_from_negative)
    rank = ss.rankdata(relative_closeness, "ordinal")

    # print(relative_closeness)
    # print("\n")
    # print(rank)
    
    return relative_closeness, rank


criteria = ['x1', 'x2', 'x3', 'x4', 'x5']
criteria_type = ['cost', 'benefit', 'benefit', 'cost', 'benefit']
weight = [0.2, 0.15, 0.3, 0.25, 0.1]

decision_matrix = [
    [420, 75, 3, 1, 3],
    [580, 220, 2, 3, 2],
    [350, 80, 4, 2, 1],
    [410, 170, 3, 4, 2]
]

relative_closeness, rank = topsis(weight, decision_matrix, criteria_type)

print(relative_closeness)
print("\n")
print(rank)
