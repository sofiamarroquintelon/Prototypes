import streamlit as st
import pandas as pd
import plotly.express as px


df = pd.read_csv('hotel_bookings.csv')
st.title('Hotel Booking')

#first tab- Information about bookings in each hotel 
def display_calendar(df):
    st.header("Reservations/Cancellations Calendar")

    #Had to convert the data into datetime format
    df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'], errors='coerce')
    df = df.dropna(subset=['reservation_status_date'])

    #Get the timeline of the dataset ( since when to when we have reservations) 
    min_date = df['reservation_status_date'].min().date()
    max_date = df['reservation_status_date'].max().date()
    default_date = min_date

    #Input/select a date 
    selected_date = st.date_input("Select a Date:", value=default_date, min_value=min_date, max_value=max_date)

    #Select ONE hotel
    available_hotels = df["hotel"].unique().tolist()
    selected_hotel = st.radio(
        "Select Hotel Type:", 
        options=available_hotels,
        index=0 
    )

    #Select the booking status you want to see (multiselect)
    available_statuses = df["reservation_status"].unique().tolist()
    selected_statuses = st.multiselect(
        "Reservations:",
        options=available_statuses,
        default=available_statuses,
        key="calendar_status"  # chat gave me this one to avoid conflicts because i had an error with this part of the code
    )

    #filter data 
    df_filtered = df[
        (df["reservation_status_date"] == pd.Timestamp(selected_date)) & 
        (df["hotel"] == selected_hotel) & 
        (df["reservation_status"].isin(selected_statuses))
    ]

    if df_filtered.empty:
        st.warning(f"No reservations found for {selected_date} at {selected_hotel}.")
    else:
        #I filtered the data to show just a part of the dataset, the important columns for "bookings"
        df_filtered = df_filtered[[
            "hotel", 
            "reservation_status",
            "assigned_room_type",
            "stays_in_week_nights",
            "stays_in_weekend_nights"
        ]]

        # Rename columns to have a clear name
        df_filtered = df_filtered.rename(columns={
            "hotel": "Hotel",
            "reservation_status": "Status",
            "assigned_room_type": "Room Type",
            "stays_in_week_nights": "Week Nights",
            "stays_in_weekend_nights": "Weekend Nights"
        })
        st.dataframe(df_filtered)
    
def display_frequent_customers(df):
    st.header("Loyal Customers")

    selected_hotels = st.multiselect( #Botton to select the hotel you want to see 
        "Select Hotel Type:",
        options=["Resort Hotel", "City Hotel"],
        default=["Resort Hotel", "City Hotel"] 
    ) 


    selected_guest_types = st.multiselect( #Botton to select the type of guest you want to see 
        "Select Guest Type:",
        options=["Loyal Guests", "New Guests"],
        default=["Loyal Guests", "New Guests"] 
    )


    df_filtered = df[df["hotel"].isin(selected_hotels)] #Filter for the hotel info

    #filter for the guest info 
    if "Loyal Guests" in selected_guest_types and "New Guests" in selected_guest_types:
        pass 
    elif "Loyal Guests" in selected_guest_types:
        df_filtered = df_filtered[df_filtered["is_repeated_guest"] == 1]
    elif "New Guests" in selected_guest_types:
        df_filtered = df_filtered[df_filtered["is_repeated_guest"] == 0]
    else:
        st.warning("Select at least one guest type.")
        return

    if df_filtered.empty:
        st.warning("No guests match.")
    else:
        df_filtered = df_filtered[[
            "hotel", 
            "is_repeated_guest", 
            "country" 
        ]]

        df_filtered = df_filtered.rename(columns={
            "hotel": "Hotel Type",
            "is_repeated_guest": "Customer Type",
            "country": "Country of Origin"
        })

        df_filtered["Customer Type"] = df_filtered["Customer Type"].apply(lambda x: "Loyal Guest" if x == 1 else "New Guest")

        st.dataframe(df_filtered)

        #Count customers per country
        country_counts = df_filtered["Country of Origin"].value_counts().reset_index()
        country_counts.columns = ["Country", "Number of Guests"]

        #Use a pie chart to see the distribution
        st.write("### Guests of each country")
        fig = px.pie(country_counts, names="Country", values="Number of Guests")  
        st.plotly_chart(fig)


def display_guest_origin_map(df):

    
    #group the info by country and count how many guests are from that country 
    df_filtered = df.groupby("country").size().reset_index(name="count")

    #create the chorepleth map *chat helped me a bit* 
    fig = px.choropleth(df_filtered, locations="country", locationmode="ISO-3", 
                        color="count", hover_name="country", color_continuous_scale="blues")
    fig.update_layout(title="Guests around the world")
    st.plotly_chart(fig)

#I created the 3 different tabs 
tab_calendar, tab_customers, tab_rooms = st.tabs( 
    ["Reservations Calendar", "Loyal Customers", "Map"]
)
with tab_calendar:
    display_calendar(df)

with tab_customers:
    display_frequent_customers(df)

with tab_rooms:
    display_guest_origin_map(df)

