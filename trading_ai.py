import pandas as pd

# Load market data (CSV file)
# Format: time,open,high,low,close,volume
data = pd.read_csv("market_data.csv")

# Create empty columns
data['signal'] = None
data['confidence'] = 0

for i in range(1, len(data)):
    
    prev_high = data['high'][i-1]
    prev_low = data['low'][i-1]
    close = data['close'][i]
    volume = data['volume'][i]
    prev_volume = data['volume'][i-1]

    confidence = 0

    # Breakout logic
    if close > prev_high:
        signal = "BUY"
        confidence += 40
    elif close < prev_low:
        signal = "SELL"
        confidence += 40
    else:
        signal = None

    # Volume confirmation
    if volume > prev_volume:
        confidence += 20

    # Simple trend confirmation (moving average)
    ma = data['close'][max(0, i-5):i].mean()
    if close > ma:
        confidence += 20

    # Save results
    data.at[i, 'signal'] = signal
    data.at[i, 'confidence'] = confidence

# Print signals
signals = data[data['signal'].notnull()]

for index, row in signals.iterrows():
    entry = row['close']
    
    if row['signal'] == "BUY":
        sl = entry - 30
        target = entry + 60
    else:
        sl = entry + 30
        target = entry - 60

    print("----- SIGNAL -----")
    print(f"Type: {row['signal']}")
    print(f"Entry: {entry}")
    print(f"Stop Loss: {sl}")
    print(f"Target: {target}")
    print(f"Confidence: {row['confidence']}%")
    print("------------------")