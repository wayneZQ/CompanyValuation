"""
两段式自由现金流（FCF）估值模型
author: zhong wei qi
"""


# ========== 1. 用户输入区（改成你要算的公司） ==========
fcf0 = 1940  # 最近一年自由现金流，亿元
shares = 91.79  # 总股本，亿股
net_cash = 670  # 净现金（现金-有息负债），亿元；如果是净负债请填负数
growth_high = 0.10  # 未来10年复合增长率
growth_perp = 0.05  # 永续增长率
wacc_list = [0.08, 0.10, 0.12]  # 想对比的折现率情景


# ========================================================

def dcf_value(fcf0, g_high, g_perp, wacc, shares, net_cash):
    """两段式DCF核心计算，返回股权价值（亿元）和每股价值（元）"""
    # 1) 预测未来10年FCF并折现
    pv_high = 0
    for t in range(1, 11):
        fcf_t = fcf0 * (1 + g_high) ** t
        pv_high += fcf_t / (1 + wacc) ** t

    # 2) 第11年起永续现金流（Gordon Growth）折现到第10年末
    fcf_11 = fcf0 * (1 + g_high) ** 10 * (1 + g_perp)
    term_val = fcf_11 / (wacc - g_perp)
    pv_term = term_val / (1 + wacc) ** 10

    # 3) 企业价值 → 股权价值 → 每股价值
    ent_value = pv_high + pv_term
    eq_value = ent_value + net_cash
    per_share = eq_value / shares
    return eq_value, per_share


# ========== 2. 跑三种情景 ==========
print("两段式FCF估值结果（单位：亿元，每股元）\n")
for wacc in wacc_list:
    eq, ps = dcf_value(fcf0, growth_high, growth_perp, wacc, shares, net_cash)
    print(f"WACC={wacc:.0%}: 股权价值={eq:,.0f}亿，每股={ps:,.2f}元")
