#lvl req test


xp_need = 6000
lvl = 1
xp_sum = 0
v1 = 8000
v2 = 16000
v3 = 30000
xp_var = 1.010

for i in range(1, 99):
    xp_sum += xp_need
    d1 = round(xp_sum / v1)
    d2 = round(xp_sum / v2)
    d3 = round(xp_sum / v3)
    print(f"Level: {lvl} | XP needed: {xp_need} | Total XP: {xp_sum} | Easy: {d1} | Medium: {d2} | Hard: {d3} | XP Var: {xp_var:.2f}")
    xp_need = int(xp_need * xp_var)
    lvl += 1
    xp_var += 0.001
    if xp_var >= 1.05:
        xp_var = 1.05
    