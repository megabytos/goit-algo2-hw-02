from typing import List, Dict


def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Finds the optimal way to cut the rod using memoization
    :param length: length of the rod
    :param prices: list of prices, where prices[i] is the price of the rod of length i+1
    :return:  Dict with maximum profit and list of cuts and numbers of cuts
    """
    memo = {}

    def dp(n):
        if n == 0:
            return 0, []
        if n in memo:
            return memo[n]

        max_profit = 0
        best_cuts = []
        for i in range(1, n + 1):
            if i <= len(prices):
                profit, cuts = dp(n - i)
                profit += prices[i - 1]
                if profit > max_profit:
                    max_profit = profit
                    best_cuts = cuts + [i]

        memo[n] = (max_profit, best_cuts)
        return memo[n]

    max_profit, cuts = dp(length)

    return {
        "max_profit": max_profit,
        "cuts": cuts,
        "number_of_cuts": len(cuts) - 1 if cuts else 0
    }


def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Finds the optimal way to cut the rod using tabulation
    :param length: length of the rod
    :param prices: list of prices, where prices[i] is the price of the rod of length i+1
    :return:  Dict with maximum profit and list of cuts and numbers of cuts
    """
    dp = [0] * (length + 1)
    cuts = [[] for _ in range(length + 1)]

    for n in range(1, length + 1):
        for i in range(1, n + 1):
            if i <= len(prices):
                profit = dp[n - i] + prices[i - 1]
                if dp[n] < profit:
                    dp[n] = profit
                    cuts[n] = cuts[n - i] + [i]

    return {
        "max_profit": dp[length],
        "cuts": cuts[length],
        "number_of_cuts": len(cuts[length]) - 1 if cuts[length] else 0
    }


def run_tests():
    test_cases = [
        {
            "length": 5,
            "prices": [2, 5, 7, 8, 10],
            "name": "Base case"
        },
        {
            "length": 3,
            "prices": [1, 3, 8],
            "name": "Not to cut"
        },
        {
            "length": 4,
            "prices": [3, 5, 6, 7],
            "name": "Uniform cuts"
        }
    ]

    for test in test_cases:
        print(f"\nTest: {test['name']} {'*' * 20}")
        print(f"Rod length: {test['length']}")
        print(f"Prices: {test['prices']}")

        memo_result = rod_cutting_memo(test['length'], test['prices'])
        print("\nMemoization result:")
        print(f"Maximum profit: {memo_result['max_profit']}")
        print(f"Cuts: {memo_result['cuts']}")
        print(f"Number of cuts: {memo_result['number_of_cuts']}")

        table_result = rod_cutting_table(test['length'], test['prices'])
        print("\nTabulation result:")
        print(f"Maximum profit: {table_result['max_profit']}")
        print(f"Cuts: {table_result['cuts']}")
        print(f"Number of cuts: {table_result['number_of_cuts']}")


if __name__ == "__main__":
    run_tests()
