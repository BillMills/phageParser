from restapi.models import Organism, Spacer, Repeat, OrganismSpacerRepeatPair

class CRISPRSequence(object):
    """Turns a accession number into an object containing the sequences, in order,
    of the spacers and repeats
    """

    def __init__(self, acc):
        self.accession_id = acc
        self.organism = Organism.objects.get(accession=self.accession_id)
        self.pairs = OrganismSpacerRepeatPair.objects.filter(organism_id=self.organism.id).order_by('order')

    def pair_sequence(self, pair):
        spacer_seq = self.get_spacer_sequence(pair.spacer)
        repeat_seq = self.get_repeat_sequence(pair.repeat)
        return {'spacer': spacer_seq, 'repeat': repeat_seq }

    def get_spacer_sequence(self, spacer):
        spacer = Spacer.objects.get(id=spacer.id)
        return spacer.sequence

    def get_repeat_sequence(self, repeat):
        repeat = Repeat.objects.get(id=repeat.id)
        return repeat.sequence

    def sequences(self):
        seq = {'spacers': [], 'repeats': []}
        for pair in self.pairs:
            seq['repeats'].append(self.pair_sequence(pair)['repeat'])
            seq['spacers'].append(self.pair_sequence(pair)['spacer'])
        return seq

