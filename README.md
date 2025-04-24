# EduLiving

This web application is built using **Streamlit** and leverages two key datasets:
- **High School Data** in Ho Chi Minh City (HCMC)
- **Real Estate Data** in Ho Chi Minh City (HCMC)

The application serves two primary purposes:
1. **Data Analysis** - Analyzing and comparing the high school and real estate data to derive insights.
2. **Recommendation Chatbot** - Providing users with real estate recommendations near the high school of their choice based on their budget.

## Features

### 1. **Data Analysis Tab**
   - **Overview**: This tab allows users to explore and analyze two datasets:
     - High School Data: Information on various high schools in HCMC, such as location, reputation, and school type.
     - Real Estate Data: Listings of properties for sale or rent around HCMC, including location, price range, and property type.
   - **Capabilities**:
     - Visualize trends, comparisons, and relationships between the high school locations and nearby real estate listings.
     - Analyze the distribution of real estate prices and the proximity to high schools.
     - Generate insights about the best real estate areas based on school ratings and affordability.

### 2. **Recommendation Chatbot Tab**
   - **Overview**: The chatbot helps users find real estate options based on two inputs:
     - **High School**: The user can select their preferred high school from the list.
     - **Budget Range**: Users specify their budget range for buying or renting property.
   - **Capabilities**:
     - The chatbot will process the user’s input and provide a list of real estate recommendations that meet their criteria.
     - Recommendations are tailored to offer properties that are close to the selected high school and fall within the specified budget range.

## Technologies Used
- **Streamlit**: For creating the interactive user interface.
- **Pandas**: For data processing and analysis.
- **Matplotlib/Seaborn**: For visualizing the data.
- **Python**: For scripting the back-end logic.

## Installation

To run this web application locally, follow these steps:

1. **Clone the repository**:
   ```
   git clone https://github.com/your-repository-name
   cd your-repository-name
   ```

2. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app**:
   ```
   streamlit run app.py
   ```

4. Open the app in your browser (Streamlit will provide a URL like `http://localhost:8501`).

## Data Sources
- **High School Data**: Contains information on various high schools in HCMC (location, name, reputation, etc.)
- **Real Estate Data**: Contains listings of properties for sale or rent around HCMC (location, price, property type, etc.)

Both datasets are pre-processed and integrated into the application for analysis and recommendations.

## Contributions

Feel free to contribute by:
- Reporting bugs or issues
- Suggesting improvements
- Adding new features

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Let me know if you need any adjustments or further details!
