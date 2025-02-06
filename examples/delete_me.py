from euchre.bots.tools.denormalize import denormalize

# ["♠", "♥", "♣", "♦"]

x = denormalize(["10♠"], "♥")
print(x)