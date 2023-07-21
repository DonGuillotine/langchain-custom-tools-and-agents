import speedtest

def get_internet_speed():
    st = speedtest.Speedtest()

    try:
        download_speed = st.download() / 10**6  # Convert to Mbps
        upload_speed = st.upload() / 10**6  # Convert to Mbps

        return download_speed, upload_speed
    except speedtest.SpeedtestException as e:
        print(f"An error occurred: {e}")
        return None

download_speed, upload_speed = get_internet_speed()
print(f"Download Speed: {download_speed:.2f} Mbps")
print(f"Upload Speed: {upload_speed:.2f} Mbps")
