# Name: Nicholas Slazinski
# Student ID: 4426 2981
# Email: nslazins@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT): I worked with Chatgpt and Google Gemini
# If you worked with generative AI also add a statement for how you used it.
# e.g.:I asked ChatGPT and Google Gemini to explain the instructions, outline the approach, and provide guidance on how to implement each method. I used the responses to understand the logic but wrote and adjusted the final code myself. Asked ChatGPT hints for debugging and suggesting the general structure of the code
# Did your use of GenAI on this assignment align with your goals and guidelines in 
#    your Gen AI contract? If not, why? Yes it did

import random
import io
from contextlib import redirect_stdout


class CouponDispenser:

    def __init__(self, coupon_cards):
        self.coupon_cards = coupon_cards
        self.customer_roster = []
        self.issued_indices = []
        

    def __str__(self):
        if not self.coupon_cards:
            return ""
        return "|".join(self.coupon_cards)

    def issue_coupon(self, name):
        # If no coupons exist
        if len(self.coupon_cards) == 0:
            return "The box is empty."

        # Check if customer already exists
        for i in range(len(self.customer_roster)):
            if self.customer_roster[i] == name:
                existing_index = self.issued_indices[i]
                return f"That name already has a coupon: {self.coupon_cards[existing_index]}"

        # New name: pick random coupon index
        idx = random.randrange(len(self.coupon_cards))
        self.customer_roster.append(name)
        self.issued_indices.append(idx)
        return self.coupon_cards[idx]

    def distribute_session(self):
        round_number = 1

        while True:
            prompt = f"Round {round_number} - Enter a name (or a comma-separated list), or type 'show' or 'exit': "
            user_input = input(prompt)

            # exit
            if user_input == "exit":
                print("Goodbye!")
                break

            # show
            elif user_input == "show":
                for i in range(len(self.customer_roster)):
                    name = self.customer_roster[i]
                    coupon = self.coupon_cards[self.issued_indices[i]]
                    print(f"{name}: {coupon}")

            # names
            else:
                pieces = user_input.split(",")
                for p in pieces:
                    stripped = p.strip()
                    if stripped == "":
                        continue
                    msg = self.issue_coupon(stripped)
                    print(msg)

            round_number += 1

    def tally_distribution(self):
        if len(self.issued_indices) == 0:
            print("Empty")
            return

        # Count occurrences of each coupon index
        for i in range(len(self.coupon_cards)):
            count = 0
            for idx in self.issued_indices:
                if idx == i:
                    count += 1
            print(f"{self.coupon_cards[i]} distribution count: {count}.")


def main():
    coupon_cards = [
        "10% off",
        "Free small coffee",
        "Buy 1 get 1 half off",
        "Free extra espresso shot",
    ]

    box = CouponDispenser(coupon_cards)
    box.distribute_session()
    box.tally_distribution()


# -----------------------
# Tests (unchanged)
# -----------------------

def _capture_session_output(box, inputs):
    stream = io.StringIO()
    it = iter(inputs)

    def fake_input(prompt=""):
        print(prompt, end="")
        try:
            return next(it)
        except StopIteration:
            return "exit"

    original_input = __builtins__.input
    try:
        __builtins__.input = fake_input
        with redirect_stdout(stream):
            box.distribute_session()
    finally:
        __builtins__.input = original_input
    return stream.getvalue()


def test():
    total, passed = 0, 0

    def check(condition, msg):
        nonlocal total, passed
        total += 1
        if condition:
            passed += 1
            print(f"[PASS] {msg}")
        else:
            print(f"[FAIL] {msg}")

    notes_base = ["A", "B", "C"]
    box = CouponDispenser(notes_base)
    try:
        check(hasattr(box, "coupon_cards") and hasattr(box, "customer_roster") and hasattr(box, "issued_indices"),
              "__init__: attributes exist")
        check(box.coupon_cards == notes_base, "__init__: coupon_cards assigned")
        check(isinstance(box.customer_roster, list) and box.customer_roster == [], "__init__: customer_roster empty list")
        check(isinstance(box.issued_indices, list) and box.issued_indices == [], "__init__: issued_indices empty list")
        check(len(box.customer_roster) == len(box.issued_indices), "__init__: invariant lengths align")
    except Exception as e:
        check(False, f"__init__: unexpected exception {e}")

    try:
        box_empty = CouponDispenser([])
        check(str(box_empty) == "", "__str__: empty list returns empty string")
        box_single = CouponDispenser(["Only"])
        check(str(box_single) == "Only", "__str__: single element returns itself")
        box_multi = CouponDispenser(["X", "Y", "Z"])
        check(str(box_multi) == "X|Y|Z", "__str__: multi elements joined by pipes")
        _ = str(box_multi)
        check(box_multi.coupon_cards == ["X", "Y", "Z"], "__str__: does not modify coupon_cards")
    except Exception as e:
        check(False, f"__str__: unexpected exception {e}")
