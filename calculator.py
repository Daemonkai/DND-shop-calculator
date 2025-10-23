from dataclasses import dataclass
from typing import Dict


@dataclass
class Config:
    days_in_year: int = 315
    months_in_year: float = 10.5
    months_to_simulate: float = 10.5
    workdays_per_week: int = 5

    sale_price_per_scroll: float = 50.0
    crafting_cost_per_scroll: float = 25.0
    tax_rate: float = 0.30  # 0.30 == 30%

    number_of_wizards: int = 1
    scrolls_per_day_wizard: int = 2
    scrolls_per_day_hireling: int = 1
    number_of_hirelings: int = 2

    skilled_hireling_cost_per_day: float = 2.0

    living_cost_per_person_per_day: float = 1.0
    living_cost_people_count: int = 5  # total people covered by living costs

    total_shop_rent_per_year: float = 1575.0


def _workdays_in_period(total_days: int, workdays_per_week: int) -> int:
    if workdays_per_week <= 0:
        return 0
    weeks = total_days // 7
    remainder = total_days % 7
    return weeks * workdays_per_week + min(remainder, workdays_per_week)


def calculate(cfg: Config) -> Dict[str, float]:
    # Convert months to days based on custom calendar
    days_to_simulate = int(round(cfg.months_to_simulate * (cfg.days_in_year / cfg.months_in_year)))

    # Count of effective workdays within the simulated period
    workdays = _workdays_in_period(days_to_simulate, cfg.workdays_per_week)

    # Production per workday
    total_scrolls_per_day = (
        cfg.number_of_wizards * cfg.scrolls_per_day_wizard
        + cfg.number_of_hirelings * cfg.scrolls_per_day_hireling
    )

    # Totals driven by workdays
    total_scrolls_crafted = total_scrolls_per_day * workdays

    gross_income = total_scrolls_crafted * cfg.sale_price_per_scroll
    total_tax_paid = gross_income * cfg.tax_rate
    net_income_after_tax = gross_income - total_tax_paid

    crafting_cost_total = total_scrolls_crafted * cfg.crafting_cost_per_scroll
    hireling_cost_total = cfg.skilled_hireling_cost_per_day * cfg.number_of_hirelings * workdays
    living_cost_total = (
        cfg.living_cost_per_person_per_day
        * cfg.living_cost_people_count
        * days_to_simulate
    )

    # Overhead proportional to simulated months
    proportional_shop_rent = cfg.total_shop_rent_per_year * (cfg.months_to_simulate / cfg.months_in_year)

    # Aggregate costs and net profit
    total_cost = crafting_cost_total + hireling_cost_total + living_cost_total + proportional_shop_rent
    net_profit = net_income_after_tax - total_cost

    return {
        "Days To Simulate": float(days_to_simulate),
        "Workdays": float(workdays),
        "Total Scrolls Crafted": float(total_scrolls_crafted),
        "Total Income Before Tax (GP)": gross_income,
        "Total Tax Paid (GP)": total_tax_paid,
        "Total Income After Tax (GP)": net_income_after_tax,
        "Total Crafting Cost (GP)": crafting_cost_total,
        "Total Hireling Cost (GP)": hireling_cost_total,
        "Total Living Cost (GP)": living_cost_total,
        "Proportional Shop Rent (GP)": proportional_shop_rent,
        "Net Profit (GP)": net_profit,
    }
