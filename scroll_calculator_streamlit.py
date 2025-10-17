import streamlit as st
from calculator import Config, calculate

def main():
    st.title("Scroll Crafting Calculator")

    st.write("""
    Enter all your parameters below. Then click **Calculate** to see the results.

    **Note:** For the tax rate, use 0.20 for 20%, 0.30 for 30%, etc.
    """)

    left, right = st.columns(2)
    with left:
        days_in_year = st.number_input("Days in a year", min_value=1, max_value=1000, value=315, step=1)
        months_in_year = st.number_input("Months in a year", min_value=1.0, max_value=24.0, value=10.5, step=0.1)
        months_to_simulate = st.number_input("Months to simulate", min_value=0.1, max_value=60.0, value=10.5, step=0.1)
        workdays_per_week = st.number_input("Workdays per week", min_value=0, max_value=7, value=5, step=1)
        tax_rate = st.number_input("Tax rate (e.g., 0.30 = 30%)", min_value=0.0, max_value=1.0, value=0.30, step=0.01)
        currency = st.text_input("Currency label", value="GP")
    with right:
        sale_price_per_scroll = st.number_input(f"Sale price per scroll ({currency})", min_value=0.0, value=50.0, step=1.0)
        crafting_cost_per_scroll = st.number_input(f"Crafting cost per scroll ({currency})", min_value=0.0, value=25.0, step=1.0)
        number_of_wizards = st.number_input("Number of wizards", min_value=0, max_value=100, value=1, step=1)
        scrolls_per_day_wizard = st.number_input("Scrolls per day per wizard", min_value=0, max_value=100, value=2, step=1)
        number_of_hirelings = st.number_input("Number of hirelings", min_value=0, max_value=100, value=2, step=1)
        scrolls_per_day_hireling = st.number_input("Scrolls per day per hireling", min_value=0, max_value=100, value=1, step=1)
    skilled_hireling_cost_per_day = st.number_input(f"Skilled hireling wage per day ({currency})", min_value=0.0, value=2.0, step=0.5)
    living_cost_per_person_per_day = st.number_input(
        f"Living cost per person per day ({currency})",
        min_value=0.0,
        value=1.0,
        step=0.5,
    )
    living_cost_people_count = st.number_input("People covered by living costs", min_value=0, max_value=100, value=5, step=1)
    total_shop_rent = st.number_input(f"Total shop rent (per year, {currency})", min_value=0.0, value=1522.0, step=10.0)

    if st.button("Calculate"):
        cfg = Config(
            days_in_year=days_in_year,
            months_in_year=months_in_year,
            months_to_simulate=months_to_simulate,
            workdays_per_week=workdays_per_week,
            sale_price_per_scroll=sale_price_per_scroll,
            crafting_cost_per_scroll=crafting_cost_per_scroll,
            tax_rate=tax_rate,
            number_of_wizards=number_of_wizards,
            scrolls_per_day_wizard=scrolls_per_day_wizard,
            scrolls_per_day_hireling=scrolls_per_day_hireling,
            number_of_hirelings=number_of_hirelings,
            skilled_hireling_cost_per_day=skilled_hireling_cost_per_day,
            living_cost_per_person_per_day=living_cost_per_person_per_day,
            living_cost_people_count=living_cost_people_count,
            total_shop_rent_per_year=total_shop_rent,
        )

        results = calculate(cfg)

        st.write("## Final Results")
        # Pretty print with alignment
        result_lines = []
        order = [
            "Days To Simulate",
            "Workdays",
            "Total Scrolls Crafted",
            "Total Income Before Tax (GP)",
            "Total Tax Paid (GP)",
            "Total Income After Tax (GP)",
            "Total Crafting Cost (GP)",
            "Total Hireling Cost (GP)",
            "Total Living Cost (GP)",
            "Proportional Shop Rent (GP)",
            "Net Profit (GP)",
        ]
        for key in order:
            value = results[key]
            label = key.replace("(GP)", f"({currency})")
            line = f"{label:<35} {value:12.2f}"
            result_lines.append(line)
        st.code("\n".join(result_lines))

        # Optional CSV download
        csv_lines = ["Metric,Value"] + [f"{k},{results[k]:.2f}" for k in order]
        st.download_button("Download results (CSV)", data="\n".join(csv_lines), file_name="scroll_calculator_results.csv", mime="text/csv")

if __name__ == "__main__":
    main()

# add customers per week too
