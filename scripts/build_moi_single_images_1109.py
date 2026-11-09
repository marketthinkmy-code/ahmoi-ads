# -*- coding: utf-8 -*-
"""Build «MOI | 单图 x5 | MY+SG | CBO RM100 | 9 NOV 2026» — everything PAUSED.

Owner request 2026-11-09: put the 5 new single images into ONE ad set, CBO, Malaysia +
Singapore, daily budget RM100, copy written in the style of MOI's existing course ads.

Run through the ops workflow (adbot-ops.yml, script=build_moi_single_images_1109.py):
  confirm=false -> dry run: print every payload, create nothing
  confirm=true  -> upload the 5 images and create campaign / ad set / 5 ads, all PAUSED
Resumable: reuses the campaign / ad set / ads already created under these names (no duplicates).
The owner reviews in Ads Manager and switches the campaign on by hand.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from adbot.commands import graph_client
from adbot.settings import load_settings

CONFIRM = os.environ.get("CONFIRM", "false").lower() == "true"
ROOT = Path(os.environ.get("ADBOT_ROOT", Path(__file__).resolve().parents[1]))
IMG_DIR = ROOT / "creatives" / "2026-11-09"

CAMPAIGN_NAME = "MOI | 单图 x5 | MY+SG | CBO RM100 | 9 NOV 2026"
ADSET_NAME = "MOI | Broad MY+SG | 中文 | 单图 x5"
DAILY_BUDGET_CENTS = 100_00          # RM100 / day, campaign level (CBO)
HEADLINE = "免费线上分享会｜让钱工作，资产增长蓝图"
DISCLAIMER = "⚠️ 个人经验与投资教育分享，不构成个别投资建议。投资有风险，过去表现不代表未来。"
CTA_LINE = "👇 点击「Learn More」，立即免费报名！"
ME = "👋 我是 Moi。29 岁时，我的投资组合已经超过 RM1,000,000。"
FTP = ("🔍 Fundamental：这家公司值不值得拥有？\n"
       "⏳ Timing：现在这个价格值不值得买？\n"
       "🛡️ Portfolio：这一笔，到底应该放多少？")

ADS = [
    {
        "file": "si01_stock-drop-3-questions.jpg",
        "name": "MOI SI01｜股价跌了，下单前先问三句",
        "body": f"""💰 股价跌了，你第一个念头是：「便宜了，快点买」？
先等一下。

最近市场消息一个接一个，股价一跌，很多人就急着进场。
但跌下来的价格，不一定是折扣。
它也可能是风险，正在提醒你一些事。

下单之前，我会先问自己这三句👇

1️⃣ 发生了什么事？
是整个市场情绪在波动，还是这家公司本身出了问题？

2️⃣ 会影响公司赚钱吗？
短期的新闻，和长期做生意的能力，是两件不同的事。

3️⃣ 跌到这个价，真的便宜了吗？
「比之前低」，不等于「低过它值的价」。

问完这三句，才轮到最后一个问题：这一笔，应该放多少钱？🛡️

{ME}
我买之前，看的就是 FTP 三件事：
{FTP}

在《让钱工作，资产增长蓝图》免费线上分享会，我会拿真实案例拆给你看，
学会判断：跌下来的价格，到底值不值得买。

{CTA_LINE}

{DISCLAIMER}""",
    },
    {
        "file": "si02_keep-vs-invest.jpg",
        "name": "MOI SI02｜有一笔钱，多少该留多少能投",
        "body": f"""💰 有一笔钱，多少该留，多少能投？

很多人一存到钱，第一个问题是：「我应该买什么？」
但在问买什么之前，有一个更基本的问题——

这笔钱，哪些是你短期要用的？
哪些，才是可以长期放着的？✉️

📌 短期要用：应急金、几年内买房、结婚、孩子的学费……
📌 长期可投：短时间内不会动用，市场跌了也不用急着卖的钱。

分错信封，问题就来了：
短期要用的钱拿去投资，市场一跌，你可能被迫在低点卖掉。📉
可以长期投入的钱一直闲着，它就少了为你工作的时间。⏳

先分清楚，再谈买什么，才不会每次一跌就慌。

{ME}

在《让钱工作，资产增长蓝图》免费线上分享会，我会带你：
🎯 根据现有本金、每月可投入金额和理想生活，算出自己的 FU Money 目标。
🧭 分清楚哪些钱该留、哪些钱可以长期投入。
🛡️ 通过 FTP 投资决策系统，理清「买什么、什么时候买、买多少」。

你已经学会靠自己赚钱。
下一步，学会怎样安排赚回来的钱。

{CTA_LINE}

{DISCLAIMER}""",
    },
    {
        "file": "si03_fd-renew-auntie.jpg",
        "name": "MOI SI03｜定存到期了，要续存吗",
        "body": f"""💰 定存到期了，要续存吗？

很多人收到 FD 到期通知，第一个反应是：「续多一次吧，最安全。」

续存没有错。
但在签名之前，值得多问自己几个问题👇

🤔 这笔钱，未来几年会不会用到？
🤔 算上通胀，它的购买力还剩多少？
🤔 除了续存，还有没有其他安排，适合我的年纪和需要？

有些钱，确实应该放在随时拿得到的地方。
有些钱，可以考虑更长期的安排。
重点不是「全部搬走」，也不是「全部不动」，而是每一笔钱都有清楚的用途。🧭

{ME}
我做每一个决定之前，都会先想清楚：这笔钱的任务是什么。

在《让钱工作，资产增长蓝图》免费线上分享会，我会带你了解：
🎯 你的生活和退休目标，大概需要多少资产。
🧭 FD、EPF、ETF、个股，各自适合放哪一种钱。
🛡️ 怎样安排资金，避免一次判断错误影响整个财富计划。

不用急着做决定。先学会怎样安排这笔钱。

{CTA_LINE}

{DISCLAIMER}""",
    },
    {
        "file": "si04_fd-beyond-renew.jpg",
        "name": "MOI SI04｜FD 到期，除了续存还能怎么安排",
        "body": f"""💰 定存到期了，这笔钱除了续存，还能怎么安排？

刚好遇上美股回调，很多人心里开始痒：
「是不是应该拿 FD 的钱进场？」

先别急。
回调可能是机会，也可能继续跌。📉
在决定之前，先分清楚：哪一部分资金，是你真的可以长期放着的？

我会这样想👇

1️⃣ 近期要用的钱：先留着，不跟市场赌时间。
2️⃣ 可以长期投入的钱：才考虑分批、长期的安排。
3️⃣ 每一笔投进去之前：先想好「如果判断错了，会伤到整盘钱多少？」

不是 FD 不好，也不是投资一定比较好。
每一种工具，都有它适合的用途。

{ME}
我买之前，会看 FTP 三件事：
{FTP}

来参加《让钱工作，资产增长蓝图》免费线上分享会，
跟我学看公司，算出自己的 FU Money。

{CTA_LINE}

{DISCLAIMER}""",
    },
    {
        "file": "si05_retirement-foundation.jpg",
        "name": "MOI SI05｜退休生活可以慢慢想，地基要早点算",
        "body": f"""💰 退休生活可以慢慢想。它的地基，要早点算。

你想退休后怎样过？
每年去旅行几次？周末和家人吃饭？还是继续做自己喜欢的事？🏡

这些画面，每一个都有价钱。

很多人的顺序是：先努力存钱，存到「差不多」再说。
但「差不多」，到底是多少？

我的建议是反过来👇
📍 先想好退休后想怎样过；
📍 再估算这种生活，每年大概需要多少；
📍 最后才算出：从今天开始，要准备多少，每个月要投入多少。

这个数字，我叫它你的 FU Money。
算清楚了，你才知道自己离「有选择权」还有多远。🧭

越早算，你越有时间准备；越晚算，每个月要补的就越多。⏳

{ME}

在《让钱工作，资产增长蓝图》免费线上分享会，我会带你：
🎯 根据理想生活，估算自己的 FU Money 目标。
🧭 通过 FTP 投资决策系统，理清「买什么、什么时候买、买多少」。
🛡️ 学习分配资金，降低一次判断错误对整体资产的影响。

{CTA_LINE}

{DISCLAIMER}""",
    },
]


def main() -> None:
    s = load_settings()
    m = s.meta
    account = m.account_path
    countries = ["MY", "SG"]

    campaign = {
        "name": CAMPAIGN_NAME, "objective": m.objective, "buying_type": "AUCTION",
        "status": "PAUSED",
        "special_ad_categories": m.special_ad_categories,
        "special_ad_category_country": countries if m.special_ad_categories else [],
        "daily_budget": DAILY_BUDGET_CENTS,
        "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
    }
    # Financial special ad category: Meta requires age 18-65 and no detailed targeting,
    # so the ad set is broad (countries + Chinese language) with Advantage+ audience.
    adset = {
        "name": ADSET_NAME, "optimization_goal": m.optimization_goal,
        "billing_event": "IMPRESSIONS", "promoted_object": m.promoted_object,
        "targeting": {"geo_locations": {"countries": countries},
                      "age_min": 18, "age_max": 65, "locales": [20, 21, 22],
                      "targeting_automation": {"advantage_audience": 1}},
        # Meta: ads that include Singapore must declare this regional regulated category.
        "regional_regulated_categories": ["SINGAPORE_UNIVERSAL"],
        "status": "PAUSED",
    }

    def creative(ad, image_hash):
        spec = {"name": ad["name"], "object_story_spec": {
            "page_id": m.page_id,
            "link_data": {"link": m.lead_destination.link_url, "image_hash": image_hash,
                          "message": ad["body"], "name": HEADLINE,
                          "call_to_action": {"type": m.call_to_action,
                                             "value": {"link": m.lead_destination.link_url}}}}}
        if m.instagram_user_id:
            spec["object_story_spec"]["instagram_user_id"] = m.instagram_user_id
        if m.url_tags:
            spec["url_tags"] = m.url_tags
        return spec

    for ad in ADS:
        assert (IMG_DIR / ad["file"]).exists(), f"missing image {ad['file']}"

    if not CONFIRM:
        print("=== DRY RUN (confirm=false): nothing is created ===")
        print("CAMPAIGN:", json.dumps(campaign, ensure_ascii=False))
        print("AD SET:  ", json.dumps(adset, ensure_ascii=False))
        for ad in ADS:
            print(f"\n--- AD «{ad['name']}»  image={ad['file']}")
            print(json.dumps(creative(ad, "<image_hash>"), ensure_ascii=False, indent=1))
        print(f"\nSUMMARY: dry run — would create 1 campaign (CBO RM{DAILY_BUDGET_CENTS / 100:.0f}/day), "
              f"1 ad set, {len(ADS)} ads, all PAUSED")
        return

    g = graph_client(s)

    # Resumable: re-uploading an image returns the same hash, and a campaign / ad set /
    # ad that already exists under this name is reused instead of created again.
    hashes = {}
    for ad in ADS:
        hashes[ad["file"]] = g.upload_image(account, str(IMG_DIR / ad["file"]))
        print(f"uploaded {ad['file']} -> {hashes[ad['file']]}")

    same = [c for c in g.list_campaigns(account) if c.get("name") == CAMPAIGN_NAME]
    if len(same) > 1:
        raise SystemExit(f"{len(same)} campaigns named «{CAMPAIGN_NAME}» — clean up by hand first")
    if same:
        campaign_id = same[0]["id"]
        print("campaign", campaign_id, "(already exists, reused)")
    else:
        campaign_id = g.create_campaign(account, **campaign)["id"]
        print("campaign", campaign_id, "(PAUSED)")

    adsets = {a["name"]: a["id"] for a in g._get_all(f"{campaign_id}/adsets", {"fields": "id,name"})}
    if ADSET_NAME in adsets:
        adset_id = adsets[ADSET_NAME]
        print("ad set", adset_id, "(already exists, reused)")
    else:
        adset_id = g.create_adset(account, campaign_id=campaign_id, **adset)["id"]
        print("ad set", adset_id, "(PAUSED)")

    existing_ads = {a["name"] for a in g._get_all(f"{adset_id}/ads", {"fields": "id,name"})}
    ad_ids = []
    for ad in ADS:
        if ad["name"] in existing_ads:
            print(f"ad «{ad['name']}» already exists, skipped")
            continue
        creative_id = g.create_adcreative(account, **creative(ad, hashes[ad["file"]]))["id"]
        new = g.create_ad(account, name=ad["name"], adset_id=adset_id,
                          creative={"creative_id": creative_id}, status="PAUSED",
                          conversion_domain=m.conversion_domain_bare or None)
        ad_ids.append(new["id"])
        print(f"ad {new['id']}  «{ad['name']}»  creative {creative_id} (PAUSED)")

    print(f"\nSUMMARY: created campaign {campaign_id}, ad set {adset_id}, "
          f"{len(ad_ids)} ads — all PAUSED; owner activates in Ads Manager")


if __name__ == "__main__":
    main()
