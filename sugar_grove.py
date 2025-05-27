import streamlit as st
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import time


def scrape_data(parcel_numbers, selected_fields):
    rows = []
    total_requests = len(parcel_numbers)
    start_time = time.time()

    for idx, parcel_number in enumerate(parcel_numbers, start=1):
        url = f'https://www.sugargrovetownship.com/Assessor/Parcel/{parcel_number}'

        headers = {
            'authority': 'www.sugargrovetownship.com',
            'method': 'GET',
            'path': f'/Assessor/Parcel/{parcel_number}',
            'scheme': 'https',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Cookie': 'ASP.NET_SessionId=pa3ussxwpvx01k0ok3p04ayf',
            'Priority': 'u=0, i',
            'Referer': 'https://www.sugargrovetownship.com/Assessor/Addresses',
            'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': "Windows",
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }

        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            soup_str = str(soup)

            # Initialize scraped_data dictionary
            scraped_data = {
                'parcel_number': '',
                'address': '',
                'billing_info': '',
                'subdivision': '',
                'neighborhood_code': '',
                'lot_number': '',
                'lot_sqft': '',
                'property_class': '',
                'model_name': '',
                'style': '',
                'garage': '',
                'total_building_sqft': '',
                'basement': '',
                'year_built': '',
                'central_air': '',
                'total_rooms': '',
                'fireplace': '',
                'bedrooms': '',
                'porch': '',
                'values_2025': ''
            }

            if 'parcel_number' in selected_fields:
                parcel_num = re.findall(r'style="color:#0000ff;">[^<>]*', soup_str)
                parcel_num = ''.join(parcel_num).replace('style="color:#0000ff;">', '')
                scraped_data['parcel_number'] = parcel_num

            if 'address' in selected_fields:
                address = re.findall(r'Property Address\s+<\/div>\s+[^<>]*<br\/>\s+[^<>]*', soup_str)
                address = ''.join(address)
                address = re.sub(r'\s+', ' ', address)
                scraped_data['address'] = address

            if 'billing_info' in selected_fields:
                billing_info = re.findall(r'Billing Information\s+<\/div>\s+[^<>]*<br\/>\s+[^<>]*', soup_str)
                billing_info = ''.join(billing_info)
                billing_info = re.sub(r'\s+', ' ', billing_info)
                scraped_data['billing_info'] = billing_info

            if 'subdivision' in selected_fields:
                subdivision = re.findall(r'Subdivision:<\/td>\s+<td>[^<>]*', soup_str)
                subdivision = ''.join(subdivision).replace('Subdivision:</td>\n<td>', '')
                scraped_data['subdivision'] = subdivision

            if 'neighborhood_code' in selected_fields:
                neighborhood_code = re.findall(r'Neighborhood Code:<\/td>\s+<td>[^<>]*', soup_str)
                neighborhood_code = ''.join(neighborhood_code).replace('Neighborhood Code:</td>\n<td>', '')
                scraped_data['neighborhood_code'] = neighborhood_code

            if 'lot_number' in selected_fields:
                lot_number = re.findall(r'Lot Number:<\/td>\s+<td>[^<>]*', soup_str)
                lot_number = ''.join(lot_number).replace('Lot Number:</td>\n<td>', '')
                scraped_data['lot_number'] = lot_number

            if 'lot_sqft' in selected_fields:
                lot_sqft = re.findall(r'Lot Sqft:<\/td>\s+<td>[^<>]*', soup_str)
                lot_sqft = ''.join(lot_sqft).replace('Lot Sqft:</td>\n<td>', '')
                scraped_data['lot_sqft'] = lot_sqft

            if 'property_class' in selected_fields:
                property_class = re.findall(r'Property Class:<\/td>\s+<td>[^<>]*', soup_str)
                property_class = ''.join(property_class).replace('Property Class:</td>\n<td>', '')
                scraped_data['property_class'] = property_class

            if 'model_name' in selected_fields:
                model_name = re.findall(r'Model Name:<\/td>\s+<td[^<>]*>[^<>]*', soup_str)
                model_name = '|'.join(model_name).replace('Model Name:</td>\n<td colspan="3">', '')
                scraped_data['model_name'] = model_name

            if 'style' in selected_fields:
                style = re.findall(r'Style:<\/td>\s+<td[^<>]*>[^<>]*', soup_str)
                style = '|'.join(style).replace('Style:</td>\n<td style="width:100px;">', '')
                scraped_data['style'] = style

            if 'garage' in selected_fields:
                garage = re.findall(r'Garage:<\/td>\s+<td[^<>]*>[^<>]*', soup_str)
                garage = '|'.join(garage).replace('Garage:</td>\n<td>', '')
                scraped_data['garage'] = garage

            if 'total_building_sqft' in selected_fields:
                total_building_sqft = re.findall(r'Total Building Sqft:<\/td>\s+<td[^<>]*>[^<>]*', soup_str)
                total_building_sqft = '|'.join(total_building_sqft).replace('Total Building Sqft:</td>\n<td>',
                                                                            '').strip()
                scraped_data['total_building_sqft'] = total_building_sqft

            if 'basement' in selected_fields:
                basement = re.findall(r'Basement:<\/td>\s+<td[^<>]*>[^<>]*', soup_str)
                basement = '|'.join(basement).replace('Basement:</td>\n<td>', '').strip()
                scraped_data['basement'] = basement

            if 'year_built' in selected_fields:
                year_built = re.findall(r'Year Built:<\/td>\s+<td[^<>]*>[^<>]*', soup_str)
                year_built = '|'.join(year_built).replace('Year Built:</td>\n<td>', '')
                scraped_data['year_built'] = year_built

            if 'central_air' in selected_fields:
                central_air = re.findall(r'Central Air:<\/td>\s+<td[^<>]*>[^<>]*', soup_str)
                central_air = '|'.join(central_air).replace('Central Air:</td>\n<td>', '')
                scraped_data['central_air'] = central_air

            if 'total_rooms' in selected_fields:
                total_rooms = re.findall(r'Total Rooms:<\/td>\s+<td[^<>]*>[^<>]*', soup_str)
                total_rooms = '|'.join(total_rooms).replace('Total Rooms:</td>\n<td>', '')
                scraped_data['total_rooms'] = total_rooms

            if 'fireplace' in selected_fields:
                fireplace = re.findall(r'Fireplace:<\/td>\s+<td[^<>]*>[^<>]*', soup_str)
                fireplace = '|'.join(fireplace).replace('Fireplace:</td>\n<td>', '')
                scraped_data['fireplace'] = fireplace

            if 'bedrooms' in selected_fields:
                bedrooms = re.findall(r'Bedrooms:<\/td>\s+<td[^<>]*>[^<>]*', soup_str)
                bedrooms = '|'.join(bedrooms).replace('Bedrooms:</td>\n<td>', '')
                scraped_data['bedrooms'] = bedrooms

            if 'porch' in selected_fields:
                porch = re.findall(r'Porch:<\/td>\s+<td[^<>]*>[^<>]*', soup_str)
                porch = '|'.join(porch).replace('Porch:</td>\n<td>', '')
                scraped_data['porch'] = porch

            if 'values_2025' in selected_fields:
                values_2025 = re.findall(
                    r'2025<\/td>\s+<td>[^<>]*<\/td>\s+<td>[^<>]*<\/td>\s+<td>[^<>]*<\/td>\s+<td>[^<>]*<\/td>\s+<td>[^<>]*',
                    soup_str)
                values_2025 = ''.join(values_2025)
                values_2025 = re.sub(r'\s+', ' ', values_2025)
                values_2025 = re.sub('</td> <td>', '|', values_2025)
                scraped_data['values_2025'] = values_2025

            # Create a dictionary to store the scraped data
            row_dict = {'input_parcel_number': parcel_number}

            # Only include selected fields in the output
            for field in selected_fields:
                if field in scraped_data:
                    row_dict[field] = scraped_data[field]

            rows.append(row_dict)

            # Display progress and estimated time remaining
            elapsed_time = time.time() - start_time
            avg_time_per_request = elapsed_time / idx if idx > 0 else 0
            remaining_requests = total_requests - idx
            estimated_time_remaining = avg_time_per_request * remaining_requests

            st.markdown(
                f"<p style='color: green;'>Processing: {idx}/{total_requests} | Estimated time remaining: {round(estimated_time_remaining, 2)} seconds</p>",
                unsafe_allow_html=True)

        except Exception as e:
            st.warning(f"Failed to fetch data for parcel number {parcel_number}: {str(e)}")
            # Set all selected fields to empty strings for failed requests
            row_dict = {'input_parcel_number': parcel_number}
            for field in selected_fields:
                row_dict[field] = ''
            rows.append(row_dict)

    result_df = pd.DataFrame(rows)
    return result_df


def main():
    st.title('Sugar Grove Township Property Scraper')
    st.write("Upload an Excel file containing 'parcel_number' column.")

    uploaded_file = st.file_uploader("Upload Excel file", type=['xlsx', 'xls'])

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)

            # Check if parcel_number column exists
            if 'parcel_number' not in df.columns:
                st.error("The uploaded file must contain a 'parcel_number' column.")
                return

            st.write(f"Found {len(df)} parcel numbers in the uploaded file.")

            min_range = st.number_input('Enter the start index of parcel numbers:', value=0, min_value=0)
            max_range = st.number_input('Enter the end index of parcel numbers:',
                                        value=min(len(df), 10),
                                        min_value=min_range + 1,
                                        max_value=len(df))

            parcel_numbers = df['parcel_number'].iloc[min_range:max_range].tolist()

            # Define available fields for selection based on Sugar Grove Township structure
            available_fields = [
                'Select All',
                'parcel_number',
                'address',
                'billing_info',
                'subdivision',
                'neighborhood_code',
                'lot_number',
                'lot_sqft',
                'property_class',
                'model_name',
                'style',
                'garage',
                'total_building_sqft',
                'basement',
                'year_built',
                'central_air',
                'total_rooms',
                'fireplace',
                'bedrooms',
                'porch',
                'values_2025'
            ]

            # Checkbox options for selecting fields
            selected_fields = st.multiselect('Select Fields for Output', available_fields,
                                             default=['parcel_number', 'address', 'property_class'])

            # Check if 'Select All' is chosen and update selected_fields accordingly
            if 'Select All' in selected_fields:
                selected_fields = available_fields[1:]  # Exclude the 'Select All' option

            if not selected_fields:
                st.warning("Please select at least one field to scrape.")
                return

            st.write(f"Will process {len(parcel_numbers)} parcel numbers with {len(selected_fields)} selected fields.")

            if st.button('Scrape Data'):
                with st.spinner('Scraping data...'):
                    scraped_data = scrape_data(parcel_numbers, selected_fields)

                st.success(f"Scraping completed! Found {len(scraped_data)} records.")
                st.write(scraped_data)

                # Download options
                col1, col2 = st.columns(2)

                with col1:
                    csv = scraped_data.to_csv(index=False)
                    st.download_button(
                        label="Download as CSV",
                        data=csv,
                        file_name='sugargrove_scraped_data.csv',
                        mime='text/csv'
                    )

                with col2:
                    # Convert to Excel for download
                    import io
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        scraped_data.to_excel(writer, index=False, sheet_name='Scraped Data')
                    excel_data = output.getvalue()

                    st.download_button(
                        label="Download as Excel",
                        data=excel_data,
                        file_name='sugargrove_scraped_data.xlsx',
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )

        except Exception as e:
            st.error(f"Error processing file: {str(e)}")


if __name__ == "__main__":
    main()