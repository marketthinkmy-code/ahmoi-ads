# -*- coding: utf-8 -*-
"""Build «MOI | SCALE | 3 角度 Broad | ABO | 12 NOV 2026» — everything PAUSED.

Owner 2026-11-10 (proposal 1): put each winning ad angle into ONE broad ad set and let Meta
find the prospects. Winners picked by lifetime CPL (11/2–11/10, registrations only — no CPA yet):

  A ETF/指数        vd 05 EPF vs QQQ · carousel 02 VOO · vd 08 定投 QQQ · carousel 04 无脑 QQQ
  B 存钱/理财观念    carousel 05 30 岁前存到 RM100K · vd 07 钱是拿来存的
  C 现金流          vd 06 Buy, Borrow, Die · carousel 01 用现金流买车

Each new ad reuses the SOURCE ad's creative_id, so it runs the same post (likes / comments
carry over) with the same copy, link and UTM. ABO at RM100/day per ad set so every angle gets
its own data (in a CBO the cheapest angle would take the whole budget). Ad sets start
2026-11-12 00:00 MYT (the weekly reset); the owner still switches the campaign on by hand.

Run through the ops workflow (adbot-ops.yml, script=build_moi_scale_angles_1112.py):
  confirm=false -> dry run: read the source ads, print every payload, create nothing
  confirm=true  -> create campaign / 3 ad sets / 8 ads, all PAUSED
Resumable: reuses a campaign / ad set / ad that already exists under the same name.
"""
from __future__ import annotations

import json
import os

from adbot.commands import graph_client
from adbot.settings import load_settings

CONFIRM = os.environ.get("CONFIRM", "false").lower() == "true"

CAMPAIGN_NAME = "MOI | SCALE | 3 角度 Broad | ABO | 12 NOV 2026"
START_TIME = "2026-11-12T00:00:00+0800"
ADSET_BUDGET_CENTS = 100_00      # RM100 / day per ad set (ABO)
COUNTRIES = ["MY", "SG"]

ANGLES = [
    ("MOI | A ETF/指数 | Broad MY+SG", [
        "120251921826760682",   # Moi vd 05｜RM100k：EPF vs QQQ          RM576.97 / 17 = 33.94
        "120251937880390682",   # Moi carousel 02｜1 分钟说服你了解 VOO   RM186.92 / 10 = 18.69
        "120251921826780682",   # Moi vd 08｜20–30 岁定投 QQQ             RM315.56 / 8  = 39.45
        "120251938300920682",   # Moi carousel 04｜无脑投资 QQQ           RM109.98 / 3  = 36.66
    ]),
    ("MOI | B 存钱/理财观念 | Broad MY+SG", [
        "120251938417530682",   # Moi carousel 05｜30 岁前存到 RM100K     RM86.99 / 10  = 8.70
        "120251921826740682",   # Moi vd 07｜钱是拿来存的，不是拿来花的   RM354.38 / 13 = 27.26
    ]),
    ("MOI | C 现金流 | Broad MY+SG", [
        "120251921826770682",   # Moi vd 06｜Maybank：Buy, Borrow, Die    RM90.33 / 6   = 15.06
        "120251937880400682",   # Moi carousel 01｜用现金流买车           RM32.58 / 3   = 10.86
    ]),
]


def main() -> None:
    s = load_settings()
    m = s.meta
    account = m.account_path
    g = graph_client(s)

    # Source ads: name + creative id (read-only, also in the dry run).
    sources = {}
    for _, ad_ids in ANGLES:
        for ad_id in ad_ids:
            ad = g.get_object(ad_id, "name,creative{id}")
            sources[ad_id] = {"name": ad["name"], "creative_id": ad["creative"]["id"]}

    campaign = {
        "name": CAMPAIGN_NAME, "objective": m.objective, "buying_type": "AUCTION",
        "status": "PAUSED",
        "special_ad_categories": m.special_ad_categories,
        "special_ad_category_country": COUNTRIES if m.special_ad_categories else [],
        "is_adset_budget_sharing_enabled": False,   # ABO: each ad set keeps its own budget
    }

    def adset_fields(name):
        return {
            "name": name, "optimization_goal": m.optimization_goal,
            "billing_event": "IMPRESSIONS", "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
            "daily_budget": ADSET_BUDGET_CENTS, "promoted_object": m.promoted_object,
            "targeting": {"geo_locations": {"countries": COUNTRIES},
                          "age_min": 18, "age_max": 65, "locales": [20, 21, 22],
                          "targeting_automation": {"advantage_audience": 1}},
            "regional_regulated_categories": ["SINGAPORE_UNIVERSAL"],
            "start_time": START_TIME,
            "status": "PAUSED",
        }

    if not CONFIRM:
        print("=== DRY RUN (confirm=false): nothing is created ===")
        print("CAMPAIGN:", json.dumps(campaign, ensure_ascii=False))
        for adset_name, ad_ids in ANGLES:
            print("\nAD SET:", json.dumps(adset_fields(adset_name), ensure_ascii=False))
            for ad_id in ad_ids:
                src = sources[ad_id]
                print(f"  AD «{src['name']}»  reuses creative {src['creative_id']} (from ad {ad_id})")
        n_ads = sum(len(a) for _, a in ANGLES)
        print(f"\nSUMMARY: dry run — would create 1 ABO campaign, {len(ANGLES)} ad sets "
              f"(RM{ADSET_BUDGET_CENTS / 100:.0f}/day each, start {START_TIME}), {n_ads} ads, all PAUSED")
        return

    same = [c for c in g.list_campaigns(account) if c.get("name") == CAMPAIGN_NAME]
    if len(same) > 1:
        raise SystemExit(f"{len(same)} campaigns named «{CAMPAIGN_NAME}» — clean up by hand first")
    if same:
        campaign_id = same[0]["id"]
        print("campaign", campaign_id, "(already exists, reused)")
    else:
        campaign_id = g.create_campaign(account, **campaign)["id"]
        print("campaign", campaign_id, "(PAUSED)")

    existing_sets = {a["name"]: a["id"] for a in g._get_all(f"{campaign_id}/adsets", {"fields": "id,name"})}
    created = 0
    for adset_name, ad_ids in ANGLES:
        if adset_name in existing_sets:
            adset_id = existing_sets[adset_name]
            print(f"\nad set {adset_id} «{adset_name}» (already exists, reused)")
        else:
            adset_id = g.create_adset(account, campaign_id=campaign_id, **adset_fields(adset_name))["id"]
            print(f"\nad set {adset_id} «{adset_name}» (PAUSED, RM{ADSET_BUDGET_CENTS / 100:.0f}/day)")
        existing_ads = {a["name"] for a in g._get_all(f"{adset_id}/ads", {"fields": "id,name"})}
        for ad_id in ad_ids:
            src = sources[ad_id]
            if src["name"] in existing_ads:
                print(f"  ad «{src['name']}» already exists, skipped")
                continue
            new = g.create_ad(account, name=src["name"], adset_id=adset_id,
                              creative={"creative_id": src["creative_id"]}, status="PAUSED",
                              conversion_domain=m.conversion_domain_bare or None)
            created += 1
            print(f"  ad {new['id']}  «{src['name']}»  creative {src['creative_id']} (PAUSED)")

    print(f"\nSUMMARY: campaign {campaign_id}, {len(ANGLES)} ad sets, {created} new ads — all PAUSED; "
          f"ad sets start {START_TIME}; owner switches the campaign on in Ads Manager")


if __name__ == "__main__":
    main()
