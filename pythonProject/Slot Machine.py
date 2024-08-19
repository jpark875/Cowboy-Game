import jackpot

average_total=0
for i in range(1000):
    average_total += jackpot.jackpot()
average_pulls=average_total/1000
print(average_pulls)