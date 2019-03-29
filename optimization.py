import math
import random


def gradient_descent(x, y, alpha, tolerance, iterations):
    it = 0
    m = len(x)
    if m != len(y):
        return
    n = len(x[0])
    theta = []
    for i in range(n):
        theta.append(random.randrange(0, 1))

    costs_i = []

    while it < iterations:
        costs = []
        previous_theta = []
        for i in range(len(theta)):
            previous_theta.append(theta[i])

        update_cost(theta, costs, m, n, x, y)

        for j in range(n):
            theta_temp = 0

            for i in range(m):
                theta_temp = theta_temp + costs[i] * x[i][j]

            theta[j] = theta[j] - (alpha / m) * theta_temp

            update_cost(theta, costs, m, n, x, y)

        c = 0.0
        for i in range(len(costs)):
            c = c + (costs[i] * costs[i])

        c = (1.0 / (2.0 * m)) * c

        costs_i.append(0.0)
        costs_i[it] = c

        stop = False

        if it > 0:
            stop = math.fabs(costs_i[it] - costs_i[it - 1]) <= tolerance

        if stop:
            break
        it = it + 1

    str_theta = ""

    for i in range(len(theta)):
        str_theta += "theta" + repr(i) + "="
        str_theta += repr(theta[i])
        if i < len(theta) - 1:
            str_theta += ','

    return costs_i


def update_cost(thetas, costs, m, n, x, y):
    for i in range(m):
        cost_n = 0
        for j in range(n):
            cost_n = cost_n + thetas[j] * x[i][j]
        cost_n = cost_n - y[i][0]
        costs.append(cost_n)
