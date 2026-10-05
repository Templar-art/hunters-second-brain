#!/usr/bin/env python3
"""Build Hunter's trade journal workbook (Excel; opens in Numbers and Google Sheets too).

Sheets: Start Here, Settings, Trades (log), Dashboard (auto stats + equity curve), Size Calculator.
Every stat is a live formula, so it updates as trades are logged. Three example trades are included; delete them.
Usage: python3 projects/trading/build_journal.py  -> projects/trading/Trade-Journal.xlsx
"""
import os
from openpyxl import Workbook
from openpyxl.chart import LineChart, Reference
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Trade-Journal.xlsx")
N = 500                      # trade rows with formulas ready
INK, MUTE, LINE = "111111", "6B6B6B", "D9D9D9"
HEAD = PatternFill("solid", fgColor="111111")
INPUT = PatternFill("solid", fgColor="FFF7D6")     # yellow = you type here
CALC = PatternFill("solid", fgColor="F3F3F3")      # grey = automatic
GOOD = PatternFill("solid", fgColor="DDF3E4")
BAD = PatternFill("solid", fgColor="FBE0DE")
thin = Side(style="thin", color=LINE)
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
H = Font(bold=True, color="FFFFFF")
TITLE = Font(bold=True, size=18)

wb = Workbook()

# ---------------------------------------------------------------- Start Here
s = wb.active
s.title = "Start Here"
s.column_dimensions["A"].width = 110
lines = [
    ("TRADE JOURNAL: HOW TO USE", TITLE),
    ("General education tool, not financial advice.", Font(italic=True, color=MUTE)),
    ("", None),
    ("1. SETTINGS tab: type your starting balance (paper or real), risk % per trade and your circuit-breaker limits. Yellow cells = you type.", None),
    ("2. Before a trade: use the SIZE CALCULATOR tab to work out how many shares/contracts so you only lose your planned $ if the stop is hit.", None),
    ("3. After a trade closes: add ONE row in the TRADES tab. Fill the yellow columns only. Grey columns calculate themselves.", None),
    ("    • Direction: Long (you bought, want price up) or Short (want price down).", None),
    ("    • Qty: number of shares. For OPTIONS, put contracts × 100 (one contract = 100 shares) and use the option prices for entry/stop/exit.", None),
    ("    • Stop = where you planned to get out if wrong. This sets your risk (1R).", None),
    ("    • Fees = brokerage + FX fees for that trade, round trip.", None),
    ("    • Followed rules? Be honest. This is the most useful column in the whole journal.", None),
    ("4. DASHBOARD tab: win rate, average win/loss, EXPECTANCY (your average $ per trade), profit factor, drawdown and the equity curve.", None),
    ("    • Expectancy > 0 after 50+ trades = you probably have an edge (skill). < 0 = it isn't working yet, so fix it or go back to paper.", None),
    ("    • Profit factor > 1.5 is solid, > 2 is excellent, < 1 is losing.", None),
    ("    • Circuit breakers turn RED when you hit your daily/weekly loss limit: stop trading.", None),
    ("5. Every Sunday: copy the week's rows into Claude and ask 'what patterns do you see?'", None),
    ("", None),
    ("The 3 example trades in TRADES are there so you can see it working. Delete those rows before you start.", Font(bold=True)),
]
for i, (t, f) in enumerate(lines, 1):
    c = s.cell(row=i, column=1, value=t)
    c.alignment = Alignment(wrap_text=True, vertical="top")
    if f:
        c.font = f

# ---------------------------------------------------------------- Settings
st = wb.create_sheet("Settings")
st.column_dimensions["A"].width = 38
st.column_dimensions["B"].width = 16
st.column_dimensions["C"].width = 60
rows = [
    ("Starting balance ($)", 10000, "Paper: match what you'd really use. Aggressive pot: your fixed pot."),
    ("Risk per trade (%)", 0.01, "Slow plan 1%. Aggressive plan 3–5%."),
    ("Daily loss limit (%)", 0.10, "Stop for the day when down this much of the starting balance."),
    ("Weekly loss limit (%)", 0.20, "Stop for the week when down this much."),
    ("Losing streak pause (trades)", 4, "Take 48h off after this many losses in a row."),
]
st["A1"], st["B1"], st["C1"] = "Setting", "Value", "What it means"
for c in ("A1", "B1", "C1"):
    st[c].font, st[c].fill = H, HEAD
for i, (a, b, c) in enumerate(rows, 2):
    st.cell(row=i, column=1, value=a)
    v = st.cell(row=i, column=2, value=b)
    v.fill, v.border = INPUT, BOX
    if isinstance(b, float) and b < 1:
        v.number_format = "0%"
    elif i == 2:
        v.number_format = '"$"#,##0'
    st.cell(row=i, column=3, value=c).font = Font(color=MUTE)
st["A9"] = "Setups you trade (used for dropdowns + breakdown)"
st["A9"].font = Font(bold=True)
for i, name in enumerate(["Pullback", "Momentum breakout", "Options - long call", "Options - debit spread", "Other"], 10):
    c = st.cell(row=i, column=1, value=name)
    c.fill, c.border = INPUT, BOX
START, RISK, DAYLIM, WEEKLIM, STREAK = "Settings!$B$2", "Settings!$B$3", "Settings!$B$4", "Settings!$B$5", "Settings!$B$6"

# ---------------------------------------------------------------- Trades
t = wb.create_sheet("Trades")
cols = [  # header, width, kind
    ("#", 5, "calc"), ("Date", 11, "in"), ("Ticker", 10, "in"), ("Market", 10, "in"), ("Direction", 10, "in"),
    ("Setup", 22, "in"), ("Entry $", 10, "in"), ("Stop $", 10, "in"), ("Target $", 10, "in"), ("Qty", 8, "in"),
    ("Exit $", 10, "in"), ("Fees $", 8, "in"), ("Followed rules?", 10, "in"), ("Emotion", 12, "in"), ("Notes", 34, "in"),
    ("Risk $ (1R)", 11, "calc"), ("P&L $", 11, "calc"), ("R multiple", 10, "calc"), ("Result", 8, "calc"),
    ("Balance $", 12, "calc"), ("Peak $", 12, "calc"), ("Drawdown %", 11, "calc"), ("Loss streak", 9, "calc"), ("Week", 8, "calc"),
]
for j, (name, w, kind) in enumerate(cols, 1):
    c = t.cell(row=1, column=j, value=name)
    c.font, c.fill = H, HEAD
    c.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")
    t.column_dimensions[c.column_letter].width = w
t.row_dimensions[1].height = 32
t.freeze_panes = "C2"

for r in range(2, N + 2):
    blank = f'$B{r}=""'
    f = {
        1: f'=IF({blank},"",ROW()-1)',
        16: f'=IF(OR({blank},G{r}="",H{r}="",J{r}=""),"",ABS(G{r}-H{r})*J{r})',
        17: f'=IF(OR({blank},K{r}=""),"",IF(E{r}="Short",G{r}-K{r},K{r}-G{r})*J{r}-N(L{r}))',
        18: f'=IF(OR(P{r}="",Q{r}="",P{r}=0),"",Q{r}/P{r})',
        19: f'=IF(Q{r}="","",IF(Q{r}>0,"Win",IF(Q{r}<0,"Loss","Flat")))',
        20: f'=IF(Q{r}="","",{START}+SUM($Q$2:Q{r}))',
        21: f'=IF(T{r}="","",MAX({START},MAX($T$2:T{r})))',
        22: f'=IF(T{r}="","",(T{r}-U{r})/U{r})',
        23: (f'=IF(S{r}="","",IF(S{r}="Loss",1,0))' if r == 2 else f'=IF(S{r}="","",IF(S{r}="Loss",N(W{r-1})+1,0))'),
        24: f'=IF({blank},"",YEAR(B{r})&"-W"&TEXT(WEEKNUM(B{r},2),"00"))',
    }
    for j, (name, w, kind) in enumerate(cols, 1):
        c = t.cell(row=r, column=j)
        c.border = BOX
        if kind == "in":
            c.fill = INPUT
        else:
            c.fill = CALC
            c.value = f[j]
        if j == 2:
            c.number_format = "dd/mm/yyyy"
        elif j in (7, 8, 9, 11, 12, 16, 17, 20, 21):
            c.number_format = '"$"#,##0.00'
        elif j == 18:
            c.number_format = '0.00"R"'
        elif j == 22:
            c.number_format = "0.0%"

examples = [  # date, ticker, market, dir, setup, entry, stop, target, qty, exit, fees, rules, emotion, notes
    ("2026-10-06", "EXAMPLE", "ASX", "Long", "Pullback", 50, 48, 54, 50, 54, 10, "Y", "Calm", "EXAMPLE: delete me. Hit 2R target."),
    ("2026-10-07", "EXAMPLE", "ASX", "Long", "Momentum breakout", 20, 19.5, 21, 200, 19.5, 10, "Y", "Calm", "EXAMPLE: delete me. Stopped out, -1R."),
    ("2026-10-08", "EXAMPLE", "US", "Long", "Options - long call", 2.10, 1.05, 4.20, 100, 1.60, 2, "N", "FOMO", "EXAMPLE: delete me. 1 contract, broke rules."),
]
import datetime
for i, e in enumerate(examples, 2):
    vals = list(e)
    vals[0] = datetime.date.fromisoformat(vals[0])
    for j, v in zip([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], vals):
        t.cell(row=i, column=j, value=v)

def dv(formula, rng):
    d = DataValidation(type="list", formula1=formula, allow_blank=True)
    t.add_data_validation(d)
    d.add(rng)

dv('"Long,Short"', f"E2:E{N+1}")
dv('"ASX,US,Forex,Crypto,Other"', f"D2:D{N+1}")
dv("=Settings!$A$10:$A$14", f"F2:F{N+1}")
dv('"Y,N"', f"M2:M{N+1}")
dv('"Calm,Confident,FOMO,Revenge,Bored,Tired,Anxious"', f"N2:N{N+1}")
t.conditional_formatting.add(f"Q2:Q{N+1}", CellIsRule(operator="greaterThan", formula=["0"], fill=GOOD))
t.conditional_formatting.add(f"Q2:Q{N+1}", CellIsRule(operator="lessThan", formula=["0"], fill=BAD))
t.conditional_formatting.add(f"M2:M{N+1}", CellIsRule(operator="equal", formula=['"N"'], fill=BAD))

# ---------------------------------------------------------------- Dashboard
d = wb.create_sheet("Dashboard", 1)
d.column_dimensions["A"].width = 34
d.column_dimensions["B"].width = 16
d.column_dimensions["C"].width = 54
d["A1"] = "DASHBOARD"
d["A1"].font = TITLE
d["A2"] = "Everything here updates automatically from the Trades tab."
d["A2"].font = Font(italic=True, color=MUTE)
R = f"Trades!$Q$2:$Q${N+1}"
RM = f"Trades!$R$2:$R${N+1}"
RES = f"Trades!$S$2:$S${N+1}"
stats = [
    ("Trades logged", f'=COUNT({R})', "0", ""),
    ("Wins", f'=COUNTIF({RES},"Win")', "0", ""),
    ("Losses", f'=COUNTIF({RES},"Loss")', "0", ""),
    ("Win rate", f'=IFERROR(B5/B4,0)', "0.0%", "How often you're right. Can be under 50% and still profitable."),
    ("Average win $", f'=IFERROR(AVERAGEIF({R},">0"),0)', '"$"#,##0.00', ""),
    ("Average loss $", f'=IFERROR(AVERAGEIF({R},"<0"),0)', '"$"#,##0.00', ""),
    ("Average R per trade", f'=IFERROR(AVERAGE({RM}),0)', '0.00"R"', "Average result in 'risk units'. Above 0 = good."),
    ("EXPECTANCY $ per trade", f'=IFERROR(B7*B8+(1-B7)*B9,0)', '"$"#,##0.00', "THE key number: what you make on an average trade after fees."),
    ("Profit factor", f'=IFERROR(SUMIF({R},">0")/ABS(SUMIF({R},"<0")),0)', "0.00", ">1.5 solid, >2 excellent, <1 losing."),
    ("Total P&L $", f'=SUM({R})', '"$"#,##0.00', ""),
    ("Current balance $", f'={START}+B13', '"$"#,##0.00', ""),
    ("Return on starting balance", f'=IFERROR(B13/{START},0)', "0.0%", ""),
    ("Max drawdown", f'=IFERROR(-MIN(Trades!$V$2:$V${N+1}),0)', "0.0%", "Biggest drop from a peak. 50% down needs +100% to recover."),
    ("Rules followed", f'=IFERROR(COUNTIF(Trades!$M$2:$M${N+1},"Y")/COUNTA(Trades!$M$2:$M${N+1}),0)', "0%", "Aim for 90%+."),
    ("Avg P&L when rules followed", f'=IFERROR(AVERAGEIF(Trades!$M$2:$M${N+1},"Y",{R}),0)', '"$"#,##0.00', ""),
    ("Avg P&L when rules broken", f'=IFERROR(AVERAGEIF(Trades!$M$2:$M${N+1},"N",{R}),0)', '"$"#,##0.00', "Usually the eye-opener."),
    ("Current losing streak", f'=IFERROR(INDEX(Trades!$W$2:$W${N+1},MATCH(9.9E+307,Trades!$W$2:$W${N+1})),0)', "0", ""),
]
d["A3"], d["B3"], d["C3"] = "Stat", "Value", "What it means"
for c in ("A3", "B3", "C3"):
    d[c].font, d[c].fill = H, HEAD
for i, (a, fml, fmt, note) in enumerate(stats, 4):
    d.cell(row=i, column=1, value=a)
    v = d.cell(row=i, column=2, value=fml)
    v.number_format, v.fill, v.border = fmt, CALC, BOX
    d.cell(row=i, column=3, value=note).font = Font(color=MUTE)
d["A11"].font = Font(bold=True)
d["B11"].font = Font(bold=True, size=13)
d.conditional_formatting.add("B11", CellIsRule(operator="greaterThan", formula=["0"], fill=GOOD))
d.conditional_formatting.add("B11", CellIsRule(operator="lessThan", formula=["0"], fill=BAD))

# circuit breakers
d["A23"] = "CIRCUIT BREAKERS"
d["A23"].font = Font(bold=True, size=13)
cb = [
    ("P&L today $", f'=SUMIF(Trades!$B$2:$B${N+1},TODAY(),{R})', '"$"#,##0.00'),
    ("Daily limit $", f'=-{START}*{DAYLIM}', '"$"#,##0.00'),
    ("TODAY", '=IF(B24<=B25,"STOP: daily limit hit","OK to trade")', "@"),
    ("P&L this week $", f'=SUMIF(Trades!$X$2:$X${N+1},YEAR(TODAY())&"-W"&TEXT(WEEKNUM(TODAY(),2),"00"),{R})', '"$"#,##0.00'),
    ("Weekly limit $", f'=-{START}*{WEEKLIM}', '"$"#,##0.00'),
    ("THIS WEEK", '=IF(B27<=B28,"STOP: weekly limit hit","OK to trade")', "@"),
    ("LOSING STREAK", f'=IF(B20>={STREAK},"PAUSE 48h: review journal","OK")', "@"),
]
for i, (a, fml, fmt) in enumerate(cb, 24):
    d.cell(row=i, column=1, value=a)
    v = d.cell(row=i, column=2, value=fml)
    v.number_format, v.fill, v.border = fmt, CALC, BOX
for cell in ("B26", "B29", "B30"):
    d.conditional_formatting.add(cell, FormulaRule(formula=[f'LEFT({cell},2)="OK"'], fill=GOOD))
    d.conditional_formatting.add(cell, FormulaRule(formula=[f'LEFT({cell},2)<>"OK"'], fill=BAD))

# by setup
d["A33"] = "BY SETUP"
d["A33"].font = Font(bold=True, size=13)
for j, h in enumerate(["Setup", "Trades", "Win rate", "Avg R", "Total P&L $"], 1):
    c = d.cell(row=34, column=j, value=h)
    c.font, c.fill = H, HEAD
d.column_dimensions["D"].width = 10
d.column_dimensions["E"].width = 14
SET = f"Trades!$F$2:$F${N+1}"
for k in range(5):
    r = 35 + k
    d.cell(row=r, column=1, value=f"=Settings!A{10+k}")
    d.cell(row=r, column=2, value=f'=COUNTIFS({SET},A{r},{RES},"<>")')
    d.cell(row=r, column=3, value=f'=IFERROR(COUNTIFS({SET},A{r},{RES},"Win")/B{r},0)').number_format = "0%"
    d.cell(row=r, column=4, value=f'=IFERROR(AVERAGEIF({SET},A{r},{RM}),0)').number_format = '0.00"R"'
    d.cell(row=r, column=5, value=f'=SUMIF({SET},A{r},{R})').number_format = '"$"#,##0.00'
    for j in range(1, 6):
        d.cell(row=r, column=j).border = BOX

ch = LineChart()
ch.title, ch.y_axis.title, ch.x_axis.title = "Equity curve", "Balance $", "Trade #"
ch.height, ch.width = 9, 18
ch.add_data(Reference(t, min_col=20, min_row=1, max_row=N + 1), titles_from_data=True)
ch.legend = None
d.add_chart(ch, "G3")

# ---------------------------------------------------------------- Size Calculator
z = wb.create_sheet("Size Calculator")
z.column_dimensions["A"].width = 36
z.column_dimensions["B"].width = 16
z.column_dimensions["C"].width = 56
z["A1"] = "POSITION SIZE CALCULATOR"
z["A1"].font = TITLE
z["A2"] = "Type the yellow cells before every trade. It tells you how big to go so a stop-out only costs your planned risk."
z["A2"].font = Font(italic=True, color=MUTE)
calc = [
    ("SHARES", None, None, None),
    ("Account balance $", "=Dashboard!B14", '"$"#,##0.00', "calc"),
    ("Risk per trade %", f"={RISK}", "0.0%", "calc"),
    ("$ you're willing to lose", "=B5*B6", '"$"#,##0.00', "calc"),
    ("Entry price $", 50, '"$"#,##0.00', "in"),
    ("Stop-loss price $", 48, '"$"#,##0.00', "in"),
    ("→ SHARES TO BUY", "=IFERROR(ROUNDDOWN(B7/ABS(B8-B9),0),0)", "#,##0", "calc"),
    ("→ Position value $", "=B10*B8", '"$"#,##0.00', "calc"),
    ("→ Target price (2R)", "=IF(B8>B9,B8+2*(B8-B9),B8-2*(B9-B8))", '"$"#,##0.00', "calc"),
    ("", None, None, None),
    ("OPTIONS (buying calls/puts)", None, None, None),
    ("Option price per share $ (premium)", 2.10, '"$"#,##0.00', "in"),
    ("Cost of 1 contract (×100) $", "=B15*100", '"$"#,##0.00', "calc"),
    ("→ CONTRACTS if the whole premium could go to $0", "=IFERROR(ROUNDDOWN(B7/B16,0),0)", "#,##0", "calc"),
    ("Your exit-if-wrong option price $", 1.05, '"$"#,##0.00', "in"),
    ("→ CONTRACTS using that stop", "=IFERROR(ROUNDDOWN(B7/((B15-B18)*100),0),0)", "#,##0", "calc"),
]
for i, (a, v, fmt, kind) in enumerate(calc, 4):
    ca = z.cell(row=i, column=1, value=a)
    if v is None:
        ca.font = Font(bold=True, size=13)
        continue
    cb_ = z.cell(row=i, column=2, value=v)
    cb_.number_format, cb_.border = fmt, BOX
    cb_.fill = INPUT if kind == "in" else CALC
    if a.startswith("→"):
        ca.font = Font(bold=True)
        cb_.font = Font(bold=True, size=13)
z["C17"] = "Safest for beginners: size so that even a 100% loss of the premium = your planned risk."
z["C17"].font = Font(color=MUTE)
z["C19"] = "0 = even ONE contract risks more than your limit. Pick a cheaper option, or skip it."
z["C19"].font = Font(color=MUTE)

wb.save(OUT)
print("saved", OUT)
