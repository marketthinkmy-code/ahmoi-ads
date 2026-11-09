# CLAUDE.md — MOI FU MONEY BLUEPRINT ad ops

Standing instructions for any Claude session in this repo.

**What this is:** the `adbot` Meta-ads automation, copied from `marketthinkmy-code/soocheng-ads`
on 2026-11-09 and re-parameterised for MOI (Ah Moi). Code, guardrail logic and schedule are the
same as Stock Bloom's; only `config/` (plus the 付款学员 sheet parsing in `src/adbot/cpa.py`)
differs. It shares **no keys, state or schedule** with soocheng-ads — every secret in this repo
belongs to MOI alone.

**Product:** MOI FU Money Blueprint (让钱工作资产增长蓝图). Funnel: Meta ad → free webinar
registration (https://fumoneyblueprint.com/register-page) → RM1,997 course.
Markets: Malaysia + Singapore (currently in the same ads; to be split later). Language: Chinese.

**Meta:** ad account `act_2165219017411034` («Ah Moi 666», MYR) · Page `1285525351321816` ·
IG `17841438769308083` · Pixel `1654213532722358` · special ad category FINANCIAL_PRODUCTS_SERVICES.

## Owner rules (2026-11-09)

- **The bot manages the WHOLE ad account**, including campaigns built by hand
  («Moi 让钱工作资产增长蓝图 Leads campaign …»): the monitor judges every ACTIVE
  registration-optimised ad, and weekly OFF (Wed 15:00 MYT) / ON (Thu 00:00 MYT) covers the account.
- **CPL line RM40** while MY + SG share ads (target MY < RM30, SG < RM50 once split).
  Judge an ad only after RM60 spend.
- **CPA:** price RM1,997 · target RM700 · healthy ≤780 · acceptable ≤900 · **auto-pause > RM1,000**
  (only with real matched sales, ≥14 days and ≥RM1,000 spend). Zero matched sales never pauses on CPA.
- **Sales sheet:** «Ah Moi funnel Register and Purchase list», tab `付款学员`. Its `source`
  column is the campaign (a trailing " ig" / " fb" is stripped), `UTM Ads Set` / `UTM Ads Name`
  are the ad set / ad, `報名日期` is the date. Most paid rows are `moi-ig` (organic IG invite),
  so CPA only sees the ad-attributed minority. The 15 OCT 2026 campaigns live in an older ad
  account, so their sales never match this account's spend.
- **Creatives:** Drive folder «ECOM- MOI / 自動跑» (`1cemMVoa2IWSQSiPSVVQ_-p2avVhWXbtP`).

## Status

- ⏸ **All schedules are disabled** (commented out in `.github/workflows/`). Re-enable only after
  the owner has seen `doctor` + the monitor dry run and said go. Then set up cron-job.org to
  dispatch `adbot-monitor.yml` about every 20 minutes (GitHub's own cron runs hours late).
- 📝 `config/audience.md` and `prompts/caption_system.md` still need MOI's persona; caption
  generation is blocked until the TODO in `audience.md` is gone.

## Hard rules

- Everything is built **PAUSED**; the owner activates. Never auto-activate.
- The monitor only pauses; it never re-activates. Never reopen what the owner paused by hand.
- Financial vertical compliance: no income / profit figures, no guaranteed or expected returns,
  no get-rich / risk-free / 100% language. A creative Meta rejects is never resubmitted —
  add it to `compliance.banned_creatives`.
- If a command errors, report the error verbatim and stop. Never print secret values.
