import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("game_data.csv")

plt.figure()
plt.plot(df["time"], df["ball_speed"])
plt.title("Ball Speed Over Time")
plt.xlabel("Time")
plt.ylabel("Ball Speed")
plt.show()

plt.figure()
plt.plot(df["time"], df["score_diff"])
plt.title("Score Difference Over Time")
plt.xlabel("Time")
plt.ylabel("Score Difference")
plt.show()

plt.figure()
plt.hist(df["kicks"])
plt.title("Kick Frequency")
plt.xlabel("Kicks")
plt.ylabel("Frequency")
plt.show()

print("=== STATISTICS ===")
print("Mean Ball Speed:", df["ball_speed"].mean())
print("Max Ball Speed:", df["ball_speed"].max())
print("Min Ball Speed:", df["ball_speed"].min())
print("Total Kicks:", df["kicks"].sum())
print("Total Jumps:", df["jumps"].sum())