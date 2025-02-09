import durachok as d

def test_find_lowest_trump():
    # p1 = durachok.Player("p1"
    
    h1 = [
        d.Card(14, "diamonds"),
        d.Card(10, "hearts"),
        d.Card(6, "hearts"), 
        d.Card(13, "hearts"),
        d.Card(7, "spades"),
        d.Card(11, "clubs"),
    ]
    actual = d.find_lowest_trump(h1, "hearts")
    expected = 6

    print(f"Expected={expected}, actual={actual}")
    assert actual == expected

def run_unittests():
    print("Statring Unit tests!")
    test_find_lowest_trump()

if __name__ == "__main__":
    run_unittests()