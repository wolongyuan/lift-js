labels = {}


def add(label, addr):
    labels[label] = addr


def query(label):
    return labels[label]