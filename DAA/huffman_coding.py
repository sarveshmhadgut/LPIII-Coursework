import heapq
from typing import Any
from collections import Counter


class Node:
    def __init__(
        self, char: str = "", freq: int = 0, left: "Node" = None, right: "Node" = None
    ):
        self.char: str = char
        self.freq: int = freq
        self.left: "Node" = left
        self.right: "Node" = right

    def __lt__(self, node: "Node") -> bool:
        return self.freq < node.freq

    def is_leaf(self) -> bool:
        return not self.left and not self.right


class HuffmanEncoder:
    def __init__(self):
        self.root: Node = None
        self.codes: dict = {}
        self.reversed_codes: dict = {}

    def _build_freq_table(self, text: str) -> dict:
        frequency = dict(Counter(text))
        return frequency

    def _build_huffman_tree(self, frequency: dict) -> Node:
        if not frequency:
            return None

        if len(frequency) == 1:
            char: str = list(frequency.keys())[0]
            return Node(char, freq=frequency[char])

        heap: list = []

        for c, f in frequency.items():
            heapq.heappush(heap, Node(c, f))

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)

            merged = Node(freq=left.freq + right.freq, left=left, right=right)
            heapq.heappush(heap, merged)

        return heap[0]

    def _generate_codes(self, root: Node) -> dict:
        if not root:
            return

        codes: dict = {}

        if root.is_leaf():
            codes[root.char] = "0"
            return codes

        def dfs(node: Node, code: Node):
            if node.is_leaf():
                codes[node.char] = code
                return

            if node.left:
                dfs(node.left, code + "0")

            if node.right:
                dfs(node.right, code + "1")

        dfs(root, "")
        return codes

    def encode(self, text: str) -> Any:
        frequency: Counter = self._build_freq_table(text=text)
        self.root: Node = self._build_huffman_tree(frequency=frequency)

        self.codes: dict = self._generate_codes(root=self.root)
        self.reversed_codes: dict = {code: char for char, code in self.codes.items()}

        encoded_text: str = "".join(self.codes[char] for char in text)

        return encoded_text, self.codes, frequency

    def decode(self, encoded_text: str) -> str:
        if not encoded_text:
            return ""

        if self.root.is_leaf():
            return self.root.char * len(encoded_text)

        decoded_text: list = []
        current: Node = self.root

        for bit in encoded_text:
            if bit == "0":
                current = current.left

            else:
                current = current.right

            if current.is_leaf():
                decoded_text.append(current.char)
                current = self.root

        return "".join(decoded_text)

    def print_details(
        self,
        text: str,
        codes: dict,
        frequency: dict,
        encoded_text: str,
        decoded_text: str,
    ):
        print(f"Original Text: {text}")

        print("\nCharacter\tFrequency\tCode")
        for char in codes:
            print(f"{char:^9}\t{frequency[char]:^9}\t{codes[char]:<4}")

        print(f"\n     Encoded Text: {encoded_text}")
        print(f"     Decoded Text: {decoded_text}")
        print(
            f"Compression ratio: {len(encoded_text)} / {len(text) * 8} = {round(len(encoded_text) / len(text) * 8, 2)}"
        )


def main():
    text: str = "BRACADABRAMISSISSIPPIBANANAA"
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


if __name__ == "__main__":
    main()
