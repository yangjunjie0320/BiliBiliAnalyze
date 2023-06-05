import sys, os, re
from bilibili import BiliBiliVideo

bv_list = [
    "BV1MY4y1R7EN",
    "BV1VL411U7MU",
    "BV15v4y1E7zV",
    "BV1Nm4y1z7AT",
    "BV1rj41137cr"
]

for ibv, bv in enumerate(bv_list):
    print(f"Processing {ibv+1}/{len(bv_list)}: {bv}")

    v = BiliBiliVideo(bv)
    v.dump_info()
    rs = v.dump_reply()

    # dump the first 100 replies
    with open(f"./for-ylt/reply-{bv}-1.csv", "w") as f:
        for i, r in enumerate(rs):
            if i == 100:
                break
            f.write(f"{i+1:4d}, {r[1]}\n")

    with open(f"./for-ylt/reply-{bv}-2.csv", "w") as f:
        for i, r in enumerate(rs):
            if i == 100:
                break

            tmp = re.sub(r'[^\w\u4e00-\u9fa5]', '', r[1])
            f.write(f"{i+1:4d}, {tmp}\n")