import math
import pdf2markov as p2m
import random

# load "true" Q and p of individual letters
q, letter_p, text = p2m.load_file("MCMC/Pride and Prejudice (Classics Edition).pdf")

# load scrambled
scrambled_file = open("MCMC/j_29.txt", "r")
scrambled = scrambled_file.read()
scrambled_file.close()


# hyper parameters
beta = 0.5
random_amount = 1  # what
permutation = list('abcdefghijklmnopqrstuvwxyz ')
# 'ohfyazsplnqmdbexc kiwvjtugr' for f (feynman lectures on computation)
# 'lnvtzmhawgosiujfxckqrbpdey ' for h (harry potter)
# ' rdkqhugsaxyeptbmwjlcfozivn' for j (finnegan's wake)


# start with a random permutation
random.shuffle(permutation)
permutation = ''.join(permutation)


# compute permutation on a text
def perm(sigma, amt=-1):
    data = ""
    if amt == -1:
        amt = len(scrambled)
    for j in range(amt):
        data += sigma[p2m.to_idx(scrambled[j])]
    return data


# compute E or -ln L for a permutation
def energy(sigma):
    permed_text = perm(sigma)
    likelihood = math.log(letter_p[p2m.to_idx(permed_text[0])])
    for j in range(1, len(scrambled)):
        likelihood += math.log(q[p2m.to_idx(permed_text[j-1])][p2m.to_idx(permed_text[j])])
    return - likelihood


# define a new random permutation given a current one
def new_perm():
    p = permutation
    for j in range(random_amount):
        a = random.randint(0, len(p) - 1)
        b = random.randint(0, len(p) - 2)
        if b >= a:
            b += 1
        p = list(p)
        p[a], p[b] = p[b], p[a]
        p = ''.join(p)
    return p


def run_mcmc(epochs):
    global permutation
    # loop
    for i in range(epochs):
        temp = new_perm()
        e_temp = energy(temp)
        e_perm = energy(permutation)
        e_delta = e_temp - e_perm
        if e_delta < 0 or random.uniform(0, 1) < math.exp((- beta) * e_delta):
            permutation = temp
            print(perm(permutation, 100))
        else:
            pass
        # print(e_temp)
        # print(e_perm)
        # print(e_delta)


# usually works after like 200 but just to be sure
run_mcmc(3000)
print(permutation)
print(perm(permutation))
# bias it
# consider move and decide whether to accept
# loop
