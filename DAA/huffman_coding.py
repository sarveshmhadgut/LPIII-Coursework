import heapq
from collections import Counter


class Node:
    def __init__(self, char="", freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, node):
        return self.freq < node.freq

    def is_leaf(self):
        return not self.left and not self.right


class HuffmanEncoder:
    def __init__(self):
        self.root = None
        self.codes = {}
        self.reversed_codes = {}

    def _build_freq_table(self, text):
        frequency = dict(Counter(text))
        return frequency

    def _build_huffman_tree(self, frequency):
        if not frequency:
            return None
        if len(frequency) == 1:
            char = list(frequency.keys())[0]
            return Node(char, freq=frequency[char])

        heap = []

        for c, f in frequency.items():
            heapq.heappush(heap, Node(c, f))

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)

            merged = Node(freq=left.freq + right.freq, left=left, right=right)
            heapq.heappush(heap, merged)

        return heap[0]

    def _generate_codes(self, root):
        if not root:
            return
        if root.is_leaf():
            return {root.char: "0"}

        codes: dict = {}

        def dfs(node, code):
            if node.is_leaf():
                codes[node.char] = code
                return

            if node.left:
                dfs(node.left, code + "0")

            if node.right:
                dfs(node.right, code + "1")

        dfs(root, "")
        return codes

    def encode(self, text):
        if not text:
            return ""

        frequency = self._build_freq_table(text=text)
        self.root = self._build_huffman_tree(frequency=frequency)

        self.codes = self._generate_codes(root=self.root)
        self.reversed_codes = {code: char for char, code in self.codes.items()}

        encoded_text = "".join(self.codes[char] for char in text)

        return encoded_text, self.codes, frequency

    def decode(self, encoded_text):
        if not encoded_text:
            return ""

        if self.root.is_leaf():
            return self.root.char * len(encoded_text)

        decoded_text = []
        current = self.root

        for bit in encoded_text:
            if bit == "0":
                current = current.left
            else:
                current = current.right

            if current.is_leaf():
                decoded_text.append(current.char)
                current = self.root

        return "".join(decoded_text)

    def print_tree(self, codes):
        if not self.root:
            print("Tree is empty")
            return

        self._print_helper(self.root, " ", codes)

    def _print_helper(self, node, indent, codes):
        if node is None:
            return
        if node == self.root:
            print("\n  Root\n    |")
        elif node.is_leaf():
            print(f"  ({node.char}, {codes[node.char]})")
        else:
            print("")

        if node.left or node.right:
            new_indent = indent + "   "
            if node.right:
                print(f"{new_indent}R:", end="")
                self._print_helper(node.right, new_indent, codes)
            if node.left:
                print(f"{new_indent}L:", end="")
                self._print_helper(node.left, new_indent, codes)

    def print_details(
        self,
        text,
        codes,
        frequency,
        encoded_text,
        decoded_text,
    ):
        print(f"\n{'Original Text':>20} : {text}")

        print("\n\tChar\tFrequency\tCode")
        for char in codes:
            print(f"\t{char:^6}\t{frequency[char]:^9}\t{codes[char]:<9}")

        print(
            f"\n{'Encoded Text':>20} : {encoded_text}\n{'Decoded Text':>20} : {decoded_text}\n{'Compression ratio':>20} = {len(text) * 8} / {len(encoded_text)} = {round(len(text) * 8 / len(encoded_text), 2)}"
        )


def main():
    text = "ABRACADABRAMISSISSIPPIBANANAA"
    huffman = HuffmanEncoder()
    encoded_text, codes, frequency = huffman.encode(text=text)

    decoded_text = huffman.decode(encoded_text=encoded_text)
    huffman.print_details(
        text=text,
        codes=codes,
        frequency=frequency,
        encoded_text=encoded_text,
        decoded_text=decoded_text,
    )
    huffman.print_tree(codes)


if __name__ == "__main__":
    main()
