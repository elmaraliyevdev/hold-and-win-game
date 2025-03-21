import sys
from main import Game

class TestableGame(Game):
    """Extended Game class that allows injecting custom random values for testing"""
    
    def __init__(self, custom_random_values=None):
        super().__init__()
        # If custom values provided, replace the random source
        if custom_random_values:
            self.src = custom_random_values
            self.src_index = 0
        
        # Add tracking for random calls to help QA understand what values are used
        self.random_calls = []
    
    def get_next_random(self):
        """Override to track random calls"""
        value = super().get_next_random()
        
        # Record information about this random call for debugging
        call_info = {
            "state": self.current_state,
            "index": self.src_index - 1,
            "value": value
        }
        self.random_calls.append(call_info)
        
        return value
    
    def print_random_usage(self):
        """Print how random values were used during the test"""
        print("\n=== RANDOM VALUE USAGE ===")
        for i, call in enumerate(self.random_calls):
            print(f"Call {i+1}: State '{call['state']}', Index {call['index']}, Value {call['value']}")


def run_test_scenario(name, random_values, num_spins=1, verbose=True):
    """Run a test scenario with custom random values"""
    if verbose:
        print(f"\n=== RUNNING TEST SCENARIO: {name} ===")
    
    # Create testable game with custom random values
    game = TestableGame(custom_random_values=random_values)
    
    # Run the game
    game.run(num_spins=num_spins)
    
    # Print random value usage if verbose
    if verbose:
        game.print_random_usage()
        
        print("\n=== TEST RESULTS ===")
        print(f"Final balance: {game.cur['balance']}")
        if 'bonus_simbols' in game.cur:
            print(f"Bonus symbols: {game.cur['bonus_simbols']}")
            print(f"Bonus win: {game.cur['bonus_total_win']}")
        else:
            print("No bonus game triggered in this test")
    
    # Return final game state for verification
    return game.cur


# Example test scenarios
def test_bonus_no_symbols():
    """Test scenario: Bonus game with no symbols collected"""
    # Values needed:
    # - First value 5: Triggers bonus (below 15)
    # - Next three values 75, 75, 75: No new symbols (above 50)
    return run_test_scenario(
        "Bonus Game with No Symbols",
        random_values=[5, 75, 75, 75],
        num_spins=1
    )

def test_bonus_with_3_symbols():
    """Test scenario: Bonus game with 3 symbols collected"""
    # Values needed:
    # - First value 5: Triggers bonus (below 15)
    # - Next values 25, 25, 25: New symbols appear (below 50)
    # - Next values 1, 5, 9: Symbol values (modulo 10 + 1 = 2, 6, 10)
    # - Last values 75, 75, 75: No new symbols to end bonus
    return run_test_scenario(
        "Bonus Game with 3 Symbols",
        random_values=[5, 25, 1, 25, 5, 25, 9, 75, 75, 75],
        num_spins=1
    )

def test_regular_small_win():
    """Test scenario: Regular spin with small win"""
    # Values needed:
    # - First value 20: No bonus (above 15)
    # - Second value 30: Small win category (below 40)
    # - Third value 1: Win amount calculation (modulo 3 + 1 = 2)
    return run_test_scenario(
        "Regular Spin with Small Win",
        random_values=[20, 30, 1],
        num_spins=1
    )

def test_regular_medium_win():
    """Test scenario: Regular spin with medium win"""
    # Values needed:
    # - First value 20: No bonus (above 15)
    # - Second value 50: Medium win category (between 40-70)
    # - Third value 1: Win amount calculation (modulo 2 + 3 = 4)
    return run_test_scenario(
        "Regular Spin with Medium Win",
        random_values=[20, 50, 1],
        num_spins=1
    )

def test_no_win():
    """Test scenario: Regular spin with no win"""
    # Values needed:
    # - First value 20: No bonus (above 15)
    # - Second value 80: No win category (above 70)
    return run_test_scenario(
        "Regular Spin with No Win",
        random_values=[20, 80],
        num_spins=1
    )

def test_multiple_spins():
    """Test multiple spins with mixed outcomes"""
    # Generate a longer sequence for multiple spins
    random_values = [
        # Spin 1: No bonus, medium win
        20, 50, 1,
        # Spin 2: Bonus with 2 symbols
        5, 25, 3, 25, 7, 75, 75, 75,
        # Spin 3: No bonus, small win
        20, 30, 2
    ]
    
    return run_test_scenario(
        "Multiple Spins with Mixed Outcomes",
        random_values=random_values,
        num_spins=3
    )


def print_help():
    """Print usage information"""
    print("Hold&Win Game Testing Utility")
    print("Usage: python test_holdwin.py [test_name]")
    print("\nAvailable tests:")
    print("  bonus_no_symbols    - Test bonus game with no symbols")
    print("  bonus_with_3        - Test bonus game with 3 symbols")
    print("  small_win           - Test regular spin with small win")
    print("  medium_win          - Test regular spin with medium win")
    print("  no_win              - Test regular spin with no win")
    print("  multiple            - Test multiple spins with mixed outcomes")
    print("  all                 - Run all test scenarios")
    print("  help                - Show this help message")


# Main function to run tests
def main():
    # Map command line arguments to test functions
    test_map = {
        "bonus_no_symbols": test_bonus_no_symbols,
        "bonus_with_3": test_bonus_with_3_symbols,
        "small_win": test_regular_small_win,
        "medium_win": test_regular_medium_win, 
        "no_win": test_no_win,
        "multiple": test_multiple_spins,
        "help": print_help
    }
    
    # Get command line argument if provided
    if len(sys.argv) > 1:
        test_name = sys.argv[1].lower()
        
        if test_name == "all":
            # Run all tests
            for name, test_func in test_map.items():
                if name != "help":
                    test_func()
        elif test_name in test_map:
            # Run specific test
            test_map[test_name]()
        else:
            print(f"Unknown test: {test_name}")
            print_help()
    else:
        # No argument provided, show help
        print_help()


if __name__ == "__main__":
    main()