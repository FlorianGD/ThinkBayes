"""This file contains code for use with "Think Bayes",
by Allen B. Downey, available from greenteapress.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

from thinkbayes import Pmf

class Bowl():
    """
    Bowl object with number of vanilla and chocolate cookies
    """

    def __init__(self, vanilla, chocolate, prior):
        '''
        Initialize self

        vanilla: int, number of vanilla cookies
        chocolate: int, number of chocolate cookies
        prior: float, probability of chosing this bowl
        '''
        self.vanilla=vanilla
        self.chocolate=chocolate
        self.prior=prior

    def Update(self, type, quantity, prior):
        '''
        Remove quantity from type, and set new prior
        type: string (either 'vanilla' or 'chocolate')
        quantity: int
        prior: float
        '''
        new_value = getattr(self, type) - quantity
        setattr(self, type, new_value)
        self.prior = prior

    def GetTotal(self):
        return self.vanilla + self.chocolate

    def copy(self):
        ''' Return a copy of a bowl
        '''
        return Bowl(self.vanilla, self.chocolate, self.prior)

class Cookie(Pmf):
    """A map from string bowl ID to priorablity."""

    def __init__(self, hypos):
        """Initialize self.

        hypos: sequence of string bowl IDs
        """
        Pmf.__init__(self)
        for hypo in hypos:
            self.Set(hypo, 1)
        self.Normalize()

    def Update(self, data):
        """Updates the PMF with new data.

        data: string cookie type
        """
        for hypo in self.Values():
            like = self.Likelihood(data, hypo)
            self.Mult(hypo, like)
        self.Normalize()

    mixes_bowl = {
        'Bowl 1':Bowl(vanilla=30, chocolate=10, prior=0.5),
        'Bowl 2':Bowl(vanilla=20, chocolate=20, prior=0.5)
        }

    mixes = {
        'Bowl 1':dict(vanilla=0.75, chocolate=0.25),
        'Bowl 2':dict(vanilla=0.5, chocolate=0.5),
        }

    def Likelihood(self, data, hypo):
        """The likelihood of the data under the hypothesis.

        data: string cookie type
        hypo: string bowl ID
        """
        mix = self.mixes_bowl[hypo]
        total = mix.GetTotal()
        like = 1.0 * getattr(mix, data) / total * mix.prior
        return like

    def Likelihood2(self, data, hypo):
        """The likelihood of the data under the hypothesis.

        data: string cookie type
        hypo: string bowl ID
        """
        mix = self.mixes[hypo]
        like = mix[data]
        return like



def main():
    hypos = ['Bowl 1', 'Bowl 2']

    pmf = Cookie(hypos)

    #pmf.Update('vanilla')
    for cook in ['vanilla', 'vanilla', 'vanilla', 'vanilla', 'chocolate', 'chocolate']:
        pmf.Update(cook)
        print 'After ' + cook
        for hypo, prior in pmf.Items():
            print hypo, prior
            pmf.mixes_bowl[hypo].Update(cook, 1, prior)
        print '-------------------------'

    print 'State of the Bowls after everything: '
    print 'Bowl 1'
    print '      , vanilla ', pmf.mixes_bowl['Bowl 1'].vanilla
    print '      , chocolate ', pmf.mixes_bowl['Bowl 1'].chocolate
    print '      , prior ', pmf.mixes_bowl['Bowl 1'].prior
    print 'Bowl 2'
    print '      , vanilla ', pmf.mixes_bowl['Bowl 2'].vanilla
    print '      , chocolate ', pmf.mixes_bowl['Bowl 2'].chocolate
    print '      , prior ', pmf.mixes_bowl['Bowl 2'].prior

if __name__ == '__main__':
    main()
