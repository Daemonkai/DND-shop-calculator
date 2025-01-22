import streamlit as st

def main():
    st.title("Scroll Crafting Calculator")

    # Input fields
    months = st.number_input("Months to simulate", min_value=1, max_value=12, value=12)
    tax = st.number_input("Tax rate (e.g. 0.30 = 30%)", min_value=0.0, max_value=1.0, value=0.30, step=0.01)

    # Pressing "Calculate" triggers the main logic
    if st.button("Calculate"):
        # Constants
        days_in_year = 365
        workdays_per_week = 5
        sale_price = 50
        cost_per_scroll = 25
        wizard_scrolls_per_day = 2
        hireling_scrolls_per_day = 1
        num_hirelings = 2
        hireling_cost_per_day = 2
        rations_cost = 1
        living_cost = rations_cost * (5 + num_hirelings)
        shop_rent_yearly = 1750

        # Derived values
        days_to_sim = months * (days_in_year // 12)
        total_scrolls_each_day = wizard_scrolls_per_day + (hireling_scrolls_per_day * num_hirelings)
        rent_for_period = shop_rent_yearly * (months / 12)

        # Simulation variables
        total_scrolls = 0
        total_income = 0
        total_cost = 0
        total_tax_paid = 0

        # Simulate day-by-day
        for day in range(days_to_sim):
            if day % 7 < workdays_per_week:
                daily_scrolls = total_scrolls_each_day
                total_scrolls += daily_scrolls

                # Cost to craft
                total_cost += cost_per_scroll * daily_scrolls

                # Income & tax
                daily_income = daily_scrolls * sale_price
                daily_tax = daily_income * tax
                total_tax_paid += daily_tax
                total_income += (daily_income - daily_tax)

                # Living cost
                total_cost += living_cost

        # Add shop rent
        total_cost += rent_for_period

        # Net profit
        net_profit = total_income - total_cost

        # Display results
        st.subheader("Results")
        st.write(f"**Total Scrolls Crafted:** {total_scrolls}")
        st.write(f"**Total Income (Before Tax):** {total_scrolls * sale_price:.2f} GP")
        st.write(f"**Total Tax Paid:** {total_tax_paid:.2f} GP")
        st.write(f"**Total Income (After Tax):** {total_income:.2f} GP")
        st.write(f"**Net Profit:** {net_profit:.2f} GP")

if __name__ == "__main__":
    main()
