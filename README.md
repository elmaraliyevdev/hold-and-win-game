# Hold&Win Game Testing Framework

This testing framework allows QA to easily test specific scenarios in the Hold&Win game by controlling the random number sequences that determine game outcomes.

## Quick Start

1. Make sure both `main.py` and `test_holdwin.py` are in the same directory.

2. Run a test:
```bash
python test_holdwin.py bonus_with_3
```

3. Run all available tests:
```bash
python test_holdwin.py all
```

4. View available tests:
```bash
python test_holdwin.py help
```

## Available Tests

- `bonus_no_symbols` - Test a bonus game where no symbols are collected
- `bonus_with_3` - Test a bonus game with exactly 3 symbols collected
- `small_win` - Test a regular spin with a small win (1-3 coins)
- `medium_win` - Test a regular spin with a medium win (3-4 coins)
- `no_win` - Test a regular spin with no win
- `multiple` - Test multiple spins with different outcomes

## How It Works

The testing framework overrides the game's random number generation, replacing it with predetermined values that produce specific outcomes. This allows for deterministic, reproducible testing.

### Understanding Random Value Ranges

The game uses random values in different ways depending on the context:

1. **Spin State - Bonus Trigger Check**
   - Values < 15: Trigger bonus game
   - Values ≥ 15: Regular spin (no bonus)

2. **Spin State - Regular Win Check** (only used if bonus not triggered)
   - Values < 40: Small win (1-3 coins)
   - Values 40-69: Medium win (3-4 coins)
   - Values ≥ 70: No win

3. **Spin State - Win Amount Calculation**
   - For small wins: value % 3 + 1 (produces 1, 2, or 3)
   - For medium wins: value % 2 + 3 (produces 3 or 4)

4. **Bonus State - Symbol Check**
   - Values < 50: Add new symbol
   - Values ≥ 50: No new symbol (decrement rounds left)

5. **Bonus State - Symbol Value**
   - value % 10 + 1 (produces values from 1 to 10)

### Random Value Usage

When you run a test, the framework shows you how each random value was used:

```
=== RANDOM VALUE USAGE ===
Call 1: State 'spin', Index 0, Value 5  
Call 2: State 'bonus', Index 1, Value 75
Call 3: State 'bonus', Index 2, Value 75
Call 4: State 'bonus', Index 3, Value 75
```

This helps you understand what values are needed to produce specific outcomes.

## Creating Your Own Tests

You can create your own test scenarios by adding new functions to `test_holdwin.py`.

### Example:

```python
def test_my_custom_scenario():
    # Create a sequence of random values to control the game
    random_values = [
        # First value: 5 (below 15) triggers bonus
        5,
        # Next three values: 25, 25, 25 (below 50) add new symbols
        25, 25, 25,
        # Next three values: 0, 5, 9 determine symbol values
        # symbol value = value % 10 + 1, so these give 1, 6, 10
        0, 5, 9,
        # Last three values: 75, 75, 75 (above 50) end the bonus game
        75, 75, 75
    ]
    
    return run_test_scenario(
        "My Custom Bonus Scenario",
        random_values=random_values,
        num_spins=1
    )
```

Then add your test to the `test_map` in the `main()` function:

```python
test_map = {
    # ... existing tests ...
    "my_custom": test_my_custom_scenario,
}
```

Now you can run your test with:
```bash
python test_holdwin.py my_custom
```

## Testing Multiple Spins

For tests with multiple spins, make sure you provide enough random values to cover all spins and set the correct `num_spins` parameter:

```python
def test_three_spins():
    # Values for three spins
    random_values = [
        # Spin 1: values for first spin
        20, 30, 1,
        # Spin 2: values for second spin
        20, 50, 1,
        # Spin 3: values for third spin
        20, 80
    ]
    
    return run_test_scenario(
        "Three Regular Spins",
        random_values=random_values,
        num_spins=3  # Important: set correct number of spins
    )
```

## Troubleshooting

### Not Enough Random Values

If your test doesn't have enough random values, you'll see the game use the same values repeatedly. Make sure you provide enough values to cover all random decisions in your test.

### Unexpected Outcomes

If you're not seeing the expected outcomes:

1. Review the "RANDOM VALUE USAGE" output to see how values were used
2. Check the value ranges to ensure your values will produce the expected results
3. Add more values if the game is making more random decisions than you expected

## Advanced Usage

### Silent Mode

You can run tests in silent mode by setting `verbose=False`:

```python
run_test_scenario(
    "Silent Test",
    random_values=[5, 25, 1, 75, 75, 75],
    num_spins=1,
    verbose=False
)
```

### Programmatic Verification

All test functions return the final game state, so you can add verification logic:

```python
def test_with_verification():
    result = run_test_scenario(
        "Verified Test",
        random_values=[5, 25, 1, 75, 75, 75],
        num_spins=1
    )
    
    # Verify results
    assert len(result.get('bonus_simbols', [])) == 1, "Expected 1 bonus symbol"
    assert result.get('bonus_total_win') == 2, "Expected win of 2"
    
    print("All verifications passed!")
```

### Creating Random Value Sequences Programmatically

For complex tests, you can generate random values programmatically:

```python
def test_many_symbols():
    # Generate values for a bonus with many symbols
    random_values = [5]  # Trigger bonus
    
    # Add 10 symbols
    for i in range(10):
        random_values.append(25)  # Add symbol
        random_values.append(i)   # Symbol value
    
    # End bonus
    random_values.extend([75, 75, 75])
    
    return run_test_scenario(
        "Many Symbols Bonus",
        random_values=random_values,
        num_spins=1
    )
```