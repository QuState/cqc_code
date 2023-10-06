random.seed(123456789) (1)

probs = [random.random() for _ in range(4)] (2)
total = sum(probs)
probs = [p/total for p in probs] (3)

angles = [random.uniform(0, 2*pi) for _ in range(4)] (4)

state = [sqrt(p)*(cos(a) + 1j*sin(a)) for (p, a) in zip(probs, angles)] (5)