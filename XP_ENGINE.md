# StudyStack XP Engine

StudyStack calculates user XP from multiple coding and development platforms using a weighted scoring model. Each platform contributes XP based on measurable activity.

Only officially supported platforms are included below.

---

## Supported Platforms

### GitHub
XP = (repositories × 15) + (contributions × 5)

Measures:
- Public repositories
- Contribution calendar commits

---

### LeetCode
XP = (problems_solved × 10) + ((rating − 1300)² / 10) + (contests × 50)

Measures:
- Total solved problems
- Contest rating
- Contest participation

---

### GeeksforGeeks (GFG)
XP = (original_score × 10) + (problems_solved × 5)

Measures:
- Platform score
- Problems solved

---

### CodeChef
XP = (problems × 2) + ((rating − 1200)² / 10) + (contests × 50)

Measures:
- Problems solved
- Rating
- Contest participation

---

### HackerRank
XP = direct platform score

---

## Total XP

Total XP is calculated as:

Total XP = Sum of XP from all supported platforms

---

## Notes

- XP is recalculated on each sync
- Stored per-user in UserStats
- Used for dashboards, streaks, and leaderboard ranking
