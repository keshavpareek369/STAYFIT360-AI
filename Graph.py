import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def plot_accuracy(csv_file, exercise_name):
    """
    Plots accuracy from a given CSV file as a combined bar + line graph.
    """
    try:
        # Load data
        df = pd.read_csv(csv_file)

        # Check if the file has data
        if "Accuracy (%)" in df.columns and not df.empty:
            df["Session"] = range(1, len(df) + 1)
            plt.style.use('ggplot')

            # Create a figure
            fig, ax = plt.subplots(figsize=(10, 6))

            # Bar plot (background)
            ax.bar(df["Session"], df["Accuracy (%)"], color='skyblue', edgecolor='black', label='Accuracy (Bar)')

            # Line plot (foreground)
            ax.plot(df["Session"], df["Accuracy (%)"], marker='o', linestyle='-', color='green', linewidth=2, label='Accuracy (Line)')

            # Labels and formatting
            ax.set_xlabel("Session Number")
            ax.set_ylabel("Accuracy (%)")
            ax.set_title(f"{exercise_name} Accuracy Over Sessions")
            ax.set_ylim(-2, 105)
            ax.legend()
            ax.grid(True)

            # Display plot in Streamlit
            st.pyplot(fig)
        else:
            st.warning(f"No data available in {csv_file} to plot.")
    except FileNotFoundError:
        st.error(f"Error: {csv_file} not found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Example usage inside Streamlit
def show_graphs():
    st.write("### Biceps Curl Accuracy")
    plot_accuracy("Biceps-final.csv", "Biceps Curl")

    st.write("### Squats Accuracy")
    plot_accuracy("squats-final.csv", "Squats")

# Run only if script is executed directly
if __name__ == "__main__":
    show_graphs()
