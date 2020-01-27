"""
Scoring
=======

Classes and functions for manipulating (aggregating, analyzing, reducing) robot competition scores.
"""


class BinaryCategoryAggregator(object):
    """
    A *binary* category is a scoring category in which the values are yes/no, true/false, or 1/0.  For a given
    category, a *truthy* result (yes, true, 1) typically results in some positive point score for the participant,
    whereas a false-like result is awarded zero points.
    
    We want to be able to compare three results -- our own and that of two potential teammates -- to determine if the
    three are commplementary in their scores.  Ideally, only one of the three will have scorred *truthily*, and the 
    weight applied to the point value will be 1.  If, however, two of the participants scored truthily, there is
    redundandcy, a lack of complement. So, we want to score this lower.   If all three score truthily, it means the
    other two are  able to do the same task as our own robot and there is no complement at all.  The weight is
    thus zero, eliminating points for this from the ovarall score being built.
    
    """
    
    # NNote that a redundancy between "me" and one other is worth less than redundancy between the two others.
    weights = { 
                0: {
                        0: {
                                0: 0,
                                1: 1,
                            },
                        1: {
                                0: 1,
                                1: 0.5,
                            },
                    },
                1: {
                        0: {
                                0: 1,
                                1: 0.25,
                            },
                        1: {
                                0: 0.25,
                                1: 0
                            },
                    }
                }
                
    trans = {
        0: 0, 'no': 0, 'false': 0, False: 0,
        1: 1, 'yes': 1, 'true': 1, True: 1    
    }
    
    def __init__(self, point_value=1):
                    
        self.pv = point_value
        
    def __call__(self, me, o1, o2):
        
        return self.weights[self.trans[me]][self.trans[o1]][self.trans[o2]] * self.pv
        
                    