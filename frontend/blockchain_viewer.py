import matplotlib.pyplot as plt


def show_blockchain(chain):

    indices = []
    hashes = []

    for block in chain:
        indices.append(block["index"])
        hashes.append(block["hash"][:8])

    plt.figure(figsize=(8,4))

    plt.plot(indices, indices, marker="o")

    for i, h in enumerate(hashes):
        plt.text(indices[i], indices[i], h)

    plt.title("Blockchain Visualization")
    plt.xlabel("Block Index")
    plt.ylabel("Chain Progress")

    plt.show()