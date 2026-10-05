---
type: concept
tags: [trading, research, finance, ai]
status: research
updated: 2026-10-05
---

# Day trading and AI-assisted trading (research, Oct 2026)

Hunter wants to explore day trading, including AI-assisted trading. This page is general education, not personal financial advice: Claude isn't a licensed adviser, and nothing here says what to buy or how much to risk.

## The odds (the most important part)
- **Taiwan:** Barber et al.'s 2019 study found most day traders lost money. In a typical six-month period more than 8 in 10 lost, and under 1% were predictably profitable after costs. ([UMich summary](https://sites.lsa.umich.edu/mje/2026/05/11/clicks-to-cash-debunking-the-myth-of-day-trading-profitability/), [CXO](https://www.cxoadvisory.com/individual-investing/do-day-traders-make-money/))
- **Brazil:** Chague's study covered Brazilian futures day traders. Of those who kept going for 300+ days, **97% lost money**, and only 1.1% earned more than the minimum wage. ([UMich summary](https://sites.lsa.umich.edu/mje/2026/05/11/clicks-to-cash-debunking-the-myth-of-day-trading-profitability/))
- **Australia, CFDs:** CFDs are the leveraged product most AU "day trading" ads push. **68% of retail clients lost money in FY24**, A$458M in total including A$73M in fees. In 2017, 72% lost. ASIC has restricted CFD leverage since 2021. ([Finance Magnates on ASIC data](https://datalab.financemagnates.com/compliance-insights/half-of-australia-s-cfd-sector-broke-the-rules-now-asic-wants-its-money-back), [ASIC 2019 release](https://www.asic.gov.au/about-asic/news-centre/find-a-media-release/2019-releases/19-220mr-asic-proposes-ban-on-the-sale-of-binary-options-to-retail-clients-and-restrictions-on-the-sale-of-cfds))

The takeaway: treat it as a skill with a long, costly learning curve and a low success rate. It is not passive income.

## Rules and tax (Australia)
- **The ATO decides whether you're an "investor" or a "trader"** based on how often and how regularly you trade, how much, and how business-like your records are. ([ATO](https://www.ato.gov.au/individuals-and-families/investments-and-assets/capital-gains-tax/shares-and-similar-investments/share-investing-versus-share-trading))
  - **Investor:** capital gains tax applies, and losses can only offset capital gains.
  - **Trader:** profits are ordinary income, and losses and costs (data, software, home office) are deductible against other income.
- **Keep records of every trade from day one.** Talk to an accountant before deciding how to structure it.
- **US stocks:** the US$25,000 "pattern day trader" minimum was **removed**. The SEC approved this on 14 April 2026, effective 4 June 2026, and brokers have an 18-month phase-in. It's replaced by real-time intraday margin, so check your broker. ([QuantInsti](https://www.quantinsti.com/articles/finra-pdt-rule-removal-2026/), [E*TRADE](https://us.etrade.com/knowledge/library/margin/pattern-day-trading-rule-change))

## AI-assisted trading: what's real
**Legitimate tools** help with analysis. They don't guarantee profit:
| Tool | What it does | Price (approx) |
|---|---|---|
| TradingView | Charts, indicators, strategy backtesting (Pine Script); free plan | Free to US$60/mo |
| TrendSpider | Auto trendlines and patterns, no-code backtests, alert bots that can route orders | ~US$47–107/mo |
| Trade Ideas | Real-time AI scanner for US stocks (its "Holly" bots) | ~US$89–178/mo |
| ChatGPT / Claude | Explaining concepts, writing backtest code, reviewing your trade journal | Subscription |

Source: [stockbrokers.com](https://www.stockbrokers.com/review/tools/trendspider-vs-tradingview), [Liberated Stock Trader](https://www.liberatedstocktrader.com/ai-stock-trading/), [Dupple](https://dupple.com/learn/best-ai-trading-tools).

- **Where AI genuinely helps:**
  - backtesting an idea on years of data before risking money
  - scanning for setups
  - enforcing your own rules through alerts
  - keeping a trade journal and spotting your bad habits
- **Where it doesn't:** reliably predicting the next price move. A backtest that looks great often fails live because of overfitting, fees and slippage.

**Scams are a major risk.** ASIC says AI-powered investment scams cost Australians **A$45M+ in 2026**. It took down 19,400+ scam sites in FY26, including 7,051 fake trading platforms. Common signs:
- AI "trading bots" promising passive income
- deepfake celebrity endorsements
- polished fake platforms

([ASIC 26-063MR](https://www.asic.gov.au/about-asic/news-centre/find-a-media-release/2026-releases/26-063mr-asic-ramps-up-action-to-protect-consumers-from-ai-powered-online-investment-scams/)) Check every platform on ASIC's professional register and Moneysmart's investor alert list.

## A sensible way to start (general, not advice)
1. **Learn first.** Moneysmart (ASIC's free site) covers trading basics and risks.
2. **Paper trade for 2–3 months** on a demo account (TradingView paper trading, or your broker's demo), and journal every trade.
3. **Write rules before you trade:** entry, exit, a stop-loss, and a maximum loss per day.
4. **Backtest those rules** with AI help (TradingView, or Claude writing Python), then forward-test them on paper.
5. **Only then use money you can afford to lose completely,** with no leverage or CFDs while learning.
6. **Keep tax records** from the first trade and speak to an accountant.

Related: [[overview]]

- **Apple Note (2026-10-05):** "Day Trading – Step-by-Step Starter Guide" is the easy-read version of this page: a 7-step roadmap (learn → tools → plan → backtest → paper trade → small real money → tax), a glossary, AI prompts, a scam checklist and a journal template.

## What makes a market good to learn on (2026-10-05)
Beginners do best with liquid, tight-spread, well-known markets, focusing on one at a time. Stocks/ETFs or forex (without leverage) are the usual starting points; CFDs, futures, options, crypto and penny stocks are the riskiest choices. ([Macroption](https://www.macroption.com/what-to-trade-as-beginner/), [DayTrading.com](https://www.daytrading.com/markets), [SelfWealth on AU brokerage](https://www.selfwealth.com.au/blog/best-trading-account-for-beginners-australia))
- **Hours in AU time:** the ASX trades 10am–4pm; the US market is overnight, about 12:30am–7am AEDT in summer and 11:30pm–6am AEST in winter. Hunter shoots during the day, so the plan uses **swing trading** (daily candles, checked in the evening) rather than intraday trading.
- **Plan v1** is in Apple Notes as "My Trading Plan – v1 (PAPER TRADING ONLY)". It uses one setup (a pullback to the 20-day moving average in an uptrend above a rising 50-day), 1% risk on a $10k paper account, a 2R target, a 10-day time stop and a maximum of 3 open trades, plus criteria for moving to real money.
- **Aggressive variant (2026-10-05):** Hunter wants high risk. Apple Note "Trading Plan – AGGRESSIVE (Risk Pot)" sets a fixed pot that is never topped up, withdraws the starting stake at 2×, risks 3–5% per trade, has circuit breakers (−10% day, −20% week, 4-loss pause), and uses a momentum breakout setup in the first 1–2 hours. Leverage is only allowed after 2 months, at most 2×.
