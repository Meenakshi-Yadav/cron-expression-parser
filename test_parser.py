from parser import simplify_field, parse_exp

"""
    Running basic assertions across field patterns and parser output.
"""
def test_simplify_field():
    # Field simplification logic
    assert simplify_field("5", 0, 59) == [5]
    assert simplify_field("*", 0, 5) == [0, 1, 2, 3, 4, 5]
    assert simplify_field("1-3", 0, 59) == [1, 2, 3]
    assert simplify_field("*/15", 0, 59) == [0, 15, 30, 45]
    assert simplify_field("1,2,3", 0, 59) == [1, 2, 3]

def test_parse_exp():
    # Full cron expression string parsing
    parsed = parse_exp("*/15 0 1,15 * 1 /usr/bin/find")
    assert parsed["minute"] == [0, 15, 30, 45]
    assert parsed["hour"] == [0]
    assert parsed["day of month"] == [1, 15]
    assert parsed["month"] == list(range(1, 13))
    assert parsed["day of week"] == [1]
    assert parsed["command"] == "/usr/bin/find"

if __name__ == "__main__":
    test_simplify_field()
    test_parse_exp()
    print("All tests passed.")

