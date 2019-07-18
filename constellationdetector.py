class ConstellationDetector:
    consellations = []
    def __init__(self, consellations_array):
        consellations = consellations_array
    
    #Take magnitiude array of an image and returns the index of the largest stars
    def find_brightest_stars(self, mags):
        #mag values
        first_largest = 0
        second_largest = 0
        #index of brightest stars
        l1 = -1
        l2 = -1
        for i, mag in enumerate(mags):
            if(mag > first_largest):
                second_largest = first_largest
                l2 = l1
                first_largest = mag
                l1 = i
            elif(mag > second_largest):
                second_largest = mag
                l2 = i
        return l1, l2
