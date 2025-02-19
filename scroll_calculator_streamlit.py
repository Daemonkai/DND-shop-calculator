import streamlit as st

def main():
    st.title("Scroll Crafting Calculator")

    st.write("""
    Enter all your parameters below. Then click **Calculate** to see the results.

    **Note:** For the tax rate, use 0.20 for 20%, 0.30 for 30%, etc.
    """)

    days_in_year = st.number_input("Days in a year", min_value=1, max_value=1000, value=315, step=1)
    months_to_simulate = st.number_input("Months to simulate", min_value=0.1, max_value=24.0, value=10.5, step=0.1)
    workdays_per_week = st.number_input("Workdays per week", min_value=1, max_value=7, value=5, step=1)
    vanilla_sale_price_per_scroll = st.number_input("Sale price per scroll (GP)", min_value=0.0, value=50.0, step=1.0)
    vanilla_crafting_cost_per_scroll = st.number_input("Crafting cost per scroll (GP)", min_value=0.0, value=25.0, step=1.0)
    tax_rate = st.number_input("Tax rate (e.g., 0.30 = 30%)", min_value=0.0, max_value=1.0, value=0.30, step=0.01)
    scrolls_per_day_wizard = st.number_input("Scrolls per day (Wizard)", min_value=0, max_value=100, value=2, step=1)
    scrolls_per_day_hireling = st.number_input("Scrolls per day (Hireling)", min_value=0, max_value=100, value=1, step=1)
    number_of_hirelings = st.number_input("Number of hirelings", min_value=0, max_value=100, value=2, step=1)
    skilled_hireling_cost_per_day = st.number_input("Skilled hireling cost per day (GP)", min_value=0.0, value=2.0, step=0.5)
    gp_cost_per_day_for_rations = st.number_input("Living cost per person per day (GP)", min_value=0.0, value=1.0, step=0.5)
    total_shop_rent = st.number_input("Total shop rent (per year, GP)", min_value=0.0, value=1522.0, step=10.0)

    if st.button("Calculate"):

        # New calendar data: 10.5 months in a year
        MONTHS_IN_YEAR = 10.5

        # Calculate total days to simulate based on the new calendar
        days_to_simulate = int(months_to_simulate * (days_in_year / MONTHS_IN_YEAR))

        # Daily living cost for the wizard (assumed 5 persons) plus hirelings
        living_cost_per_day = gp_cost_per_day_for_rations * (5 + number_of_hirelings)
        total_scrolls_per_day = scrolls_per_day_wizard + (scrolls_per_day_hireling * number_of_hirelings)

        # Calculate yearly hireling cost and then the proportional cost for the simulation period.
        total_hireling_cost = skilled_hireling_cost_per_day * number_of_hirelings * days_in_year
        proportional_shop_rent = total_shop_rent * (months_to_simulate / MONTHS_IN_YEAR)
        # (Note: proportional_hireling_cost is computed for reference; it's not added to total_cost.)
        proportional_hireling_cost = total_hireling_cost * (months_to_simulate / MONTHS_IN_YEAR)

        # Initialize simulation totals.
        total_scrolls_crafted = 0
        total_income = 0
        total_cost = 0
        total_tax_paid = 0

        # Simulation loop: Iterate over each simulated day.
        for day in range(days_to_simulate):
            # Work only on the designated workdays each week.
            if day % 7 < workdays_per_week:
                daily_scrolls = total_scrolls_per_day
                total_scrolls_crafted += daily_scrolls

                # Add the crafting cost for today's scrolls.
                total_cost += vanilla_crafting_cost_per_scroll * daily_scrolls

                # Calculate income and tax for the day.
                income = daily_scrolls * vanilla_sale_price_per_scroll
                tax = income * tax_rate
                total_tax_paid += tax
                total_income += income - tax

                # Add daily living costs.
                total_cost += living_cost_per_day

        # Add the proportional shop rent for the simulated period.
        total_cost += proportional_shop_rent

        # Calculate net profit.
        net_profit_with_new_config = total_income - total_cost

        # Prepare results with a breakdown of metrics.
        adjusted_vanilla_with_new_config_data = {
            "Metric": [
                "Total Scrolls Crafted",
                "Total Income Before Tax (GP)",
                "Total Tax Paid (GP)",
                "Total Income After Tax (GP)",
                "Total Crafting Cost (GP)",
                "Proportional Shop Rent (GP)",
                "Total Living Cost (GP)",
                "Total Hireling Cost (GP)",
                "Net Profit (GP)",
            ],
            "Value": [
                total_scrolls_crafted,
                total_scrolls_crafted * vanilla_sale_price_per_scroll,
                total_tax_paid,
                total_income,
                (total_cost 
                 - proportional_shop_rent 
                 - (living_cost_per_day * days_to_simulate) 
                 - (skilled_hireling_cost_per_day * number_of_hirelings * days_to_simulate)),
                proportional_shop_rent,
                living_cost_per_day * days_to_simulate,
                skilled_hireling_cost_per_day * number_of_hirelings * days_to_simulate,
                net_profit_with_new_config,
            ],
        }

        st.write("## Final Results")

        result_lines = []
        for metric, value in zip(adjusted_vanilla_with_new_config_data["Metric"],
                                 adjusted_vanilla_with_new_config_data["Value"]):
            # Format floats to 2 decimal places.
            if isinstance(value, float):
                line = f"{metric:<35} {value:12.2f}"
            else:
                line = f"{metric:<35} {value:12}"
            result_lines.append(line)
        
        st.code("\n".join(result_lines))

if __name__ == "__main__":
    main()
