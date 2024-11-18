class RulePart:
    def __init__(this):
        this.alleles = {}
        this.genotype = {}

    def randomize(this):
        # For each key in alleles, choose a random value and insert it into genotype
        for key, values in this.alleles.items():
            this.genotype[key] = random.choice(values)

    def __str__(this):
        sb = ""
        for key, value in this.genotype.items():
            sb = sb + f"{key}: {value}\n"

        return sb