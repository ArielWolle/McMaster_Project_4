def problem1(principle, interest_rate, future_value):
    future_value_time = 1
    while principle <= future_value:
        principle = principle * (1 + interest_rate) ** 1
        print("Year: ", future_value_time, " Value:", round(principle, 2))
        future_value_time += 1
    return future_value_time - 1


def problem2(num):
    primes = []
    isPrime = True
    for i in range(2, num + 1):
        for j in range(2, i):
            if i % j == 0:
                isPrime = False
                break
        if isPrime:
            primes.append(i)
        isPrime = True
    return primes
